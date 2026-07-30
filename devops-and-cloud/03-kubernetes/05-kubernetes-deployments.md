# 05 — Deployments: Running Apps at Scale

**← Back to [Lesson 4: Pods: The Smallest Unit](04-kubernetes-pods.md)**

---

Raw pods die when you delete them or when a node crashes. That's fine for experiments, but for a real app you need Kubernetes to **keep your app running automatically**.

Enter **Deployments**.

---

## 1. What Is a Deployment?

A Deployment tells Kubernetes: "I want N copies of this pod running at all times." Kubernetes then makes sure that's always true — even if pods crash, nodes fail, or you need to update the app.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 3                # I want 3 copies
  selector:
    matchLabels:
      app: api               # Which pods belong to this deployment?
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

Save this as `deployment.yaml` and apply it:

```bash
kubectl apply -f deployment.yaml
```

Now check what happened:

```bash
kubectl get deployments
kubectl get pods
```

You should see **3 pods** running, all created from the same template. The deployment is now responsible for keeping exactly 3 copies running.

---

## 2. How Deployments Work

A Deployment creates a **ReplicaSet**, which in turn creates the pods:

```
Deployment
    │  "I want 3 replicas"
    ▼
ReplicaSet
    │  "I manage the pods"
    ▼
Pod ─── Pod ─── Pod    (3 copies running)
```

This is called the **controller pattern** — a loop that constantly checks:

- Current state: "I see 2 pods running"
- Desired state: "The deployment says 3 pods"
- Action: "Start one more pod"

Check the chain:

```bash
kubectl get deployments
kubectl get replicasets
kubectl get pods
```

---

## 3. Self-Healing

The magic of Deployments: try killing a pod.

```bash
# Find one of your pods and delete it
kubectl get pods
kubectl delete pod api-deployment-xxxxx
```

Now quickly check:

```bash
kubectl get pods
```

Before you can even blink, a new pod has replaced the one you deleted. Kubernetes noticed the count dropped from 3 to 2 and started a new pod immediately.

```
YOU:            kubectl delete pod api-deployment-abc123
                │
KUBERNETES:     "Wait, I only see 2 pods. The deployment wants 3!"
                "Starting a new pod right now..."
                │
YOU (1 second later):  kubectl get pods
                       → 3 pods running (one is brand new)
```

This is **self-healing**. You don't need to write any scripts to restart containers. Kubernetes does it automatically.

---

## 4. Scaling

Need more copies? Change `replicas: 3` to `replicas: 5` and re-apply:

```yaml
spec:
  replicas: 5
```

```bash
kubectl apply -f deployment.yaml
kubectl get pods
```

Kubernetes will start 2 more pods to reach 5. Scale down:

```bash
# Edit the file back to 3 and apply, or use kubectl scale
kubectl scale deployment api-deployment --replicas=3
```

The extra pods get gracefully terminated.

---

## 5. Rolling Updates

This is where Deployments really shine. Imagine you've released a new version of your app. You want to update all pods without downtime.

Change the image in `deployment.yaml`:

```yaml
spec:
  template:
    spec:
      containers:
      - image: nginx:alpine   # current version
        # change to: nginx:1.27-alpine
```

Apply the change:

```bash
kubectl apply -f deployment.yaml
```

Now watch what happens:

```bash
kubectl rollout status deployment api-deployment
```

Kubernetes performs a **rolling update**:

1. Starts one new pod with the new image
2. Waits until it's healthy
3. Stops one old pod
4. Repeats until all pods are updated

```
Before:   [v1] [v1] [v1]
After:    [v2] [v2] [v2]

Rolling:  [v1] [v1] [v1]
          [v2] [v1] [v1]    ← one new pod starts
          [v2] [v2] [v1]    ← second new pod
          [v2] [v2] [v2]    ← all updated! zero downtime
```

If something goes wrong (the new version crashes), Kubernetes detects it and stops the rollout. You can also roll back:

```bash
# Undo the last rollout
kubectl rollout undo deployment api-deployment

# Check rollout history
kubectl rollout history deployment api-deployment
```

---

## 6. Key Deployment Commands

```bash
# Create or update a deployment
kubectl apply -f deployment.yaml

# List deployments
kubectl get deployments

# Get details
kubectl describe deployment api-deployment

# Scale on the fly (without editing the file)
kubectl scale deployment api-deployment --replicas=5

# Watch rollout progress
kubectl rollout status deployment api-deployment

# Roll back to previous version
kubectl rollout undo deployment api-deployment

# Delete the deployment (also deletes its pods!)
kubectl delete deployment api-deployment
```

---

## 7. Deployments vs Raw Pods — When to Use What

| | Raw Pod | Deployment |
|---|---|---|
| Self-healing | No | Yes |
| Scaling | Manual | Easy (`--replicas`) |
| Rolling updates | No | Built-in |
| Rollback | No | Built-in |
| When to use | Testing, experiments | Real apps |

**Rule of thumb:** If you're building something real, use a Deployment. Raw pods are for quick tests and debugging.

---

## 🔨 Your Turn

1. Create a `deployment.yaml` with `replicas: 5` running the `redis:7-alpine` image
2. Apply it and check that 5 pods appear
3. Delete one pod manually — watch it come back
4. Scale down to 2 pods with `kubectl scale`
5. Change the image to `redis:6-alpine` and apply — watch the rolling update with `kubectl rollout status`
6. Roll back to the previous version

**Continue to [Lesson 6: Services: Making Your App Accessible](06-kubernetes-services.md)**
