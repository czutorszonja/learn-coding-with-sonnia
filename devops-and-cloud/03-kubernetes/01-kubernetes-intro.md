# 01 — What Is Kubernetes and Why Does It Matter?

**← Back to [AWS Project: Build and Deploy a Serverless App](../02-aws/07-aws-project.md)**

---

So you've learned Docker. You can package your app into a container and run it with Docker Compose. That's great for your laptop.

But what happens when you need to run **100 containers** across **10 different machines**? What happens when one of those machines crashes? What if you need to roll out a new version without downtime?

That's where Kubernetes comes in.

---

## 1. The Problem Kubernetes Solves

Docker Compose is perfect for a single machine. You define your services, run `docker compose up`, and everything works.

But in the real world:

- **One machine isn't enough.** Your app gets popular. One server can't handle the traffic.
- **Servers fail.** Hard drives die. Networks go down. You need your app to survive.
- **You need zero-downtime updates.** You can't take your app offline every time you deploy.
- **You need to scale up and down.** More traffic at lunchtime? Spin up more copies. Quiet at 3am? Scale back down.

Kubernetes (often written as **K8s** — "K" + 8 letters + "s") solves all of this.

> **Kubernetes = a platform for running containers across multiple machines, automatically**

```
         ┌───────────────────────────────────────────┐
         │         Kubernetes Cluster                 │
         │                                           │
         │  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
         │  │ Machine 1│  │ Machine 2│  │ Machine 3│ │
         │  │ ┌──────┐ │  │ ┌──────┐ │  │ ┌──────┐ │ │
         │  │ │ App  │ │  │ │ App  │ │  │ │ App  │ │ │
         │  │ │ v2   │ │  │ │ v2   │ │  │ │ v1   │ │ │
         │  │ └──────┘ │  │ └──────┘ │  │ └──────┘ │ │
         │  │ ┌──────┐ │  │ ┌──────┐ │  │ ┌──────┐ │ │
         │  │ │ DB   │ │  │ │ Redis│ │  │ │      │ │ │
         │  │ └──────┘ │  │ └──────┘ │  │ └──────┘ │ │
         │  └──────────┘  └──────────┘  └──────────┘ │
         └───────────────────────────────────────────┘
                 Everything is managed automatically
```

---

## 2. Docker vs Kubernetes — What's What?

The confusion is common. Here's the simplest way to think about it:

| | Docker (Compose) | Kubernetes |
|---|---|---|
| **Runs on** | One machine | Many machines (a cluster) |
| **Scaling** | Manual (`--scale`) | Automatic |
| **Self-healing** | No — if a container crashes, it stays down | Yes — restarts failed containers automatically |
| **Rolling updates** | Manual | Automatic — updates one by one |
| **Load balancing** | Basic (port mapping) | Built-in service discovery and load balancing |
| **Complexity** | Simple, friendly | More complex, more powerful |

**You don't need to choose.** In fact, most people use both:
- **Docker** to build and package your app into an image
- **Kubernetes** to run and manage that image across machines

Kubernetes actually uses Docker (or other container runtimes) under the hood to run your containers.

---

## 3. What Kinds of Problems Does K8s Solve?

### Problem 1: "My server crashed at 3am"

Without K8s: you wake up to angry users. You SSH in, figure out what happened, restart everything.

With K8s: Kubernetes detects the failure and automatically restarts your containers on a healthy machine. You sleep through it.

### Problem 2: "Our app is getting too much traffic"

Without K8s: you manually provision new servers, install everything, add them to your load balancer.

With K8s: you run `kubectl scale deployment my-app --replicas=10`. In seconds, you have 10 copies running across your cluster.

### Problem 3: "The deployment broke everything"

Without K8s: you push the new version, users hit errors, you scramble to roll back.

With K8s: you use a **rolling update** — new containers start one by one. If something breaks, Kubernetes automatically stops and rolls back.

---

## 4. Kubernetes in the Real World

Kubernetes runs everywhere:

- **Google, Spotify, Airbnb, Uber** — all use K8s internally
- **GitHub Actions, GitLab CI** — K8s powers their build runners
- **Pokémon GO** — K8s handled the massive launch traffic
- **Your future project** — K8s is the industry standard for running containers

You can run Kubernetes:
- **Locally** with Minikube or Kind (for learning and development)
- **In the cloud** with EKS (AWS), GKE (Google), or AKS (Azure)
- **On your own servers** with kubeadm or MicroK8s

This course uses **Minikube** to run a single-node cluster on your machine — the simplest way to learn.

---

## 5. Key Vocabulary

Before diving in, here are the terms you'll see in every lesson:

| Term | What it is | Analogy |
|---|---|---|
| **Cluster** | A group of machines running Kubernetes | A data centre |
| **Node** | A single machine in the cluster (physical or virtual) | A server rack |
| **Pod** | The smallest thing K8s runs — one or more containers | A single app instance |
| **Deployment** | Describes how many copies of a pod should run | "I want 3 copies" |
| **Service** | Provides a stable address to reach your pods | A receptionist |
| **kubectl** | The command-line tool to talk to your cluster | The remote control |
| **Control Plane** | The brain of Kubernetes that makes all decisions | The manager |

---

## 🔨 Your Turn

1. In your own words, what's the difference between Docker Compose and Kubernetes?
2. If your app is a single Python script that runs on your laptop, do you need Kubernetes? Why or why not?
3. What do you think happens when a node in a Kubernetes cluster crashes — does the app go down too? (Answer will come in later lessons!)
4. Install **Docker Desktop** if you haven't already — Minikube (our next lesson) works best with it on Windows and Mac.

**Continue to [Lesson 2: Kubernetes Architecture: How a Cluster Works](02-kubernetes-architecture.md)**
