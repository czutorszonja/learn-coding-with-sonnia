# 06 — Docker Networking: Connecting Containers

So far, our Flask API talks to PostgreSQL using the hostname `db`. But how?

When you use Docker Compose, it creates a **network** automatically and registers each service name as a hostname. Containers can reach each other by name without knowing IP addresses.

This lesson explains how that works — and how to set it up manually.

---

## 1. The Default: Container-to-Container Isolation

By default, containers can't see each other. Each one gets its own network namespace with its own localhost.

```
Container A                    Container B
┌──────────────┐               ┌──────────────┐
│ localhost    │     NO ❌     │ localhost    │
│ (A's loopback)│──────────────│ (B's loopback)│
└──────────────┘               └──────────────┘
```

If your Flask app tries to connect to `localhost:5432` (PostgreSQL), it finds... nothing. Because `localhost` inside the Flask container is the container itself, not the host machine and not the PostgreSQL container.

---

## 2. Docker Networks

Docker provides **networks** to connect containers. When containers are on the same network, they can communicate.

```bash
# Create a network
docker network create my-app-net

# Run PostgreSQL on the network
docker run -d \
  --name my-db \
  --network my-app-net \
  -e POSTGRES_PASSWORD=secret \
  postgres:16

# Run the API on the same network
docker run -d \
  --name my-api \
  --network my-app-net \
  -p 5000:5000 \
  -e DB_HOST=my-db \
  my-api-image
```

Now `my-api` can reach `my-db:5432` (hostname:port). Docker's built-in DNS resolves `my-db` to the PostgreSQL container's IP address on this network.

```
                    my-app-net
    ┌──────────────────────────────────┐
    │                                  │
    │  my-db (postgres)   my-api       │
    │  ┌──────────────┐  ┌──────────┐ │
    │  │ postgres     │  │ Flask    │ │
    │  │ port 5432    │◀─│ pings    │ │
    │  └──────────────┘  │ "my-db"  │ │
    │                    └──────────┘ │
    └──────────────────────────────────┘
```

---

## 3. Port Mapping: The Outside World

When you want to access a container from your browser or from outside Docker, you need **port mapping** (`-p` flag).

```bash
docker run -d -p 8080:80 nginx
```

This creates a mapping:

```
Your Machine (port 8080)  ←→  Container (port 80)
```

Traffic to your machine's port 8080 is forwarded to the container's port 80. Without this, nothing outside Docker can reach the container.

---

## 4. Communication Flows (Important!)

Draw this out:

```
Your Browser
     │
     ▼  http://localhost:5000
┌──────────────────────────────────┐
│  Your Machine                    │
│  ┌────────────────────────────┐  │
│  │ Docker Network             │  │
│  │                           │  │
│  │  api (port 5000)          │  │
│  │    │                      │  │
│  │    │ DB_HOST=db           │  │
│  │    ▼                      │  │
│  │  db (port 5432)           │  │
│  └────────────────────────────┘  │
└──────────────────────────────────┘
```

Three kinds of communication:
1. **Browser → API:** Uses port mapping (`-p 5000:5000`). Goes through your machine's port to the container.
2. **API → Database:** Uses Docker DNS (`DB_HOST=db`). Stays inside the Docker network.
3. **Database → nowhere:** PostgreSQL doesn't initiate connections. It just listens.

---

## 5. Network Drivers

Docker provides different network drivers for different needs:

| Driver | Use case | Isolation |
|---|---|---|
| `bridge` (default) | Containers on same host | Good — each bridge is isolated |
| `host` | No network isolation, uses host's network | None — container uses your machine's IP |
| `none` | Completely isolated container | Maximum |
| `overlay` | Containers across multiple machines (Swarm) | Varies |

For local development, `bridge` is almost always what you want. Docker Compose creates a bridge network automatically for each project.

---

## 6. Inside a Compose Network

When you run `docker compose up`, Docker:

1. Creates a new bridge network (named `projectname_default`)
2. Adds each service to that network
3. Registers each service name as a DNS entry
4. Starts containers

You can see the network:

```bash
docker network ls
# → NETWORK ID   NAME                    DRIVER
# → abc123       note-app_default        bridge

# Inspect it
docker network inspect note-app_default
# Shows all containers on this network and their IPs
```

---

## 7. Hostnames and Ports Inside Docker

**Critical distinction:**

```
DB_HOST=db            # ← hostname (resolves to container IP)
DB_PORT=5432          # ← port inside the container
```

When the API connects to `db:5432`, both the hostname and port are **inside the Docker network**. The database's port 5432 is exposed to other containers on the same network.

When you connect from your machine: `localhost:5432` only works if you used `-p 5432:5432` (port mapping). Otherwise, port 5432 is only visible inside the Docker network.

**Common mistake:** Setting `DB_HOST=localhost` in Docker. `localhost` inside a container means the container itself, not the host. Always use the service name (Compose) or container name (manual networking).

---

## 8. Communication Diagram for the Note App

```
                   Internet (your browser)
                        │
                   http://localhost:5000
                        │
                    ┌───▼──────┐
                    │  Port    │
                    │  5000    │  ← port mapping
                    └───┬──────┘
                        │
               Docker Network (note-app_default)
                        │
              ┌─────────┼──────────┐
              │         │          │
          ┌───▼───┐ ┌──▼──┐  ┌───▼───┐
          │ API   │ │ DB  │  │ Redis │
          │:5000  │ │:5432│  │:6379  │
          └───────┘ └─────┘  └───────┘
```

The API connects to `db:5432` and `redis:6379` using Docker's internal DNS. Your browser connects to `localhost:5000` through the port mapping.

---

## 🔨 Your Turn

1. Create a Docker network called `test-net`. Run an nginx container and an alpine container on this network.
2. From the alpine container, run `ping nginx` (install ping with `apk add iputils`). Does it resolve?
3. Without the `-p` flag on the nginx container, can you access the nginx welcome page from your browser? Why or why not?
4. In the note-taking Compose project, check what network Compose created with `docker network ls`.
5. Try running `docker compose exec api ping db` inside the running project. Does it connect?

> **Next up:** Lesson 07 — Docker Best Practices.
