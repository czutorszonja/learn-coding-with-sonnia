# 03 — Your First Cluster with Minikube

**← Back to [Lesson 2: Kubernetes Architecture: How a Cluster Works](02-kubernetes-architecture.md)**

---

We've talked about what Kubernetes is and how it works. Now let's actually run it.

For learning, you don't need a cloud account or multiple servers. You'll run a **single-node cluster** on your own machine using **Minikube**.

---

## 1. Install Minikube

Minikube runs a lightweight Kubernetes cluster in a VM or container on your computer.

Go to [minikube.sigs.k8s.io/docs/start](https://minikube.sigs.k8s.io/docs/start/) and download the version for your OS:

- **Windows:** Download the installer (`.exe`) — Minikube works with Docker Desktop
- **Mac:** Download the `.pkg` or use Homebrew: `brew install minikube`
- **Linux:** Download the binary or use your package manager

You also need **kubectl**, the command-line tool for Kubernetes:

```bash
# Windows (PowerShell) — download the binary:
# curl.exe -LO "https://dl.k8s.io/release/v1.32.0/bin/windows/amd64/kubectl.exe"

# Mac:
brew install kubectl

# Linux:
curl -LO "https://dl.k8s.io/release/v1.32.0/bin/linux/amd64/kubectl"
chmod +x kubectl && sudo mv kubectl /usr/local/bin/
```

> 💡 **Already have Docker Desktop?** Docker Desktop includes an option to enable Kubernetes in its settings, but we'll use Minikube instead — it's more explicit about what's happening and works the same on all platforms.

---

## 2. Start Your Cluster

Make sure Docker Desktop is running first. Then:

```bash
minikube start --driver=docker
```

This tells Minikube to use Docker as its driver (creates a container that acts as your node). The first time takes a minute to download images.

You'll see output like:

```
😄  minikube v1.34.0 on Darwin 14.5
✨  Using the docker driver based on user configuration
👍  Starting control plane node minikube in cluster minikube
🏃  Updating the running docker "minikube" container ...
🐳  Preparing Kubernetes v1.32.0 on Docker 27.4.1 ...
🔎  Verifying Kubernetes components...
🏄  Done! kubectl is now configured to use "minikube" cluster
```

**You now have a running Kubernetes cluster.** 🎉

Check it:

```bash
kubectl get nodes
```

```
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   30s   v1.32.0
```

That's your cluster — one node that acts as both control plane and worker. In production these are separate, but for learning this is all you need.

---

## 3. Your First kubectl Commands

Let's explore the cluster:

```bash
# See what the cluster knows about
kubectl get nodes           # List all nodes (just minikube for now)
kubectl get pods            # List all pods (none yet)
kubectl get services        # List all services (there's one: kubernetes)
kubectl get deployments     # List all deployments (none yet)
```

The output `kubectl get services` shows a default service called `kubernetes` — that's the API server itself. Every cluster has this.

---

## 4. Run Your First Pod

Let's run something:

```bash
kubectl run hello-pod --image=nginx --port=80
```

This tells Kubernetes: "Create a pod named `hello-pod` using the `nginx` image, and expose port 80."

Check if it's running:

```bash
kubectl get pods
```

```
NAME        READY   STATUS    RESTARTS   AGE
hello-pod   1/1     Running   0          10s
```

The pod is running inside your Minikube cluster. But you can't access it from your browser yet — we haven't exposed it. We'll cover that in the Services lesson.

---

## 5. Peek Inside Your Pod

```bash
# See details about the pod
kubectl describe pod hello-pod

# View logs
kubectl logs hello-pod

# Run a command inside the pod
kubectl exec hello-pod -- ls /usr/share/nginx/html

# Get an interactive shell inside the pod
kubectl exec -it hello-pod -- /bin/bash
```

> 💡 This is `kubectl exec` — like `docker exec` but for a pod in a cluster. Same idea, bigger scale.

---

## 6. Delete Your Pod

```bash
kubectl delete pod hello-pod
```

Now `kubectl get pods` shows nothing. The pod is gone.

If you recreate it, it gets a new name and a new IP. That's important — pods are ephemeral. If you want something persistent, you use a **Deployment** (next lesson).

---

## 7. The Minikube Dashboard

Minikube comes with a web dashboard:

```bash
minikube dashboard
```

This opens a browser showing your cluster — pods, deployments, services, all visual. It's great for seeing what's happening without memorising every kubectl command.

---

## 8. Useful Minikube Commands

```bash
# Stop the cluster (preserves your VMs/images)
minikube stop

# Start it again later
minikube start

# Delete the entire cluster (start fresh)
minikube delete

# SSH into the Minikube VM (if you need to explore)
minikube ssh

# See the cluster's IP address
minikube ip
```

---

## 9. What We Built

```
┌─────────────────────────────────────────────────┐
│              Your Machine                        │
│                                                  │
│  ┌────────── Minikube VM/Container ───────────┐  │
│  │                                              │  │
│  │  ┌────── Control Plane ─────────────────────┐│  │
│  │  │  API Server  │  Scheduler  │  etcd       ││  │
│  │  └──────────────────────────────────────────-┘│  │
│  │                                              │  │
│  │  ┌────── Worker (same node) ────────────────┐│  │
│  │  │  hello-pod (nginx)                       ││  │
│  │  └──────────────────────────────────────────┘│  │
│  └──────────────────────────────────────────────┘  │
│                                                    │
│  kubectl  ──────────►  API Server                   │
└────────────────────────────────────────────────────┘
```

You have a working Kubernetes cluster on your machine. Everything from here builds on this.

---

## 🔨 Your Turn

1. Start Minikube (`minikube start --driver=docker`) if you haven't already
2. Run `kubectl get nodes` — what status do you see?
3. Create a pod running the `redis:7-alpine` image instead of nginx:
   ```
   kubectl run my-redis --image=redis:7-alpine
   ```
4. Use `kubectl logs my-redis` — what do you see?
5. Delete both pods
6. Run `minikube dashboard` and explore your cluster in the browser — how many pods do you see running?

**Continue to [Lesson 4: Pods: The Smallest Unit](04-kubernetes-pods.md)**
