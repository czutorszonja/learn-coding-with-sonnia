# 🗂️ Devops & Cloud — Exam Cheatsheet

Detailed reference for the whole track — commands, definitions, diagrams, and everything likely to appear in an exam. Use it alongside the full lessons, not instead of them.

**Back to [README](../README.md) · [Glossary](../glossary.md)**

---

## 0. The Big Picture

Three layers, each built on the last:

```
        ▲
        │  runs containers on many machines automatically
 ┌──────┴──────┐          ☸️ KUBERNETES
 │  CONTAINER  │  ──────▶  many machines, self-healing, scaling
 └──────┬──────┘
        │  packages your app
        ▼
 ┌──────┴──────┐          ☁️ AWS
 │  DOCKER     │  ──────▶  the cloud where you run it at scale
 └─────────────┘
```

**Mental model:** Docker = *one* container. Kubernetes = *many* containers across machines. AWS = the *infrastructure* underneath.

**Cloud service models (exam favourite):**
| Model | What you get | You manage | AWS example |
|---|---|---|---|
| **IaaS** | Raw compute, storage, network | OS, apps, runtime | EC2, S3 |
| **PaaS** | Platform to deploy apps | Just your app code | Elastic Beanstalk |
| **SaaS** | Ready-to-use software | Nothing | Gmail, Slack, Notion |

- **Serverless** = run code without managing servers (Lambda, Fargate). Pay per execution.
- **Scalability** = handle more load by adding resources (auto-scaling groups).
- **High availability** = stay up despite failures (Multi-AZ, load balancers).
- **IaC** = infrastructure managed via config files (Terraform, CloudFormation).
- **CI/CD** = automatically test & deploy code changes.

---

## 1. 🐳 Docker — package the app

### Core concepts
| Term | What it is | Analogy |
|---|---|---|
| **Image** | Frozen, immutable snapshot of app + deps | Recipe |
| **Container** | Running instance of an image | The meal / cooking it |
| **Dockerfile** | Text instructions to build an image | Recipe card |
| **Layer** | Each Dockerfile instruction creates a cached layer | Steps of the recipe |
| **Volume** | Persistent storage surviving container deletion | Kitchen pantry |
| **Bind mount** | Maps a host folder into the container (dev) | Shared cutting board |
| **Port mapping** | `-p host:container` connects your machine to the app | Door between rooms |
| **Compose** | Define + run multi-container apps from YAML | Bigger meal plan |
| **Registry** | Where images live (Docker Hub, ECR) | Store / pantry shelf |
| **Multi-stage build** | Multiple `FROM` to keep final image small | Prep in one kitchen, serve from another |
| **Network** | Isolated networks so containers talk safely | Rooms with doors |
| **ENTRYPOINT / CMD** | What runs at start (entrypoint) + default args (cmd) | The head chef + default order |

### Dockerfile essentials
```dockerfile
FROM python:3.12-slim      # base image
WORKDIR /app               # working directory
COPY . .                   # copy code in
RUN pip install -r requirements.txt   # build-time
EXPOSE 5000                # document the port (not opening it!)
CMD ["python", "app.py"]   # what runs at start
```

**EXPOSE vs `-p`:** `EXPOSE` is *documentation* only. The real port mapping is `docker run -p 8080:5000`.

### Most-used commands
```bash
docker build -t my-app .          # build from Dockerfile
docker run -p 8080:5000 my-app    # run + map port
docker run -d --name web -p 80:80 my-app   # detached + named
docker ps                         # running containers
docker ps -a                      # all (incl. stopped)
docker stop <c> ; docker start <c> ; docker restart <c>
docker rm <c>                     # remove container
docker images ; docker rmi <img>
docker logs <c> ; docker logs -f <c>
docker exec -it <c> sh            # shell inside
docker volume ls                  # list volumes
docker network ls                 # list networks
docker compose up / down / logs   # multi-container
```

### Everyday flow
```
Dockerfile → build -t → run -p → test → iterate → tag & push when done
```

---

## 2. ☸️ Kubernetes — run containers at scale

### Architecture (exam diagram)
```
                       ┌────────────────────────────────────────────┐
                       │            K8s CLUSTER                      │
                       │                                             │
                       │   ┌──── Control Plane (brain) ──────────┐   │
                       │   │ API Server │ Scheduler │ Controller │   │
                       │   │ etcd (state store)                    │   │
                       │   └──────────────────────────────────────┘   │
                       │                                             │
                       │   ┌── Worker 1 ──┐  ┌── Worker 2 ──┐       │
                       │   │ kubelet      │  │ kubelet      │       │
                       │   │ Pod  Pod     │  │ Pod  Pod  Pod│       │
                       │   └──────────────┘  └──────────────┘       │
                       └────────────────────────────────────────────┘
```
- **Control plane** = makes decisions, schedules, stores state (the manager).
- **Worker nodes** = run your containers via **kubelet** (the muscle).
- **etcd** = the database storing all cluster state — the source of truth.

### Core resources
| Resource | What it is | Analogy |
|---|---|---|
| **Pod** | Smallest deployable unit (1+ containers) | A process / small house |
| **Deployment** | Desired number of pods; handles updates, rollbacks, self-healing | The blueprint + supervisor |
| **ReplicaSet** | Created by a Deployment; ensures correct pod count | The enforcer of pod count |
| **Service** | Stable network endpoint selecting pods by label | The reception desk |
| **ConfigMap** | Non-sensitive config (env vars, files) | A sticky note wall |
| **Secret** | Sensitive config (passwords, keys), base64 | A locked drawer |
| **Volume / PV / PVC** | Persistent storage (PV = actual disk, PVC = the request) | Storage room + requisition form |
| **Namespace** | Virtual cluster within a cluster | Different departments |

**Declarative rule (exam):** You *describe the desired state* in YAML; Kubernetes (controllers) makes reality match it. Not step-by-step commands.

### Deployment YAML (know this)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 3                # I want 3 copies
  selector:
    matchLabels:
      app: api               # which pods belong here?
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: nginx:alpine
        ports:
        - containerPort: 80
```

### Service YAML + types
```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  selector:
    app: api                  # route to pods with this label
  ports:
  - protocol: TCP
    port: 80                  # service's port
    targetPort: 80            # pod's port
  type: ClusterIP             # change this for NodePort / LoadBalancer
```

| Service type | Reachable from | Used for |
|---|---|---|
| **ClusterIP** (default) | Inside the cluster only | Internal APIs, DBs |
| **NodePort** | Outside via `nodeIP:port` | Dev, simple external access |
| **LoadBalancer** | Public internet (cloud LB) | Production apps |

### Rollout & self-healing (exam)
- **Rolling update** — replaces pods gradually, zero downtime.
- **Rollback** — `kubectl rollout undo deployment/<name>`.
- **Self-healing** — failed pods are restarted/replaced automatically.
- **Scaling** — manual (`--replicas`) or automatic (HPA, horizontal pod autoscaler).

### Most-used commands
```bash
minikube start / stop / delete / status / dashboard
minikube service <svc> --url        # get a service's URL

kubectl get nodes / pods / services / deployments
kubectl get pods -o wide            # with IPs & nodes
kubectl get pods -l app=my-app      # filter by label
kubectl describe pod <pod>          # detailed info (debugging)
kubectl apply -f file.yaml          # create or update
kubectl delete -f file.yaml         # delete from file
kubectl logs <pod> ; kubectl logs -f <pod>
kubectl exec -it <pod> -- /bin/sh   # shell into a pod
kubectl scale deployment <name> --replicas=4
kubectl rollout status deployment/<name>
kubectl rollout undo deployment/<name>
```

**How they fit:**
```
Deployment → manages ReplicaSet → runs Pods → exposed via Service
```

---

## 3. ☁️ AWS — the cloud

### Core services & terms
| Service | What it is | Analogy |
|---|---|---|
| **Region / AZ** | Geography (eu-west-2 = London) / data centres within a region | City / neighbourhoods |
| **IAM** | Who can do what (users, roles, policies) | Security badges |
| **S3** | Object storage + static websites | Giant filing cabinet |
| **EC2** | Virtual servers (instances) | Renting a PC |
| **Lambda** | Serverless functions, pay per request | A waiter on demand |
| **ECS / Fargate** | Run Docker on AWS; Fargate = no servers to manage | Managed kitchen |
| **Elastic Beanstalk** | PaaS — upload code, get a public site | Full-service restaurant |
| **CloudFront** | CDN — cache content at edge for speed | Fast food chain, local branches |
| **RDS** | Managed relational databases | Hire a DBA |
| **Route 53** | DNS — domain → IP | Phone book |
| **DynamoDB** | NoSQL key-value / document store | Index cards |
| **ALB** | Application load balancer | Traffic coordinator |
| **VPC** | Your private network inside AWS | Gated community |

### IAM (exam favourite)
- **Root user** = account owner, full access; use only for setup.
- **IAM user** = person/service with specific permissions.
- **IAM role** = permissions an *AWS service* can assume (e.g., EC2 reading S3).
- **Policy** = JSON document defining permissions.
- **ARN** = Amazon Resource Name — unique ID for any resource.
- **Exam gotcha:** Billing is separate from IAM. Even admin IAM users can't see costs until the root enables *IAM access to Billing* in Account settings.

### EC2
- Instance families: **t**=general/burstable, **c**=compute, **r**=memory, **m**=balanced.
- Free tier: 750 hrs/month of `t2.micro` / `t3.micro`.
- **Security Group** = virtual firewall (allow/deny ports). Default denies inbound.
- Key pairs = SSH keys; `chmod 400 key.pem`.
- `aws ec2 stop-instances` / `terminate-instances` (terminate = delete).

### Lambda
- **Trigger** = event that invokes the function: S3, API Gateway, DynamoDB, SQS, CloudWatch Events (scheduled), SES.
- Classic pattern: upload to S3 → Lambda resizes image → save thumbnail.
- **Cost:** 1M requests + 400K GB-seconds are free tier → ~$0/month for a small function. Cheaper than an EC2 running 24/7 (~$8.50).
- Default timeout **3 s** — bump it for API calls.

### ECS / Fargate
- **Cluster** → **Task Definition** (recipe: image, ports, env) → **Task** (one running instance) → **Service** (keeps N tasks running).
- **ECR** = Docker registry inside AWS — **private by default**, secured with **IAM**. Full image name format: `<account>.dkr.ecr.<region>.amazonaws.com/<repo>:<tag>`.
- **Full ECR flow:** `docker build` → `docker tag` (to the full ECR address) → `aws ecr get-login-password | docker login` → `docker push`.
- **Exam:** tags are mutable labels (enable *tag immutability* to block overwrites); ECS pulls via an IAM execution role needing `ecr:GetAuthorizationToken` + `ecr:BatchGetImage`.
- **ALB** in front: `User → https://app → ALB (443) → ECS Task (5000)`.

### Elastic Beanstalk
- **PaaS** — you provide code, AWS provides servers, scaling, health.
- **Tiers:** Single instance (1 EC2, no LB — free-tier friendly) vs **Load balanced** (LB + auto scaling).
- Public by default: security group allows HTTP from anywhere (`0.0.0.0/0`).
- URL format: `http://<env>.<region>.elasticbeanstalk.com`
- **Exam:** load balanced can auto-scale; single instance can't. Beanstalk wraps EC2 + LB + ASG + CloudWatch.

### S3 (static website)
Five steps, both paths. Full detail in [Lesson 04](04-aws-s3.md).

1. **Create bucket** (name = your domain or unique)
2. **Objects → Upload** ← your HTML files go here (bucket *root*, not a subfolder!)
3. **Properties → Static website hosting → Enable** (`index.html`)
4. **Permissions → Bucket policy → Edit** → paste JSON (replace bucket name)
5. **Permissions → Block public access → uncheck all four boxes**

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
  }]
}
```

**"Where do I type this?"** — Only **one** place per task:
- **Web console** = paste JSON into Permissions tab edit box (click around the AWS site).
- **CLI** = Cloud Shell (`>_` icon top-right, already logged in) **or** local terminal with `aws configure` done. PowerShell/CMD can't use heredocs.

Test in an **incognito window** (a logged-in normal tab can mask permission problems).

---

## 4. 🔍 Debugging cheat

| Symptom | Likely cause | Fix |
|---|---|---|
| Container exits immediately | No long-running process / wrong CMD | Fix Dockerfile entrypoint |
| Can't reach app | Wrong port mapping | Check `-p host:container` |
| S3 static site 403 | Public access blocked / no policy | Uncheck block public access + add policy |
| S3 empty page | Files nested in subfolder | Move files to bucket root |
| `kubectl` can't connect | No cluster running | `minikube start` |
| Pod crash-loops | App error | `kubectl logs <pod>` |
| Can't reach K8s service | Wrong Service type / selector | `kubectl describe service` ; check labels match |
| AWS "Access denied" on costs | IAM can't see billing | Root enables IAM billing access |
| Can't SSH to EC2 | SG doesn't allow port 22 from your IP | Open 22 in security group |
| Lambda times out | Default 3s too short | Increase timeout / memory |

**Quick checks:**
```bash
docker ps | grep my-app
docker build -t my-app . 2>&1 | tail -20   # see build errors
curl http://localhost:5000/health
kubectl get pods ; kubectl describe pod <name> ; kubectl logs <name>
kubectl get services ; minikube service <svc> --url
aws ec2 describe-instances | grep running   # what's costing you money
```

---

## 5. ⚡ Elastic Beanstalk: `0.0.0.0` explained

**Q: Do I need `host="0.0.0.0"` in my Flask code to make it public?**

**A: Yes — keep it.**
- `app.run(host="0.0.0.0", port=5000)` tells the app to listen on **all network interfaces** on the VM. That's what lets incoming internet traffic reach it.
- If you used `host="127.0.0.1"` (localhost), the app only accepts connections from *inside the same machine*. **No AWS console setting can fix that** — the firewall is open, but the app isn't listening on the right interface.
- The **security group** in AWS (allowing `0.0.0.0/0` on port 80) is the *permission/firewall layer*; the **`0.0.0.0` in code** is the *listening layer*. **Both are needed**:

```
Internet ──▶ Security Group (firewall: port 80 open to 0.0.0.0/0) ──▶ App listening on 0.0.0.0:5000
                                    ▲ permission                          ▲ binding
```

- In **real life** you *do* keep `0.0.0.0` in code, then **restrict who** can reach it via the security group (e.g. only your office IP), put HTTPS on the load balancer, and add a WAF in front. The code listens everywhere; the firewall decides who gets in.
- Either works *technically* for a local test with `host="127.0.0.1"` — but on Beanstalk, the load balancer routes external traffic into your instance, so you must bind `0.0.0.0`.

**Exam takeaway:** `0.0.0.0` = "listen on all interfaces" (public). `127.0.0.1` = "localhost only" (private). Security group = who is *allowed* in; the binding = what the app actually *listens on*.

---

## 6. 📌 Common gotchas & one-liners

- **Heredocs** (`cat > file << EOF`) don't work in PowerShell/CMD — save JSON to a file first, or use Cloud Shell.
- **`EXPOSE`** in a Dockerfile is documentation; use `-p` to actually publish a port.
- **`kubectl apply`** is declarative; `docker run` is imperative. Exam loves "describe desired state, not steps."
- **`--force` / `--all`** flags: `kubectl delete pod --force --grace-period=0` for a stuck terminating pod.
- **Free tier isn't forever:** 12 months. Watch EC2/RDS instances you forget to stop.
- **Terminate ≠ stop** on EC2: stop keeps the disk (you keep paying for storage); terminate frees everything.

---

*Full lessons: `01-docker/`, `02-aws/`, `03-kubernetes/` · Terms: `glossary.md`*
