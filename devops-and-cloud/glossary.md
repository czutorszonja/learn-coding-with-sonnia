# 📖 Glossary — Devops & Cloud

A quick-reference dictionary of every term we've covered.

---

## Docker

| Term | What it is |
|---|---|
| **Container** | A running instance of a Docker image. Lightweight, isolated process. |
| **Image** | A frozen, immutable snapshot of an app and its dependencies. |
| **Dockerfile** | A text file with instructions to build a Docker image. |
| **Layer** | Each instruction in a Dockerfile creates a layer. Layers are cached and reused. |
| **Volume** | Persistent storage that survives container deletion. |
| **Bind mount** | Maps a specific folder on your machine into a container. Used for development. |
| **Port mapping** | Connects a port on your machine to a port inside the container (`-p 8080:80`). |
| **Docker Compose** | A tool to define and run multi-container apps with a YAML file. |
| **Docker Hub** | The public registry where Docker images are shared. |
| **Registry** | A place to store Docker images (Docker Hub, ECR, etc.). |
| **Tag** | A label for an image version (`my-app:latest`, `my-app:v1.2.3`). |
| **Multi-stage build** | Using multiple FROM statements to keep the final image small. |
| **Health check** | A command Docker runs periodically to verify the container is working. |
| **Entrypoint** | The executable that runs when the container starts. |
| **CMD** | Default arguments passed to ENTRYPOINT. |

### Docker CLI Commands

```
docker pull <image>          Download an image
docker run <image>           Start a container from an image
docker ps                    List running containers
docker ps -a                 List all containers (including stopped)
docker stop <container>      Stop a running container
docker start <container>     Start a stopped container
docker rm <container>        Remove a container
docker images                List images
docker rmi <image>           Remove an image
docker build -t <name> .     Build an image from a Dockerfile
docker exec -it <container> <cmd>  Run a command inside a running container
docker logs <container>      View container logs
docker compose up            Start all services (Compose)
docker compose down          Stop all services (Compose)
docker compose logs          View logs from all services
docker volume ls             List volumes
docker network ls            List networks
```

---

## AWS

| Term | What it is |
|---|---|
| **Region** | A geographic area with multiple data centres (eu-west-2 = London). |
| **Availability Zone (AZ)** | One or more data centres within a region. |
| **IAM** | Identity and Access Management — who can do what in your account. |
| **Root user** | The account owner (full access). Use only for setup. |
| **IAM user** | A person or service with specific permissions. |
| **IAM role** | A set of permissions an AWS service can assume (e.g., EC2 reading S3). |
| **Policy** | A JSON document that defines permissions. |
| **ARN** | Amazon Resource Name — unique identifier for any AWS resource. |
| **S3** | Simple Storage Service — store and retrieve files. |
| **Bucket** | A top-level folder in S3 (globally unique name). |
| **Object** | A file stored in S3 (data + metadata + key). |
| **Storage class** | The tier of S3 storage (Standard, Glacier, etc.). |
| **EC2** | Elastic Compute Cloud — virtual servers in the cloud. |
| **Instance** | A single virtual machine running on AWS. |
| **AMI** | Amazon Machine Image — the OS template for an EC2 instance. |
| **Security Group** | A virtual firewall for EC2 instances (what traffic is allowed). |
| **Elastic IP** | A static, fixed IP address you can attach to an instance. |
| **Key pair** | SSH keys for connecting to EC2 (public key on AWS, private key with you). |
| **Lambda** | Serverless functions — code that runs on-demand, no server management. |
| **Trigger** | An event that causes a Lambda function to run. |
| **API Gateway** | Service to create, deploy, and manage REST APIs. |
| **CloudWatch** | Monitoring and logging for AWS services. |
| **ECS** | Elastic Container Service — run Docker containers on AWS. |
| **Fargate** | Serverless compute engine for ECS — no servers to manage. |
| **Task definition** | The recipe for running a container on ECS (image, ports, env vars). |
| **Task** | One running instance of a task definition. |
| **Service** | Ensures a specified number of tasks stay running, handles rolling updates. |
| **ECR** | Elastic Container Registry — store Docker images on AWS. |
| **RDS** | Relational Database Service — managed PostgreSQL, MySQL, etc. |
| **ALB** | Application Load Balancer — distributes traffic across containers/servers. |
| **CloudFront** | Content Delivery Network (CDN) — fast global content delivery. |
| **Route 53** | DNS service — domain names to IP addresses. |
| **DynamoDB** | NoSQL database — key-value and document store. |
| **VPC** | Virtual Private Cloud — your isolated network on AWS. |
| **Free Tier** | Free usage limits for 12 months after account creation. |

### AWS CLI Commands

```
aws configure                           Set up credentials
aws s3 mb s3://bucket-name              Create a bucket
aws s3 ls                               List buckets
aws s3 cp file.txt s3://bucket/         Upload a file
aws s3 cp s3://bucket/file.txt ./       Download a file
aws s3 sync ./local s3://bucket/        Sync a directory to S3
aws ec2 run-instances --image-id ami-xxx --instance-type t2.micro
aws ec2 stop-instances --instance-ids i-xxx
aws ec2 terminate-instances --instance-ids i-xxx
aws lambda invoke --function-name my-func output.json
aws ecs create-cluster --cluster-name my-cluster
aws ecs register-task-definition --cli-input-json file://task.json
aws logs tail /ecs/my-app --follow
```

---

## Cloud Concepts

| Term | What it is |
|---|---|
| **Cloud computing** | Renting compute resources over the internet instead of owning hardware. |
| **IaaS** | Infrastructure as a Service — rent raw compute, storage, networking (EC2, S3). |
| **PaaS** | Platform as a Service — deploy apps without managing the underlying OS (Elastic Beanstalk). |
| **SaaS** | Software as a Service — ready-to-use software (Gmail, Notion, Slack). |
| **Serverless** | Run code without provisioning servers (Lambda, Fargate). Pay only for execution time. |
| **Scalability** | The ability to handle more load by adding resources (EC2 auto-scaling groups). |
| **High availability** | Remaining operational despite failures (Multi-AZ RDS). |
| **CDN** | Content Delivery Network — cache content at edge locations worldwide for faster delivery. |
| **DNS** | Domain Name System — translates domain names (sonnia.ai) to IP addresses. |
| **Load balancing** | Distributing incoming traffic across multiple servers to prevent overload. |
| **IaC** | Infrastructure as Code — managing infrastructure with config files (Terraform, CloudFormation). |
| **CI/CD** | Continuous Integration / Continuous Deployment — automatically test and deploy code changes. |

---

## Quick Checks

### "Is my container running?"
```bash
docker ps | grep my-app
curl http://localhost:5000/health
```

### "Did my Docker build fail?"
```bash
docker build -t my-app . 2>&1 | tail -20
```

### "Why can't I connect to my database?"
- Check `DB_HOST` env var — probably `localhost` instead of the service name
- Check port — are you using the container port (5432) or mapped port?
- Is the database service started? `docker compose ps`

### "Is my AWS bill going to surprise me?"
- Check **Billing Dashboard** → **Budgets**
- Check **Cost Explorer**
- Check if any EC2/RDS instances are running: `aws ec2 describe-instances | grep running`

### "Why can't I SSH into my EC2 instance?"
- Is the security group allowing port 22 from your IP?
- Is your key pair file permissions correct? (`chmod 400 key.pem`)
- Is the instance actually running? (Check EC2 console)
- Check the correct username: `ec2-user` (Amazon Linux), `ubuntu` (Ubuntu), `admin` (some AMIs)

### "My Lambda function timed out"
- Default timeout is 3 seconds — increase to 30 seconds for API calls
- Check if it needs more memory (more memory = more CPU)
- Check CloudWatch Logs for the timeout error

---

*This glossary will grow as you do. Add your own notes.*
