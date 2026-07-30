# 06 — Services: Making Your App Accessible

**← Back to [Lesson 5: Deployments: Running Apps at Scale](05-kubernetes-deployments.md)**

---

Your deployment is running 3 copies of your app. But how do you actually reach them?

Each pod has its own IP address, but pods come and go — IPs change constantly. You need a **stable address** that always points to whichever pods are running right now.

That's what a **Service** does.

---

## 1. The Problem: Pods Are Temporary

When a pod is replaced (by a rolling update, a crash, or a node failure), it gets a new IP:

```
Deployment creates Pod A  →  IP: 10.1.0.5
Pod A crashes             →  IP: 10.1.0.5 (gone)
Deployment creates Pod B  →  IP: 10.1.0.9 (different!)
```

If your database or frontend was pointing to `10.1.0.5`, it breaks. A Service solves this by providing a **stable IP and DNS name** that follows the pods wherever they go.

---

## 2. What a Service Does

A Service is a stable endpoint that sits in front of your pods and routes traffic to them:

```
                    ┌──────────────────────────┐
                    │       Service             │
                    │  Name: api-service        │
                    │  IP:   10.100.200.5       │
                    │  Port: 80                 │
                    └──────────┬───────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
    ┌──────────┐         ┌──────────┐         ┌──────────┐
    │ Pod A    │         │ Pod B    │         │ Pod C    │
    │ 10.1.0.5 │         │ 10.1.0.9 │         │ 10.1.0.3│
    │ app v2   │         │ app v2   │         │ app v2   │
    └──────────┘         └──────────┘         └──────────┘
            All pods match label: app: api
```

The Service uses **labels** to find the right pods — the same labels you set on your Deployment.

---

## 3. Creating a Service

Create a file called `service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  selector:
    app: api                  # Route traffic to pods with this label
  ports:
  - protocol: TCP
    port: 80                  # Port the service listens on
    targetPort: 80            # Port the pods are listening on
  type: ClusterIP             # Default — only reachable inside the cluster
```

Apply it:

```bash
kubectl apply -f service.yaml
```

Check it:

```bash
kubectl get services
```

```
NAME          TYPE        CLUSTER-IP      PORT(S)   AGE
api-service   ClusterIP   10.100.200.5    80/TCP    10s
kubernetes    ClusterIP   10.96.0.1       443/TCP   1h
```

You now have a stable IP (`10.100.200.5`) inside the cluster that routes to your pods. Any pod in the cluster can reach your app at `http://api-service:80`.

---

## 4. Service Types

There are 3 types of Services you'll use:

### ClusterIP (default)

Creates a virtual IP inside the cluster. Only reachable from other pods.

```yaml
type: ClusterIP
```

Used for: backend services, databases, internal APIs.

### NodePort

Opens a port on every node in the cluster, so you can reach it from outside.

```yaml
type: NodePort
```

```
Browser ───► http://localhost:30007 ───► api-service ───► Pods
```

```bash
kubectl apply -f service.yaml  # with type: NodePort
kubectl get services
```

Output:

```
NAME          TYPE        CLUSTER-IP      PORT(S)          AGE
api-service   NodePort    10.100.200.5    80:30007/TCP     10s
```

You can now visit `http://localhost:30007` in your browser. On Minikube, use:

```bash
minikube service api-service
```

This opens the service in your browser automatically.

### LoadBalancer

Creates an external load balancer (works with cloud providers like AWS, GCP, Azure).

```yaml
type: LoadBalancer
```

On Minikube, this behaves like NodePort. In the cloud, it provisions a real load balancer with a public IP.

---

## 5. How Services Find Pods

A Service uses a **label selector** to know which pods to route to:

```yaml
selector:
  app: api
```

This matches any pod with the label `app: api`. The Service watches for pods that match and automatically adds/removes them as they come and go.

```
New pod starts with label app: api
    │
    ▼
Service detects it ───► adds to the routing table
    │
    ▼
Traffic now goes to the new pod too

Pod is deleted
    │
    ▼
Service detects it ───► removes from routing table
    │
    ▼
Traffic stops going to the deleted pod
```

No configuration changes needed. The Service adapts automatically.

---

## 6. DNS Inside the Cluster

Kubernetes has built-in DNS. Any service you create gets a DNS name matching its name:

```
Service name: api-service
Namespace:    default

DNS name:     api-service.default.svc.cluster.local
Short name:   api-service (works from the same namespace)
```

So another pod in your cluster can reach your app with:

```bash
curl http://api-service:80
```

No IP addresses needed — just like Docker Compose, but cluster-wide.

---

## 7. Connecting Your Deployment to a Service

Here's the full picture — a Deployment creates pods, a Service routes to them:

```yaml
# deployment.yaml
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
        app: api          # ← This label matches the Service selector!
    spec:
      containers:
      - name: api
        image: nginx:alpine
        ports:
        - containerPort: 80
---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  selector:
    app: api              # ← Matches the pods' labels
  ports:
  - port: 80
    targetPort: 80
  type: NodePort
```

Apply both:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get pods,services
```

---

## 8. Service Commands

```bash
# List services
kubectl get services

# Get details
kubectl describe service api-service

# Delete a service
kubectl delete service api-service

# Delete using the YAML file
kubectl delete -f service.yaml

# Open a service in the browser (Minikube)
minikube service api-service

# Get the URL for a service (Minikube)
minikube service api-service --url
```

---

## 🔨 Your Turn

1. Create a Deployment with 3 replicas running `nginx:alpine` (label: `app: web`)
2. Create a Service of type `NodePort` that routes to `app: web` on port 80
3. Run `kubectl get services` — what port was assigned on the node?
4. Open the service in your browser with `minikube service <name>`
5. Scale the deployment to 5 replicas — does the service automatically include the new pods?
6. Delete one of the pods — does traffic still reach the remaining ones?

**Continue to [Lesson 7: ConfigMaps, Secrets, and Storage](07-kubernetes-configmaps-secrets-volumes.md)**
