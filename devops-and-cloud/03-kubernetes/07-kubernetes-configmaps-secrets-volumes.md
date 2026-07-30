# 07 — ConfigMaps, Secrets, and Storage

**← Back to [Lesson 6: Services: Making Your App Accessible](06-kubernetes-services.md)**

---

Your app needs configuration. A database URL. An API key. Files to serve.

In Docker, you used environment variables and bind mounts. In Kubernetes, you have three tools for this:

- **ConfigMap** — non-sensitive config (like database hostname)
- **Secret** — sensitive data (like passwords, API keys)
- **Volume** — persistent file storage

---

## 1. ConfigMap: Non-Sensitive Config

A ConfigMap stores configuration as key-value pairs. Your pods read them as environment variables or as files.

### Create a ConfigMap

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DB_HOST: postgres-service
  DB_NAME: myapp
  APP_PORT: "5000"
  CACHE_TTL: "300"
```

Apply it:

```bash
kubectl apply -f configmap.yaml
```

### Use it in a Pod

Inject the ConfigMap values as environment variables:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  containers:
  - name: app
    image: nginx:alpine
    envFrom:
    - configMapRef:
        name: app-config          # Load all values from this ConfigMap
```

Now inside the container:

```bash
echo $DB_HOST      # → postgres-service
echo $CACHE_TTL    # → 300
```

You can also load specific values:

```yaml
env:
- name: DATABASE_HOST
  valueFrom:
    configMapKeyRef:
      name: app-config
      key: DB_HOST
```

### View and manage ConfigMaps

```bash
kubectl get configmaps
kubectl describe configmap app-config
kubectl delete configmap app-config
```

> **Why not put config in the Docker image?** Because config changes between environments (dev, staging, production). A ConfigMap lets you use the same image everywhere and just swap the config.

---

## 2. Secret: Sensitive Data

Secrets work just like ConfigMaps, but the data is base64-encoded and handled more carefully by Kubernetes.

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  DB_PASSWORD: c3VwZXJzZWNyZXQ=    # base64 of "supersecret"
  API_KEY: YWJjMTIzNDU2           # base64 of "abc123456"
```

> **Note:** The values must be base64-encoded. Kubernetes handles decoding automatically when the pod reads them.

Apply the secret:

```bash
kubectl apply -f secret.yaml
```

### Use it in a Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  containers:
  - name: app
    image: nginx:alpine
    envFrom:
    - secretRef:
        name: app-secrets
```

Or mount a secret as a file:

```yaml
spec:
  containers:
  - name: app
    image: nginx:alpine
    volumeMounts:
    - name: secret-volume
      mountPath: /etc/secrets
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: app-secrets
```

Now the secret values appear as files:

```bash
kubectl exec my-app -- cat /etc/secrets/DB_PASSWORD
# → supersecret
```

### Encode a value

```bash
# macOS / Linux
echo -n "supersecret" | base64

# Windows PowerShell
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("supersecret"))
```

---

## 3. Volumes: Persistent Storage

Pods are ephemeral — when they restart, their filesystem resets to the image's default state. For data that needs to survive (databases, uploaded files, logs), you need a **Volume**.

### emptyDir — Temporary Storage (Lost When Pod Dies)

Useful for sharing files between containers in the same pod:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: shared-storage
spec:
  containers:
  - name: writer
    image: alpine
    command: ["sh", "-c", "echo Hello > /data/message && sleep 3600"]
    volumeMounts:
    - mountPath: /data
      name: shared
  - name: reader
    image: alpine
    command: ["sh", "-c", "cat /data/message && sleep 3600"]
    volumeMounts:
    - mountPath: /data
      name: shared
  volumes:
  - name: shared
    emptyDir: {}
```

The writer writes a file, the reader reads it. They share through `/data`. But when the pod dies, the data is gone.

### PersistentVolumeClaim (PVC) — Real Persistent Storage

For data that needs to survive pod restarts, Kubernetes has a two-part system:

1. **PersistentVolume (PV)** — actual storage (a disk, a cloud storage bucket, a local folder)
2. **PersistentVolumeClaim (PVC)** — a request for storage ("I need 5GB of fast storage")

On Minikube, PVs are created automatically when you claim them.

```yaml
# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-claim
spec:
  accessModes:
    - ReadWriteOnce       # One pod can read/write at a time
  resources:
    requests:
      storage: 1Gi         # Request 1GB of storage
```

```bash
kubectl apply -f pvc.yaml
kubectl get pvc
```

Now use it in a pod:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: db
spec:
  containers:
  - name: postgres
    image: postgres:16-alpine
    env:
    - name: POSTGRES_PASSWORD
      value: secret
    volumeMounts:
    - mountPath: /var/lib/postgresql/data
      name: db-storage
  volumes:
  - name: db-storage
    persistentVolumeClaim:
      claimName: data-claim
```

Now even if the pod is deleted and recreated, the database data survives.

---

## 4. Bringing It Together: Full Example

Here's what a real app config looks like:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-config
data:
  DB_HOST: postgres-service
  DB_NAME: notes
---
apiVersion: v1
kind: Secret
metadata:
  name: api-secrets
type: Opaque
data:
  DB_PASSWORD: c2VjcmV0       # base64 of "secret"
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-data
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 1Gi
---
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
        image: my-api:latest
        envFrom:
        - configMapRef:
            name: api-config
        - secretRef:
            name: api-secrets
```

---

## 🔨 Your Turn

1. Create a ConfigMap with your name and favourite programming language
2. Create a Pod that loads that ConfigMap and prints both values using `env From`
3. Create a Secret with a dummy API key, mount it as a file, and read it inside a Pod
4. Create a PVC, then start a Pod that writes a file to it. Delete the Pod. Create a new Pod that reads the same PVC — is your file still there?

**Continue to [Lesson 8: Kubernetes Project: Deploy the Note API](08-kubernetes-project.md)**
