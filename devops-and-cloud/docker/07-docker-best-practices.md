# 07 — Docker Best Practices

**← Back to [Lesson 6: Docker Networking: Connecting Containers](06-docker-networking.md)**


By now you can build images, run containers, and connect services. This lesson covers how to do it **well** — practices that save time, reduce image size, and prevent security issues.

---

## 1. Choose the Right Base Image

Always prefer smaller base images when possible.

```dockerfile
# ❌ 1.1 GB — includes compiler tools, headers, documentation
FROM python:3.12

# ✅ 130 MB — just enough to run Python
FROM python:3.12-slim

# ⚡ 50 MB — even smaller, but might lack system libraries
FROM python:3.12-alpine
```

**When to use what:**
- **`-slim`** — default choice. Works for almost everything.
- **`-alpine`** — when image size matters a lot (but may need extra build dependencies).
- **Full image** — only when you need C extensions compiled during `pip install`.

The same logic applies to Node, Go, Rust — every language has slim variants.

---

## 2. Order Your Layers for Caching

Docker builds each instruction as a layer and **caches** them. If a layer hasn't changed, Docker reuses it. This makes rebuilds faster.

**Rule:** put things that change rarely at the top, things that change often at the bottom.

```dockerfile
# ✅ Optimised for caching
FROM python:3.12-slim

# 1. System dependencies (rarely change)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Python dependencies (change when requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Application code (changes constantly!)
COPY . .

CMD ["python", "app.py"]
```

Now if you only change your code, Docker rebuilds **only layer 3**. Layers 1 and 2 are cached. Rebuild time: seconds instead of minutes.

---

## 3. Always Use .dockerignore

Just like `.gitignore`, but for Docker builds. It prevents unnecessary files from being sent to the Docker daemon.

```gitignore
# .dockerignore
__pycache__
*.pyc
*.pyo
.env
.git
.gitignore
.vscode
node_modules
.DS_Store
*.log
dist
build
```

Without `.dockerignore`, Docker might send your entire project including `node_modules` (hundreds of MB) to the build context. Every single rebuild.

---

## 4. Use Multi-Stage Builds

Multi-stage builds let you use one image for **building** and a smaller one for **running**. This is huge for compiled languages, but useful for Python too.

```dockerfile
# Stage 1: Build
FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Run (starts fresh!)
FROM python:3.12-slim AS runtime

WORKDIR /app

# Copy only what we need from the builder stage
COPY --from=builder /root/.local /root/.local
COPY app.py .

ENV PATH=/root/.local/bin:$PATH

CMD ["python", "app.py"]
```

The final image contains only `app.py` and the installed packages. No build tools, no pip cache, no temporary files. **The builder stage is discarded.**

Real impact: a Python image with pandas can go from 900 MB to 400 MB.

---

## 5. Don't Run as Root

By default, Docker runs containers as **root**. This is dangerous — if someone breaks out of the container, they have root on your host.

```dockerfile
# ❌ Runs everything as root
FROM python:3.12-slim
COPY . /app
CMD ["python", "app.py"]

# ✅ Creates a non-root user
FROM python:3.12-slim

RUN groupadd -r appgroup && useradd -r -g appgroup -m -d /app appuser
WORKDIR /app

COPY --chown=appuser:appgroup requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=appuser:appgroup app.py .

USER appuser

CMD ["python", "app.py"]
```

The `USER` instruction switches to the non-root user for the running container. Any files the app creates are owned by `appuser`, not root.

---

## 6. Use Health Checks

A container can be "running" but actually broken (e.g., Flask crashed but Docker hasn't noticed yet). A **health check** tells Docker to actively monitor your app.

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1
```

In Docker Compose:

```yaml
services:
  api:
    build: ./backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
```

You also need an `/health` endpoint in your app:

```python
@app.route('/health')
def health():
    return {"status": "ok"}, 200
```

Docker shows health status in `docker ps` — `healthy`, `unhealthy`, or `starting`.

---

## 7. Environment Variables, Not Hardcoded Config

Never hardcode secrets or configuration in your code:

```python
# ❌ Bad: hardcoded
DB_PASSWORD = "supersecret123"

# ✅ Good: from environment
import os
DB_PASSWORD = os.getenv('DB_PASSWORD')
```

In Docker:

```bash
docker run -e DB_PASSWORD=supersecret123 my-image
```

In Compose:

```yaml
services:
  api:
    environment:
      DB_PASSWORD: ${DB_PASSWORD}
```

For secrets (passwords, API keys), use Docker secrets or a `.env` file that's never committed to Git.

---

## 8. Keep Images Small — Cheat Sheet

| Technique | Impact |
|---|---|
| Use slim/alpine base | 1 GB → 130 MB |
| Multi-stage build | Can halve image size |
| `.dockerignore` | Prevents build context bloat |
| `--no-cache-dir` in pip | Saves pip cache (~50 MB) |
| `apt-get clean` after install | Saves apt cache |
| Combine RUN commands | Reduces number of layers |

```dockerfile
# ✅ Combine apt commands to reduce layers
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean
```

Each `RUN` creates a layer. Combining related commands into one `RUN` block reduces layers and image size.

---

## 9. Development vs Production Dockerfile

You often need two Dockerfiles:

**Dockerfile.dev** — bind mounts, debug mode, more logging
**Dockerfile** (production) — multi-stage, no debug, USER appuser

Or use a single Dockerfile with build args:

```dockerfile
ARG DEBUG=false

RUN if [ "$DEBUG" = "true" ]; then \
    pip install debugpy; \
    fi
```

Build with: `docker build --build-arg DEBUG=true -t my-app .`

---

## 🔨 Your Turn

1. Look at the Dockerfile you created in lesson 03. How many layers does it have? (`docker history flask-app`)
2. Add a `.dockerignore` to the note-taking project. What files should it exclude?
3. Add a non-root user to the backend Dockerfile.
4. Add a health check endpoint to the Flask API and a healthcheck in docker-compose.yml.
5. Try building with `FROM python:3.12` instead of `python:3.12-slim`. Compare image sizes with `docker images`.

**Continue to [Lesson 8: Docker Project: Build a Real-World App](08-docker-project.md)**

> **Next up:** Lesson 08 — Docker Project: building a complete real-world app.
