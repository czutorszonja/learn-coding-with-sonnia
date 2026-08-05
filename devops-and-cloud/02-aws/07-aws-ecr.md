# 07 — ECR: Your Docker Image Registry

**← Back to [Lesson 06: Lambda: Code Without Servers](06-aws-lambda.md)**


When you built Docker images you pushed them somewhere? Probably Docker Hub. But in real cloud projects you push your images into a registry *inside* your cloud account — so your cloud services can pull exactly the right version, privately, without exposing it to the world.

**ECR** (Elastic Container Registry) is AWS's answer to Docker Hub. It's where you store and version your Docker images so ECS (and other AWS services) can run them.

---

## 1. The Problem a Registry Solves

You can run containers from images stored anywhere. But storing images inside AWS gives you three big wins:

- **Privacy** — images stay in your account, not public on Docker Hub
- **Speed** — ECR lives inside AWS, so ECS pulls images fast (and historically, no data-transfer cost between ECS and ECR)
- **Security** — you control exactly who can push and pull, with IAM

Think of it like a **kitchen** (keep this image in mind for the ECS lesson next):

- The **pantry** is ECR — you don't cook straight from the delivery truck, you stock the pantry first with ingredients (your Docker images).
- The **chef** that cooks from the pantry is **ECS** (the orchestrator that runs your containers).

For now, the only part that matters here: **ECR is the shelf where you store your images** so a service can pull them later.

```
Local machine                         AWS
─────────────                         ─────
Dockerfile ── build ─▶ image ── push ─▶ ECR (your private pantry)
                                              │
                                        pull ▼
                                        ECS runs it
```

---

## 2. ECR vs Docker Hub (exam note)

Both are "registries" — places to store images. The difference is where they live and who can see them.

| | Docker Hub | ECR |
|---|---|---|
| Who runs it | A public company | AWS (inside your account) |
| Public by default? | Public repos are common | **Private by default** |
| Access control | Token / your Hub account | **IAM** (users, roles, policies) |
| Best for | Sharing open images | Production, private, cloud-native apps |
| Integration | Manual | Natively recognised by ECS, Lambda, etc. |
| Cost | Free (with limits) | Small storage + transfer cost |

**Exam takeaway:** ECR is the **AWS-native** registry — private by default, controlled by **IAM**, and designed to feed ECS. You tag images with the full ECR address so the system knows exactly which registry to use.

---

## 3. How Image Names Work in ECR

A Docker image name has parts, and in ECR the **full address** matters — you can't just call it `my-app`. The full name tells Docker *which registry* and *which repo*:

```text
<account-id>.dkr.ecr.<region>.amazonaws.com/<repository>:<tag>
    │                 │                        │          │
    │                 │                        │          └── tag (version)
    │                 │                        └── repo name
    │                 └── region (e.g. eu-west-2)
    └── your AWS account ID
```

Example:
```text
123456789012.dkr.ecr.eu-west-2.amazonaws.com/url-shortener:latest
```

Before you can `docker push`, you tag your local image with this full address:

```bash
docker tag url-shortener:latest 123456789012.dkr.ecr.eu-west-2.amazonaws.com/url-shortener:latest
```

---

## 4. Step by Step: Push Your First Image to ECR

### Step 0: Install & configure the AWS CLI (done once)

```bash
aws configure
# Enter your Access Key ID, Secret Access Key, region (eu-west-2), output format (json)
```

> 💻 Not sure where to type `aws ...` commands? Either use **AWS Cloud Shell** (the `>_` icon top-right of the console — no install needed) or your **local terminal** if the CLI is installed. Pick one path and stick with it.

### Step 1: Create a repository

Via **Console**:
1. Search **Elastic Container Registry** in the console
2. **Create repository** → name: `url-shortener` → visibility: **Private** → Create

Via **CLI**:
```bash
aws ecr create-repository --repository-name url-shortener --region eu-west-2
```

### Step 2: Log in to ECR (so Docker is allowed to push)

ECR requires Docker to authenticate with your AWS account first. This command fetches a temporary password and feeds it to Docker:

```bash
# macOS / Linux
aws ecr get-login-password --region eu-west-2 | \
  docker login --username AWS --password-stdin \
  123456789012.dkr.ecr.eu-west-2.amazonaws.com
```

> 💻 **Windows PowerShell / CMD:** the `|` pipe works in PowerShell, but if you hit quoting issues, run the two parts separately:
> ```powershell
> aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.eu-west-2.amazonaws.com
> ```
> Replace `123456789012` with your real account ID (find it top-right of the console, or `aws sts get-caller-identity`).

**Why this step?** `aws ecr get-login-password` gets a short-lived token, and `docker login` stores it. Without it, `docker push` fails with an auth error.

### Step 3: Build, tag, and push

```bash
# Build your image
docker build -t url-shortener ./backend

# Tag it with the full ECR address
docker tag url-shortener:latest 123456789012.dkr.ecr.eu-west-2.amazonaws.com/url-shortener:latest

# Push it to ECR
docker push 123456789012.dkr.ecr.eu-west-2.amazonaws.com/url-shortener:latest
```

### Step 4: Verify it's there

Via console: open your **ECR repo** → **Images** tab → you'll see the pushed image with its tag.
Via CLI:
```bash
aws ecr describe-images --repository-name url-shortener --region eu-west-2
```

---

## 5. The CLI Commands Cheatsheet

```bash
# Create a repo
aws ecr create-repository --repository-name <name> --region eu-west-2

# List repos
aws ecr describe-repositories --region eu-west-2

# Log in Docker to ECR
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com

# Tag + push
docker tag <image> <account>.dkr.ecr.<region>.amazonaws.com/<repo>:<tag>
docker push <account>.dkr.ecr.<region>.amazonaws.com/<repo>:<tag>

# Pull it back on another machine
docker pull <account>.dkr.ecr.<region>.amazonaws.com/<repo>:<tag>

# See images in a repo
aws ecr describe-images --repository-name <repo> --region eu-west-2

# Delete an image (careful!)
aws ecr batch-delete-image --repository-name <repo> --image-ids imageTag=<tag> --region eu-west-2
```

**The whole flow:**
```
docker build → docker tag → docker login (ECR) → docker push
```

---

## 6. Tags & Immutability (exam note)

- **Tags** are labels you choose (`latest`, `v1.2.3`, `prod`). `latest` is a convention, not automatic — you can tag anything as `latest`.
- By default ECR allows overwriting a tag (push `v1` again and it points to the new image).
- **Tag immutability** (a setting you can turn on) *blocks* overwriting a tag once it exists. This stops accidental "I pushed over the production tag" disasters.
- **Image scanning** — ECR can scan images for vulnerabilities (like known CVEs in base packages). Good practice to enable.

**Exam takeaway:** Tags are not version *truth* — they're mutable labels unless you enable immutability. Use unique tags (commit hash, date) for reproducible deploys.

---

## 7. ECR + IAM: Who Can Push and Pull

ECR access is controlled by **IAM** (from Lesson 02). You give users/roles permissions like:

- `ecr:CreateRepository` — make a repo
- `ecr:GetAuthorizationToken` — log in (needed for any push/pull)
- `ecr:BatchGetImage` — pull images
- `ecr:BatchCheckLayerAvailability` — pull optimisations
- `ecr:PutImage` — push images

ECS uses an IAM **role** (the execution role) to pull your image. For that to work, the role needs `ecr:GetAuthorizationToken` + `ecr:BatchGetImage` permissions — usually provided by the built-in `AmazonECSTaskExecutionRolePolicy`.

**Exam takeaway:** "ECR is public" is wrong — it's **private by default** and secured via **IAM**. The moment an ECS task can't start, a common cause is the execution role lacking ECR pull permissions.

---

## 8. Where ECR Fits Next

ECR is the *storage* half of deploying containers on AWS. The *running* half is **ECS** (Lesson 08) — you point a task definition at your ECR image and ECS runs it.

```
Push image → ECR  →   Task definition references ECR image  →   ECS runs it (Lesson 08)
```

Some other AWS services also accept images from ECR (e.g. Lambda container images) — once it's in ECR, many services can use it.

---

## 🔨 Your Turn

1. Create a private ECR repository called `url-shortener`
2. Take any Docker image you've built (or build a tiny one) and push it to ECR
3. Verify it appears under **Images** in the console / `aws ecr describe-images`
4. Pull it back to a fresh image to prove round-tripping works
5. Enable **tag immutability** — try pushing the same tag twice; what error do you get?
6. List the IAM permissions you'd need to push vs pull (hint: build a small IAM policy)

**Continue to [Lesson 08: ECS: Running Docker on AWS](08-aws-ecs.md)**
