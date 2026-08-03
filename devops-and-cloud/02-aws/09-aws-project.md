# 08 — Final Project: Full-Stack Notes App on AWS

**← Back to [Lesson 08: ECS: Running Docker on AWS](08-aws-ecs.md)**


This is where everything comes together. We'll build and **deploy a full-stack Notes app to AWS** — entirely serverless, with no servers to manage.

You'll use:
- **Lambda + API Gateway** → serverless API endpoints
- **DynamoDB** → database
- **S3 + CloudFront** → static frontend and CDN
- **CloudWatch** → monitoring and logs
- *(Optional: containerised deployment with ECS if you've done the Docker lessons)*

---

## Architecture Overview

```
                    ┌──────────────┐
                    │  CloudFront   │
                    │  (CDN)        │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  S3           │
                    │  (Static     │
                    │   Frontend)  │
                    └──────────────┘

                    ┌──────────────┐
                    │  API Gateway  │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  Lambda       │
                    │  (Backend     │
                    │   Logic)      │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  DynamoDB    │
                    │  (Database)  │
                    └──────────────┘
```

All serverless — no servers to manage, minimum cost, auto-scaling.

> **Containerised option:** If you've completed the Docker lessons and want to deploy via ECS + RDS instead, the **ECS lesson** covers those building blocks — same concepts, different packaging.

---

## Deploy the Serverless Backend (Lambda + DynamoDB)

For simple apps, this costs essentially **nothing** at low traffic.

### Step 1: Create DynamoDB Table

```bash
# macOS / Linux
aws dynamodb create-table --table-name notes --attribute-definitions '[{"AttributeName":"id","AttributeType":"S"}]' --key-schema '[{"AttributeName":"id","KeyType":"HASH"}]' --billing-mode PAY_PER_REQUEST

# Windows PowerShell — same command on one line
# aws dynamodb create-table --table-name notes --attribute-definitions '[{"AttributeName":"id","AttributeType":"S"}]' --key-schema '[{"AttributeName":"id","KeyType":"HASH"}]' --billing-mode PAY_PER_REQUEST
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

Upload to S3 and enable static website hosting (lesson 4). Put CloudFront in front for HTTPS and speed.

---

## Monitoring and Alerting

```bash
# macOS / Linux — Create a CloudWatch dashboard
aws cloudwatch put-dashboard --dashboard-name NotesApp \
  --dashboard-body '{
    "widgets": [{
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/Lambda", "Invocations", {"stat": "Sum"}],
          ["AWS/Lambda", "Errors", {"stat": "Sum"}],
          ["AWS/API Gateway", "Count", {"stat": "Sum"}]
        ],
        "period": 300,
        "stat": "Average",
        "region": "eu-west-2",
        "title": "Notes App"
      }
    }]
  }'
```

**Set up alerts for:**
- Lambda errors > 0 → check the logs
- API Gateway 5xx errors > 1% → notify you
- DynamoDB throttled requests > 0 → check capacity

---

## Clean Up Checklist

AWS costs real money if you leave things running. After you're done:

```bash
# S3 bucket (must be empty first)
aws s3 rm s3://notes-app-bucket --recursive
aws s3 rb s3://notes-app-bucket

# Lambda functions (delete from console)
# API Gateway API (delete from console)

# DynamoDB table
aws dynamodb delete-table --table-name notes

# CloudWatch log groups
aws logs delete-log-group --log-group-name /aws/lambda/notes-api
```

Always check the **Billing Dashboard** after cleaning up to confirm nothing is still accruing.

---

## What You've Built

By completing this project, you've built what a real startup would call their **MVP (Minimum Viable Product)**:

- ✅ A fully serverless API with Lambda + API Gateway
- ✅ DynamoDB as a managed database with auto-scaling
- ✅ A static frontend on S3 + CloudFront CDN
- ✅ Static assets served from a CDN
- ✅ Monitoring and alerts
- ✅ Multi-environment infrastructure

Everything from serverless functions to a global CDN — that's the power of AWS. ☁️

---

## 🔨 Your Turn

1. Create the DynamoDB table for notes
2. Write the Lambda function for the Notes API (use the code from this lesson)
3. Set up API Gateway with GET, POST, DELETE methods
4. Test your API with `curl`
5. Host the static frontend (even a basic HTML page) on S3 → CloudFront
6. Set up a CloudWatch dashboard to see your metrics
7. **Crucially:** clean everything up when you're done, then check the billing dashboard

> **Want to deploy with containers instead?** If you've completed the Docker lessons, check the **ECS lesson** for the containerised deployment pattern — it builds on the same architecture but packages your app differently.

> **Final stop:** Check the **glossary.md** for a quick reference of every term and command we've covered.
