# 07 — ECS: Running Docker on AWS

**← Back to [Lesson 06: Lambda: Code Without Servers](06-aws-lambda.md)**


You've containerised your app with Docker. Now let's run it in the cloud — properly.

EC2 was "rent a server and install Docker." **ECS** (Elastic Container Service) is "give me your Docker image and I'll run it for you — scaling, load balancing, health checks included."

---

## 1. The Problem EC2 Doesn't Solve

Running Docker on EC2 (lesson 5) works, but you're still managing:

- What happens if the EC2 instance dies?
- What if traffic spikes — who launches more instances?
- How do you roll out a new version without downtime?
- Where do you store your Docker images?

ECS answers all of this.

---

## 2. ECS vs Fargate (Serverless Containers)

ECS has two modes:

| | **ECS (EC2)** | **ECS Fargate** |
|---|---|---|
| You manage | The EC2 cluster (servers) | Nothing |
| AWS manages | The containers on your servers | Both servers AND containers |
| Best for | Large workloads, cost optimisation | Simplicity, variable traffic |
| Cost | Cheaper for steady high traffic | More expensive but worry-free |

**For beginners: use Fargate.** You write a Dockerfile, push the image, and tell ECS "run this on port 5000." AWS does the rest. No servers to see.

---

## 3. The Pieces of ECS

```
                 ┌──────────────────────────────────────┐
                 │          ECS Cluster                  │
                 │                                      │
                 │  ┌──────────────────────────────┐    │
                 │  │  Task Definition              │    │
                 │  │  (recipe: image, ports, env)   │    │
                 │  └──────┬───────────────────────┘    │
                 │         │                             │
                 │  ┌──────▼───────────────────────┐    │
                 │  │  Service                      │    │
                 │  │  (keeps N tasks running,      │    │
                 │  │   health checks, rolling       │    │
                 │  │   deployments)                 │    │
                 │  └──────┬───────────────────────┘    │
                 │         │                             │
                 │  ┌──────▼──────┐  ┌──────▼──────┐   │
                 │  │  Task 1     │  │  Task 2     │   │
                 │  │  (running   │  │  (running   │   │
                 │  │   container)│  │   container)│   │
                 │  └─────────────┘  └─────────────┘   │
                 └──────────────────────────────────────┘
```

| Component | What it is | Analogy |
|---|---|---|
| **Cluster** | Your container namespace | Your kitchen |
| **Task Definition** | Recipe for your container (like a Dockerfile + compose) | A cake recipe |
| **Task** | One running instance of a task definition | One cake baking |
| **Service** | Ensures N tasks are always running, handles rollouts | The bakery manager |
| **ECR** | Docker image registry (like Docker Hub but on AWS) | The pantry |

---

## 4. Step by Step: Deploy the URL Shortener to ECS

### Step 1: Push your image to ECR

```bash
# Login to ECR
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.eu-west-2.amazonaws.com

# Create a repository
aws ecr create-repository --repository-name url-shortener --region eu-west-2

# Build, tag, and push
docker build -t url-shortener ./backend
docker tag url-shortener:latest <account-id>.dkr.ecr.eu-west-2.amazonaws.com/url-shortener:latest
docker push <account-id>.dkr.ecr.eu-west-2.amazonaws.com/url-shortener:latest
```

### Step 2: Create a Task Definition

```json
{
  "family": "url-shortener",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::<account-id>:role/ecsTaskExecutionRole",
  "containerDefinitions": [{
    "name": "api",
    "image": "<account-id>.dkr.ecr.eu-west-2.amazonaws.com/url-shortener:latest",
    "portMappings": [{"containerPort": 5000, "protocol": "tcp"}],
    "environment": [
      {"name": "DB_HOST", "value": "<rds-endpoint>"},
      {"name": "DB_NAME", "value": "urlshortener"},
      {"name": "DB_USER", "value": "postgres"},
      {"name": "DB_PASSWORD", "value": "secret"},
      {"name": "REDIS_HOST", "value": "<elasticache-endpoint>"}
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/url-shortener",
        "awslogs-region": "eu-west-2",
        "awslogs-stream-prefix": "ecs"
      }
    }
  }]
}
```

### Step 3: Create a Service

Via Console:
1. Go to **ECS** → **Clusters** → **Create Cluster** → **Networking only (Fargate)** → Name: `url-shortener-cluster`
2. Go to **Task Definitions** → **Create new Task Definition** → **FARGATE** → paste JSON above
3. Go to your cluster → **Create Service** → choose the task definition, set desired tasks to **1**, add a load balancer

### Step 4: Add a Load Balancer

An Application Load Balancer (ALB) sits in front of your containers:

```
User → https://app.example.com → ALB (port 443) → ECS Task (port 5000)
```

The ALB:
- Distributes traffic across multiple tasks
- Runs health checks (your `/health` endpoint)
- Handles SSL/TLS certificates
- Routes traffic based on path (`/api/*` → one service, `/static/*` → another)

### Step 5: RDS (Managed PostgreSQL)

Instead of running PostgreSQL in a container (which loses data on restart), use **RDS**:

```bash
# macOS / Linux
aws rds create-db-instance --db-instance-identifier url-shortener-db --db-instance-class db.t3.micro --engine postgres --master-username postgres --master-user-password secret --allocated-storage 20 --region eu-west-2

# Windows PowerShell — put it on one line (same command, no backslashes)
# Or use backtick continuations if you prefer:
# aws rds create-db-instance `
#   --db-instance-identifier url-shortener-db `
#   --engine postgres --master-username postgres
#   (etc.)
```

RDS gives you:
- Automated backups (point-in-time recovery)
- Multi-AZ for high availability
- Automated patching

---

## 5. ECS with Docker Compose (Preview)

AWS now supports running Docker Compose files directly on ECS:

```bash
# Deploy your docker-compose.yml to ECS Fargate
docker compose -f docker-compose.yml up -d
```

This creates ECS task definitions, services, and a load balancer **from your compose file**. Most of your local setup translates directly to production.

---

## 6. Deploying Updates

When you update your app:

1. Push the new version of your image to ECR (or update your task definition to use a different public image)
2. Update the task definition (point to the new image tag)
3. Update the service with the new task definition revision
4. ECS performs a **rolling update** — starts new tasks, stops old ones

```bash
# Trigger a new deployment
aws ecs update-service --cluster hello-cluster --service hello-service --force-new-deployment
```

Zero downtime. ECS starts new tasks, waits for health checks, then stops the old ones.

---

## 7. Monitoring with CloudWatch

ECS automatically sends logs to CloudWatch:

```bash
# View logs
aws logs tail /ecs/hello-app --follow

# See metrics
aws cloudwatch get-metric-statistics --namespace AWS/ECS --metric-name CPUUtilization --dimensions Name=ServiceName,Value=hello-service
```

Set up alarms:
- CPU > 80% → add more tasks
- Health check fails → send SMS
- Error count spikes → rollback

---

## 🔨 Your Turn

1. Create an ECS cluster with Fargate
2. Use the public sample image (`public.ecr.aws/ecs-sample-image/hello-world`) to create a task definition
3. Create a service with 1 running task
4. Find the public IP of your task and visit it in your browser
5. Scale the service to 3 tasks — what happens?
6. Clean up: delete the service, cluster, and any resources created

> **📁 Deploy your own app?** If you've completed the Docker lessons, come back and try pushing your own image to ECR instead of the sample.

**Continue to [Lesson 08: Final Project: Full-Stack Notes App on AWS](08-aws-project.md)**
