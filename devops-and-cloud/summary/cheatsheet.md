# 🗂️ Devops & Cloud — Cheatsheet

One-page reference for the whole track. Flip back here when you forget a command or a term. Works best as a companion to the full lessons, not a replacement.

**Back to [README](../README.md) · [Glossary](../glossary.md)**

---

## The Big Picture

Three layers, building on each other:

```
 Your code
    │
    ▼
 ┌─────────────────────────────────────────────────┐
 │  DOCKER — package the app (containers)          │
 │  "runs the same everywhere"                     │
 ├─────────────────────────────────────────────────┤
 │  KUBERNETES — run containers at scale           │
 │  "many machines, automatic"                     │
 ├─────────────────────────────────────────────────┤
 │  AWS — the cloud you run it all on              │
 └─────────────────────────────────────────────────┘
```

**The mental model:** Docker is *one* container. Kubernetes runs *many* containers across machines. AWS is the *infrastructure* underneath.

---

## 🐳 Docker — package the app

**Core terms**
- **Image** — frozen snapshot of your app + dependencies (like a recipe).
- **Container** — a running instance of an image (the meal).
- **Dockerfile** — text instructions that build an image.
- **Volume** — persistent storage that survives a container being deleted.
- **Bind mount** — map a folder on *your machine* into the container (dev use).
- **Port mapping** — connect a port on your machine to one inside the container (`-p 8080:80`).
- **Compose** — define + run multiple containers from one YAML file.

**Most-used commands**
```bash
docker build -t my-app .        # Build an image from a Dockerfile
docker run -p 8080:80 my-app    # Start a container, map port 8080→80
docker ps                       # List RUNNING containers
docker ps -a                    # List ALL containers (incl. stopped)
docker stop <id/name>           # Stop a container
docker rm <id/name>             # Remove a container
docker images                   # List images
docker rmi <image>              # Remove an image
docker logs <container>         # View logs
docker exec -it <container> sh # Open a shell inside a running container
docker compose up              # Start all services (Compose)
docker compose down            # Stop all services (Compose)
```

**Everyday flow**
```
write Dockerfile → docker build -t my-app . → docker run -p 8080:80 my-app → iterate
```

---

## ☸️ Kubernetes — run containers at scale

**Core terms**
- **Cluster** — group of machines (nodes): 1 control plane + workers.
- **Node** — a single machine in the cluster.
- **Control Plane** — the "brain": scheduling, state, API server.
- **Pod** — the smallest unit Kubernetes runs (one or more containers).
- **Deployment** — declares *how many copies* of a pod; handles updates, rollbacks, self-healing.
- **ReplicaSet** — made by a Deployment; ensures the right number of pods run.
- **Service** — a stable network entry point to a set of pods.
- **ConfigMap / Secret / Volume** — config (non-sensitive / sensitive) and storage.

**Most-used commands**
```bash
kubectl get nodes            # List cluster nodes
kubectl get pods             # List pods
kubectl get services         # List services
kubectl get deployments      # List deployments
kubectl apply -f file.yaml   # Create/update from a config file
kubectl delete -f file.yaml  # Delete resources defined in a file
kubectl logs <pod>           # View pod logs
kubectl logs -f <pod>        # Follow logs live
kubectl exec -it <pod> -- sh # Shell into a pod
kubectl describe pod <pod>   # Detailed info / debugging
kubectl scale deployment <name> --replicas=4   # Scale up/down
kubectl rollout status deployment/<name>       # Watch a rollout
kubectl rollout undo deployment/<name>         # Roll back

# Minikube (local cluster)
minikube start       # Start a local cluster
minikube stop        # Stop it
minikube dashboard   # Open the web dashboard
minikube service <svc>  # Open a service in the browser
minikube delete      # Tear it all down
```

**How they fit**
```
Deployment → manages ReplicaSet → runs Pods → exposed via Service
```

---

## ☁️ AWS — the cloud

**Core terms**
- **IAM** — who can do what (users, roles, policies). Billing is separate.
- **S3** — object storage (files, static websites). Files = *objects* in *buckets*.
- **EC2** — virtual servers in the cloud.
- **Lambda** — serverless: run code without managing a server (pay per run).
- **ECS / Fargate** — run Docker containers on AWS (Fargate = no servers to manage).
- **Elastic Beanstalk** — a quick "deploy your app without the server headache" wrapper.
- **CloudFront** — CDN, serves content fast worldwide.
- **RDS** — managed relational databases.

**CLI basics**
```bash
aws configure                 # Set access key, secret, region (once)
aws s3 ls                     # List buckets
aws s3 mb s3://my-bucket      # Create a bucket
aws s3 cp file.txt s3://my-bucket/   # Upload a file
aws s3 cp s3://my-bucket/file .      # Download
aws ec2 stop-instances --instance-ids <id>   # Stop an EC2 server
aws ec2 terminate-instances --instance-ids <id>  # Delete it
```

**S3 static website — the 5 steps (console)**
1. **Create bucket** (name = your domain, or any unique name)
2. **Objects → Upload** ← this is where your HTML files go (keep them at the bucket *root*)
3. **Properties → Static website hosting → Enable** (index document = `index.html`)
4. **Permissions → Bucket policy → Edit** → paste the JSON (replace bucket name)
5. **Permissions → Block public access → uncheck all four boxes**
Then test: open the **bucket website endpoint** in an incognito window.

**The bucket policy JSON** (paste into Permissions → Bucket policy, with *your* bucket name):
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
💡 **"where do I type this?"** — You only need **one** of two places: the **web console** (paste the JSON into the Permissions tab edit box) *or* the **command line** (Cloud Shell `>_` icon, or your local terminal with the AWS CLI installed). Never mix them mid-task.

---

## 🔍 Debugging cheat

| Symptom | Likely cause | Fix |
|---|---|---|
| Container exits immediately | No long-running process / wrong CMD | Check Dockerfile entrypoint |
| Can't reach app | Port mapping wrong | `-p host:container` check |
| S3 static site 403 | Public access blocked / no policy | uncheck Block public access + add policy |
| S3 empty page | Files nested in a subfolder | Move them to bucket root |
| `kubectl` can't connect | No cluster running | `minikube start` |
| Pod crash-loops | App error | `kubectl logs <pod>` |
| AWS "Access denied" on costs | IAM can't see billing | Root must enable IAM billing access |

> 📌 **Windows note:** commands like `cat > file << EOF` (heredocs) don't work in PowerShell/CMD. For CLI work on Windows, use Cloud Shell or save the JSON to a file first.

---

*Full lessons: `01-docker/`, `02-aws/`, `03-kubernetes/` · Terms: `glossary.md`*
