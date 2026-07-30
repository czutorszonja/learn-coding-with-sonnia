# 04 — Pods: The Smallest Unit

**← Back to [Lesson 3: Your First Cluster with Minikube](03-kubernetes-minikube.md)**

---

We ran `kubectl run hello-pod --image=nginx` in the last lesson. That created a **pod**. Let's understand what pods really are and how to work with them properly.

---

## 1. What Is a Pod?

A pod is the smallest thing Kubernetes manages. It's a wrapper around one or more containers.

```
┌───────────────────────────────────┐
│           Pod                     │
│  ┌───────────────────────────┐    │
│  │  Container (your app)     │    │
│  │  - runs your code         │    │
│  │  - has its own filesystem │    │
│  │  - listens on a port      │    │
│  └───────────────────────────┘    │
│  IP: 10.1.0.7                    │
│  Node: minikube                  │
│  Labels: app=hello               │
└───────────────────────────────────┘
```

Each pod gets:
- A **unique IP address** inside the cluster
- One or more containers (usually just one)
- Storage volumes (optional)
- Labels for organising and finding it

> **Key rule:** Pods are **ephemeral**. They die and get replaced all the time. Never treat a pod as permanent.

---

## 2. Writing a Pod YAML File

The `kubectl run` command creates pods, but real Kubernetes work is done with **YAML files**.

Create a file called `pod.yaml`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  labels:
    app: my-app
    tier: frontend
spec:
  containers:
  - name: nginx
    image: nginx:alpine
    ports:
    - containerPort: 80
```

Breakdown:

| Field | What it means |
|---|---|
| `apiVersion: v1` | Which version of the Kubernetes API to use |
| `kind: Pod` | What we're creating |
| `metadata.name` | The pod's name |
| `metadata.labels` | Tags we can search/filter by |
| `spec.containers` | Which containers to run inside this pod |
| `spec.containers[].image` | The Docker image to use |

Apply it:

```bash
kubectl apply -f pod.yaml
```

Now check:

```bash
kubectl get pods
kubectl describe pod my-app
```

---

## 3. Labels: How Kubernetes Organises Things

Labels are key-value pairs you attach to pods (and other resources). They're how Kubernetes finds and groups things.

```yaml
metadata:
  labels:
    app: my-app          # Which app does this belong to?
    tier: frontend       # frontend or backend?
    env: production      # production, staging, or dev?
```

You can filter by labels:

```bash
kubectl get pods -l app=my-app
kubectl get pods -l tier=frontend
kubectl get pods -l env=production
```

Later, when you create a **Service** or **Deployment**, it uses label selectors to find the right pods. This is how everything connects.

---

## 4. Multi-Container Pods

Most pods run one container. Sometimes you add a **sidecar** — a helper container that shares the pod:

```
┌───────────────────────────────────┐
│           Pod                     │
│  ┌──────────────────┐ ┌─────────┐ │
│  │ Main container   │ │ Sidecar  │ │
│  │ (web server)     │ │ (logs)  │ │
│  │ port 80          │ │ port     │ │
│  └──────────────────┘ └─────────┘ │
│  Shared: IP, volumes, network     │
└───────────────────────────────────┘
```

The sidecar can access the main container on `localhost` because they share the same network. Common sidecar patterns:

- **Log collector** — reads logs from the main app and ships them
- **Proxy** — handles authentication before forwarding to the main app
- **File sync** — watches for file changes and syncs them

---

## 5. Pod Lifecycle

A pod goes through stages:

```
Pending  →  Running  →  Succeeded / Failed / CrashLoopBackOff
```

| Status | What it means |
|---|---|
| **Pending** | Kubernetes is downloading the image or scheduling the pod |
| **Running** | The pod is running and healthy (for now) |
| **Succeeded** | The containers ran and exited normally (for batch jobs) |
| **Failed** | The containers exited with an error |
| **CrashLoopBackOff** | The container keeps crashing — Kubernetes keeps restarting it with increasing delays |

Check pod status:

```bash
kubectl get pods
kubectl describe pod my-app   # detailed info including events
```

---

## 6. Common Pod Operations

```bash
# List all pods
kubectl get pods

# Get more detail (including node and IP)
kubectl get pods -o wide

# Watch pods in real time
kubectl get pods -w

# View logs
kubectl logs my-app
kubectl logs -f my-app        # follow logs (like tail -f)

# Run a command inside the pod
kubectl exec my-app -- ls /app
kubectl exec -it my-app -- /bin/sh

# Delete a pod
kubectl delete pod my-app

# Delete a pod using the YAML file
kubectl delete -f pod.yaml
```

---

## 7. The Problem with Raw Pods

Try this: create a pod, then delete it.

```bash
kubectl apply -f pod.yaml
kubectl get pods
kubectl delete pod my-app
kubectl get pods    # gone!
```

The pod is gone forever. That's fine for testing, but for a real app you need Kubernetes to **keep your pods alive** — restart them if they crash, create new ones if a node fails.

That's what **Deployments** are for (next lesson).

---

## 🔨 Your Turn

1. Create a `pod.yaml` that runs the `redis:7-alpine` image (instead of nginx) on port 6379. Apply it.
2. Use `kubectl get pods -o wide` and note the IP address of your redis pod.
3. Check the logs: `kubectl logs my-redis`
4. Add a label `cache: redis` to your pod YAML, re-apply it, then filter with `kubectl get pods -l cache=redis`
5. Delete your pod and check it's gone

**Continue to [Lesson 5: Deployments: Running Apps at Scale](05-kubernetes-deployments.md)**
