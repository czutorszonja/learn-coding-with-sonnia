# 08 — Kubernetes Project: Deploy the Note API

**← Back to [Lesson 7: ConfigMaps, Secrets, and Storage](07-kubernetes-configmaps-secrets-volumes.md)**

---

Let's put everything together. We'll deploy the note-taking API on Kubernetes — the same app you ran with Docker Compose earlier.

## Project Structure

```
k8s-notes/
├── postgres-pvc.yaml
├── postgres-deployment.yaml
├── postgres-service.yaml
├── api-configmap.yaml
├── api-secret.yaml
├── api-deployment.yaml
├── api-service.yaml
└── redis-deployment.yaml
```

Make sure Minikube is running:

```bash
minikube start --driver=docker
```

---

## 1. Persistent Storage for PostgreSQL

PostgreSQL needs persistent storage so your notes survive pod restarts.

Create `postgres-pvc.yaml`:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-data
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

```bash
kubectl apply -f postgres-pvc.yaml
```

---

## 2. PostgreSQL: Deployment + Service

Create `postgres-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:16-alpine
        env:
        - name: POSTGRES_DB
          value: notes
        - name: POSTGRES_USER
          value: postgres
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: DB_PASSWORD
        ports:
        - containerPort: 5432
        volumeMounts:
        - mountPath: /var/lib/postgresql/data
          name: storage
      volumes:
      - name: storage
        persistentVolumeClaim:
          claimName: postgres-data
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
  type: ClusterIP
```

```bash
kubectl apply -f postgres-deployment.yaml
kubectl get pods -l app=postgres   # wait for Running
```

---

## 3. ConfigMap and Secret for the API

Create `api-configmap.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-config
data:
  DB_HOST: postgres-service
  DB_NAME: notes
  DB_USER: postgres
  REDIS_HOST: redis-service
```

Create `api-secret.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: api-secrets
type: Opaque
data:
  DB_PASSWORD: c2VjcmV0    # base64 of "secret"
```

```bash
kubectl apply -f api-configmap.yaml
kubectl apply -f api-secret.yaml
```

---

## 4. Redis: Deployment + Service

Create `redis-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
  type: ClusterIP
```

```bash
kubectl apply -f redis-deployment.yaml
kubectl get pods -l app=redis
```

---

## 5. The API: Deployment + Service

Create `api-deployment.yaml`:

> ⚠️ You need to build and push the Docker image from the note-app project first, or use a public image. For now, we'll use a placeholder — if you have the note-app project built, replace the image name below.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: note-app-api:latest          # Replace with your image
        ports:
        - containerPort: 5000
        envFrom:
        - configMapRef:
            name: api-config
        - secretRef:
            name: api-secrets
        env:
        - name: REDIS_HOST
          value: redis-service
---
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  selector:
    app: api
  ports:
  - port: 5000
    targetPort: 5000
  type: NodePort
```

> **💡 Building your image for Minikube:**
>
> ```bash
> # Point Docker to Minikube's Docker daemon
> eval $(minikube docker-env)    # macOS / Linux
> # or: minikube docker-env | InvokeExpression   # PowerShell
>
> # Build your image inside Minikube
> cd note-app
> docker build -t note-app-api:latest ./backend
>
> # Now apply the deployment
> kubectl apply -f api-deployment.yaml
> ```

```bash
kubectl apply -f api-deployment.yaml
kubectl get pods -l app=api
```

---

## 6. Check Everything

```bash
# See all resources
kubectl get pods
kubectl get deployments
kubectl get services
kubectl get pvc

# Check the logs
kubectl logs -l app=api
kubectl logs -l app=postgres
kubectl logs -l app=redis

# Open the API in your browser
minikube service api-service
```

Test the API:

```bash
# Get the URL
API_URL=$(minikube service api-service --url)

# Create a note
curl -X POST $API_URL/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Hello K8s","body":"This note is running on Kubernetes!"}'

# List notes
curl $API_URL/notes
```

---

## 7. Scale the API

```bash
# Increase to 5 replicas
kubectl scale deployment api --replicas=5
kubectl get pods -l app=api

# Watch a rolling update (if you had a new image)
kubectl rollout status deployment api
```

The Service automatically distributes traffic across all 5 pods.

---

## 8. Clean Up

```bash
# Delete everything (but keep the cluster)
kubectl delete -f api-deployment.yaml
kubectl delete -f redis-deployment.yaml
kubectl delete -f postgres-deployment.yaml
kubectl delete -f api-configmap.yaml
kubectl delete -f api-secret.yaml
kubectl delete -f postgres-pvc.yaml

# Or delete by resource type:
kubectl delete deployments --all
kubectl delete services --all
kubectl delete pods --all
kubectl delete pvc --all

# Stop Minikube
minikube stop
```

---

## What You Built

```
┌─────────────────────────────────────────────────┐
│              Minikube Cluster                     │
│                                                   │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ PostgreSQL│  │  Redis   │  │   API × 3    │  │
│  │ Pod       │  │  Pod     │  │  ┌─────────┐ │  │
│  │ Port 5432 │  │  Port    │  │  │ Pod     │ │  │
│  │           │  │  6379    │  │  │ Pod     │ │  │
│  │ 1GB PVC   │  │          │  │  │ Pod     │ │  │
│  └─────┬─────┘  └────┬────┘  │  └────┬────┘ │  │
│        │              │       │       │       │  │
│  ┌─────▼──────────────▼──────────────▼──────┐ │  │
│  │        Services (stable names)           │ │  │
│  │  postgres-service  redis-service        │ │  │
│  │  api-service (:5000 → NodePort)         │ │  │
│  └──────────────────────────────────────────┘ │  │
└──────────────────────────────────────────────────┘
```

Your note-taking API is running on Kubernetes — three replicas, auto-healing, with a database backed by persistent storage and Redis for caching.

---

## 🔨 Your Turn

1. Deploy all the YAML files above on your Minikube cluster
2. Create a note and verify it appears
3. Delete the API pod — watch it get recreated by the Deployment
4. Scale the API to 5 replicas — does the Service still route correctly?
5. Delete the PostgreSQL pod — is the data still there when it comes back?
6. Destroy everything with `kubectl delete deployments --all`

**Continue to the [Glossary](../glossary.md) for a full reference of every term we've covered.**
