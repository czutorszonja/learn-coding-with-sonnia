# 02 — Kubernetes Architecture: How a Cluster Works

**← Back to [Lesson 1: What Is Kubernetes and Why Does It Matter?](01-kubernetes-intro.md)**

---

Before you run commands, it helps to understand what you're talking to.

A Kubernetes cluster is a group of machines working together. Some are the **brain** (control plane), others are the **muscle** (worker nodes). Let's look at each piece.

---

## 1. The Two Parts of a Cluster

A Kubernetes cluster has two halves:

```
┌─────────────────────────────────────────────────────┐
│                  K8s Cluster                         │
│                                                      │
│  ┌────── Control Plane ──────────────────────────┐  │
│  │  API Server  │  Scheduler  │ Controller Mgr   │  │
│  │  etcd (the brain's memory)                     │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ┌────── Worker Node 1 ───┐  ┌── Worker Node 2 ──┐  │
│  │  Kubelet │ Pod │ Pod   │  │ Kubelet │ Pod     │  │
│  │  Pod │ Pod             │  │ Pod │ Pod │ Pod   │  │
│  └────────────────────────┘  └────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

| Part | What it does | Analogy |
|---|---|---|
| **Control Plane** | Makes decisions, schedules work, stores cluster state | The manager |
| **Worker Nodes** | Run your actual containers (pods) | The workers |

---

## 2. The Control Plane — The Brain

The control plane is a set of processes that keep the cluster running. In production, it runs on multiple machines for reliability. On your laptop (with Minikube), it all runs on one.

### API Server (`kube-apiserver`)

Everything talks to the API server. When you run `kubectl`, you're sending HTTP requests to the API server. It's the only component that directly talks to the data store.

```
kubectl get pods
     │
     ▼
  kubectl  ─────HTTPS────▶  API Server  ───▶  etcd
     │                          │
     │                     (validates request,
     │                      checks permissions)
     │
     ▼
  "Here are your pods"
```

### etcd — The Cluster's Memory

etcd is a database that stores the entire cluster state: what pods are running, what nodes exist, what config is set. It's the source of truth.

If etcd is corrupted, the cluster doesn't know what's running. That's why production clusters back it up.

### Scheduler (`kube-scheduler`)

When you say "I want 3 copies of my app," the scheduler decides **which node** each copy should run on. It looks at:

- Which nodes have free CPU/memory
- Which nodes are healthy
- Any special requirements (e.g. "this pod needs a GPU")

### Controller Manager

This runs controller processes — loops that watch the current state and work toward the desired state. For example:

- **Node controller:** notices when a node goes down
- **ReplicaSet controller:** notices when a pod crashes and starts a new one

---

## 3. Worker Nodes — The Muscle

Worker nodes are the machines that actually run your containers. Each worker runs:

### Kubelet

The kubelet is an agent that runs on every node. It talks to the API server and makes sure the containers it's told to run are actually running.

```
API Server: "Run pod 'api-abc123' on this node"
     │
     ▼
  Kubelet  ───▶  Docker/containerd  ───▶  Container starts
     │
     ▼
  Kubelet reports back: "Pod is running, healthy"
```

### Container Runtime

This is what actually runs the containers — Docker, containerd, or CRI-O. Kubernetes doesn't care which one, as long as it follows the Container Runtime Interface (CRI).

### kube-proxy

This handles networking. It makes sure traffic reaches the right pods, even as pods move between nodes. We'll cover this more in the Services lesson.

---

## 4. Pods — The Smallest Unit

A **pod** is the smallest thing Kubernetes runs. It's one or more containers that share:

- The same network (same IP address)
- The same storage volumes
- The same lifecycle (they start and stop together)

```
┌───────────────────────┐
│        Pod            │
│  ┌─────────────────┐  │
│  │  Container      │  │
│  │  (your app)     │  │
│  └─────────────────┘  │
│  IP: 10.1.0.5         │
│  Node: worker-2       │
└───────────────────────┘
```

Most of the time, a pod runs a single container. Sometimes you add helper containers (a logging sidecar, a proxy) that share the pod.

> **Why pods and not just containers?** Kubernetes needed something that could run multiple containers that need to share resources (like a web server and a helper that syncs files). A pod wraps them together.

---

## 5. kubectl — Your Remote Control

`kubectl` is the command-line tool you use to talk to your cluster. Every command follows the same pattern:

```
kubectl [action] [resource] [flags]
```

| Command | What it does |
|---|---|
| `kubectl get pods` | List all pods |
| `kubectl get nodes` | List all nodes in the cluster |
| `kubectl describe pod my-pod` | Show detailed info about a pod |
| `kubectl logs my-pod` | View logs from a pod |
| `kubectl apply -f file.yaml` | Create or update resources from a file |
| `kubectl delete pod my-pod` | Delete a pod |

Think of `kubectl` like `docker` but for a whole cluster.

---

## 6. Declarative vs Imperative — The K8s Way

This is the most important concept in Kubernetes:

- **Imperative:** "Do this now" — `docker run nginx` (step-by-step instructions)
- **Declarative:** "I want this state" — `kubectl apply -f deployment.yaml` (describe the end result)

Kubernetes is **declarative**. You write a YAML file that says "I want 3 copies of my app running on port 5000," and Kubernetes figures out how to make it happen and keeps it that way.

```yaml
# This is a desired state, not instructions
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3          # I want 3 copies
  template:
    spec:
      containers:
      - name: api
        image: my-api:latest
        ports:
        - containerPort: 5000
```

If a pod crashes, Kubernetes notices the current state (2 running) doesn't match the desired state (3 running) and starts a new one. No manual intervention needed.

---

## 🔨 Your Turn

1. Draw a simple diagram: a cluster with 2 worker nodes, each running 2 pods. Label the control plane and the worker nodes.
2. What would happen if the kubelet on a worker node crashed? (Hint: the control plane is still running.)
3. Explain in your own words: why does Kubernetes use pods instead of running containers directly?
4. Look at the declarative YAML example above — what does `replicas: 3` mean for the cluster?

**Continue to [Lesson 3: Your First Cluster with Minikube](03-kubernetes-minikube.md)**
