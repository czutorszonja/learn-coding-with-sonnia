# 15 — Final Project: Full-Stack Notes App on AWS

This is where everything comes together. We'll take the URL shortener (or the note-taking API from earlier Docker lessons) and **deploy it to AWS for real** — with a serverless option and a container option.

You'll use:
- **Docker** → package the app
- **ECR** → store the image
- **ECS Fargate** → run the container
- **RDS** → managed PostgreSQL
- **S3 + CloudFront** → static assets and CDN
- **Lambda + API Gateway** → serverless endpoints
- **Route 53** → custom domain (optional)
- **CloudWatch** → monitoring and logs

---

## Architecture Overview

```
                           ┌──────────────┐
                           │  CloudFront   │
                           │  (CDN)        │
                           └────┬────┬────┘
                                │    │
                    ┌───────────┘    └───────────┐
                    ▼                             ▼
           ┌──────────────┐            ┌──────────────┐
           │  S3           │            │  ALB         │
           │  (static     │            │  (Load       │
           │   website)   │            │   Balancer)  │
           └──────────────┘            └──────┬───────┘
                                              │
                                     ┌────────▼───────┐
                                     │  ECS Fargate    │
                                     │  (Flask API)    │
                                     └────────┬───────┘
                                              │
                    ┌─────────────────────────┼──────────────┐
                    │                         │              │
           ┌────────▼───────┐       ┌─────────▼───────┐     │
           │  RDS            │       │  ElastiCache    │     │
           │  (PostgreSQL)   │       │  (Redis)        │     │
           └─────────────────┘       └─────────────────┘     │
                                                             │
           ┌─────────────────────────────────────────────────┘
           │  (Serverless option)
           ▼
    ┌──────────────┐
    │  API Gateway  │
    └──────┬───────┘
           │
    ┌──────▼───────┐
    │  Lambda       │
    │  (DynamoDB)   │
    └──────────────┘
```

**Two deployment options:**
1. **Containerised** (ECS Fargate) — for when you need full control
2. **Serverless** (Lambda + DynamoDB) — for simplicity and minimal cost

---

## Option 1: Containerised Deployment (ECS + RDS)

This is what a startup would do. Docker image in ECR, run on Fargate, RDS for persistence.

### Step 1: Set up RDS PostgreSQL

```bash
# Create the database
aws rds create-db-instance \
  --db-instance-identifier notes-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username notesapp \
  --master-user-password YourStrongPassword \
  --allocated-storage 20 \
  --region eu-west-2

# Get the endpoint (takes ~5 minutes)
aws rds describe-db-instances \
  --db-instance-identifier notes-db \
  --query "DBInstances[0].Endpoint.Address"
```

**Security:** Create the RDS in a private subnet (not accessible from the internet). Only your ECS tasks can reach it.

### Step 2: Create the ECR Repository

```bash
aws ecr create-repository --repository-name notes-api --region eu-west-2
```

### Step 3: Build and Push the Docker Image

```bash
# Login
aws ecr get-login-password --region eu-west-2 | docker login \
  --username AWS --password-stdin \
  <account-id>.dkr.ecr.eu-west-2.amazonaws.com

# Build for ARM (Fargate default)
docker build --platform linux/arm64 \
  -t notes-api \
  -f backend/Dockerfile.prod \
  ./backend

# Tag and push
docker tag notes-api:latest \
  <account-id>.dkr.ecr.eu-west-2.amazonaws.com/notes-api:latest
docker push <account-id>.dkr.ecr.eu-west-2.amazonaws.com/notes-api:latest
```

### Step 4: Create the ECS Cluster and Service

```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name notes-cluster

# Register task definition (Fargate)
aws ecs register-task-definition \
  --family notes-api \
  --network-mode awsvpc \
  --requires-compatibilities FARGATE \
  --cpu 256 --memory 512 \
  --execution-role-arn arn:aws:iam::<account-id>:role/ecsTaskExecutionRole \
  --container-definitions '[
    {
      "name": "api",
      "image": "<account-id>.dkr.ecr.eu-west-2.amazonaws.com/notes-api:latest",
      "portMappings": [{"containerPort": 5000}],
      "environment": [
        {"name": "DB_HOST", "value": "<rds-endpoint>"},
        {"name": "DB_NAME", "value": "notes"},
        {"name": "DB_USER", "value": "notesapp"},
        {"name": "DB_PASSWORD", "value": "YourStrongPassword"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/notes-api",
          "awslogs-region": "eu-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]'

# Create a service
aws ecs create-service \
  --cluster notes-cluster \
  --service-name notes-api-service \
  --task-definition notes-api \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:eu-west-2:<account-id>:targetgroup/notes-tg/xxx,containerName=api,containerPort=5000"
```

### Step 5: Create a Load Balancer

1. Go to **EC2** → **Load Balancers** → **Create Application Load Balancer**
2. Scheme: **internet-facing**
3. Listeners: **HTTP:80** (or **HTTPS:443** with a certificate)
4. Create a **target group** for port 5000 with health check on `/health`
5. Attach the ECS service to the target group

### Step 6: Add a Custom Domain (Optional, but Fun)

1. Buy a domain on Route 53 (or use an existing one)
2. Create a **Hosted Zone**
3. Add an **A record** pointing to your ALB (alias)
4. Request an **SSL certificate** in ACM (Certificate Manager)
5. Add HTTPS listener on the ALB with the certificate

Now `https://notes.yourdomain.com` points to your app.

---

## Option 2: Serverless Deployment (Lambda + DynamoDB)

For simple apps, this costs essentially **nothing** at low traffic.

### Step 1: Create DynamoDB Table

```bash
aws dynamodb create-table \
  --table-name notes \
  --attribute-definitions '[{"AttributeName":"id","AttributeType":"S"}]' \
  --key-schema '[{"AttributeName":"id","KeyType":"HASH"}]' \
  --billing-mode PAY_PER_REQUEST
```

### Step 2: Write the Lambda Function

```python
import json
import uuid
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('notes')

def lambda_handler(event, context):
    """Notes CRUD API via API Gateway."""
    method = event['httpMethod']
    path = event['path']
    body = json.loads(event.get('body', '{}')) if event.get('body') else {}

    # GET /notes — list all notes
    if method == 'GET' and path == '/notes':
        response = table.scan()
        return json_response(response['Items'])

    # POST /notes — create a note
    if method == 'POST' and path == '/notes':
        note = {
            'id': str(uuid.uuid4()),
            'title': body.get('title', 'Untitled'),
            'body': body.get('body', ''),
            'created_at': datetime.utcnow().isoformat()
        }
        table.put_item(Item=note)
        return json_response(note, 201)

    # DELETE /notes/{id} — delete a note
    if method == 'DELETE' and path.startswith('/notes/'):
        note_id = path.split('/')[-1]
        table.delete_item(Key={'id': note_id})
        return json_response({'deleted': note_id})

    return json_response({'error': 'Not found'}, 404)


def json_response(data, status=200):
    return {
        'statusCode': status,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(data)
    }
```

### Step 3: Create the API Gateway

1. Go to **API Gateway** → **Create API** → **REST API** → **Build**
2. Protocol: REST, Name: `notes-api`
3. Create resources: `/notes` and `/notes/{id}`
4. Create methods: `GET`, `POST` on `/notes` and `DELETE` on `/notes/{id}`
5. Each method integrates with the Lambda function
6. Deploy API → **Deploy API** → Stage name: `prod`

Your API URL will be:
```
https://<api-id>.execute-api.eu-west-2.amazonaws.com/prod/notes
```

### Step 4: Add a Static Frontend on S3

Create a simple HTML frontend and serve it from S3:

```html
<!DOCTYPE html>
<html>
<head><title>My Notes</title></head>
<body>
  <h1>📝 Notes</h1>
  <div id="notes"></div>
  <script>
    const API = 'https://<api-id>.execute-api.eu-west-2.amazonaws.com/prod';

    async function loadNotes() {
      const res = await fetch(API + '/notes');
      const notes = await res.json();
      document.getElementById('notes').innerHTML = notes.map(n =>
        `<div><b>${n.title}</b>: ${n.body}</div>`
      ).join('');
    }

    loadNotes();
  </script>
</body>
</html>
```

Upload to S3 and enable static website hosting (lesson 11). Put CloudFront in front for HTTPS and speed.

---

## Monitoring and Alerting

```bash
# Create a CloudWatch dashboard
aws cloudwatch put-dashboard \
  --dashboard-name NotesApp \
  --dashboard-body '{
    "widgets": [{
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/ECS", "CPUUtilization", {"stat": "Average"}],
          ["AWS/RDS", "DatabaseConnections"]
        ],
        "period": 300,
        "stat": "Average",
        "region": "eu-west-2",
        "title": "App Metrics"
      }
    }]
  }'
```

**Set up alerts for:**
- CPU > 80% → scale up ECS tasks
- 5xx errors > 1% → notify you
- RDS storage > 85% → increase storage
- Lambda errors > 0 → check the logs

---

## Multi-Environment Strategy

Real projects have multiple environments:

```
dev.sonnia-notes.com
    │
    ├── Dev (free-tier, for experimenting)
    │   └── Smaller instances, shorter retention
    │
staging.sonnia-notes.com
    │
    ├── Staging (mirrors production)
    │   └── Same specs as prod, connected to staging DB
    │
app.sonnia-notes.com
    │
    └── Production (real users)
        └── Multi-AZ, auto-scaling, backups
```

Use **Infrastructure as Code** (Terraform, CloudFormation, or CDK) to define all of this as text files — so your staging and production are guaranteed identical, and you can recreate everything from scratch in minutes.

---

## Clean Up Checklist

AWS costs real money if you leave things running. After you're done:

```bash
# ECS
aws ecs delete-service --cluster notes-cluster --service notes-api-service --force
aws ecs delete-cluster --cluster notes-cluster

# RDS
aws rds delete-db-instance --db-instance-identifier notes-db --skip-final-snapshot

# ECR images
aws ecr delete-repository --repository-name notes-api --force

# Deleted files in S3
aws s3 rm s3://notes-app-bucket --recursive
aws s3 rb s3://notes-app-bucket

# Lambda + API Gateway (delete manually in console — harder via CLI)
# CloudWatch log groups
aws logs delete-log-group --log-group-name /ecs/notes-api
```

Always check the **Billing Dashboard** after cleaning up to confirm nothing is still accruing.

---

## What You've Built

By completing this project, you've built what a real startup would call their **MVP (Minimum Viable Product)**:

- ✅ A containerised app running 24/7 in the cloud
- ✅ A managed database with automated backups
- ✅ A load balancer for distributing traffic
- ✅ A serverless option for low-traffic endpoints
- ✅ Static assets served from a CDN
- ✅ Monitoring and alerts
- ✅ Multi-environment infrastructure

Everything from Docker to AWS, from localhost to production — that's the full stack. ☁️🐳

---

## 🔨 Your Turn

1. Deploy the containerised notes API to ECS Fargate following the steps above
2. Create the API Gateway + Lambda version and test it with `curl`
3. Host the static frontend (even a basic HTML page) on S3 → CloudFront
4. Set up a CloudWatch dashboard to see all your metrics in one place
5. **Crucially:** clean everything up when you're done, then check your billing dashboard

> **Final stop:** Check the **glossary.md** for a quick reference of every term and command we've covered.
