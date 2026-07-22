# 03 — Dockerfiles: Baking Your Own Images

**← Back to [Lesson 2: Docker First Steps: Running Containers](02-docker-first-steps.md)**


We've run images that other people made (nginx, redis, hello-world). Now let's make our own.

A **Dockerfile** is a recipe that tells Docker how to build your image. You write it once, and anyone can build the exact same image on any machine.

---

## 1. Your First Dockerfile

Let's start simple: a Python script that prints something.

Create a file called `hello.py`:

```python
print("Hello from inside a Docker container!")
```

Now create a file called **`Dockerfile`** (no extension, capital D) in the same folder:

```dockerfile
# Use Python as the base image
FROM python:3.12-slim

# Copy our script into the container
COPY hello.py /app/hello.py

# Run it
CMD ["python", "/app/hello.py"]
```

Build and run:

```bash
docker build -t hello-app .
docker run hello-app
```

You should see: `Hello from inside a Docker container!`

**What each line means:**

| Instruction | What it does |
|---|---|
| `FROM` | Starting point. Using `python:3.12-slim` gives us Python + minimal OS. Everything builds on this. |
| `COPY` | Copies files from your machine into the image. |
| `CMD` | The command that runs when the container starts. |

---

## 2. The Docker Build Process

When you run `docker build -t hello-app .`, Docker:

1. Reads the Dockerfile
2. Starts from `python:3.12-slim` (downloads it if needed)
3. Runs each instruction as a **layer**
4. Each layer is cached — so rebuilds are fast

The `.` at the end is the **build context** — the folder Docker looks at for files to COPY. Docker sends this folder to the Docker daemon, so don't put gigabytes of junk in your build context.

```
        Dockerfile                    Layers                  Image
    ┌──────────────────┐     ┌─────────────────┐      ┌─────────────┐
    │ FROM python       │────▶│ Layer 1: Python  │      │             │
    │ COPY hello.py     │────▶│ Layer 2: hello.py│─────▶│  hello-app  │
    │ CMD python hello  │     │ Layer 3: CMD     │      │             │
    └──────────────────┘     └─────────────────┘      └─────────────┘
```

Each layer is cached. Change only `hello.py`? Only layer 2 and 3 rebuild — layer 1 stays cached. This is why you put things that change rarely (like installing packages) **before** things that change often (like copying your code).

---

## 3. A Real Python App in Docker

Let's build something real — a tiny Flask web server.

Create `app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Docker! 🐳"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Create `requirements.txt`:

```
flask==3.1.0
```

Now a Dockerfile that actually installs dependencies (like a real project):

```dockerfile
FROM python:3.12-slim

# Set working directory — all commands run relative to this
WORKDIR /app

# Copy requirements first (caching layer!)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY app.py .

# Tell Docker the container listens on port 5000
EXPOSE 5000

# Command to run when container starts
CMD ["python", "app.py"]
```

Build and run:

```bash
docker build -t flask-app .
docker run -d -p 5000:5000 --name my-flask flask-app
```

Visit `http://localhost:5000` in your browser. You should see your message!

---

## 4. The Copy Order Trick

Look at the Dockerfile above. Why did we copy `requirements.txt` separately, install dependencies, and *then* copy the app?

**Caching.**

If you write:

```dockerfile
COPY . /app          # Bad: copies everything at once
RUN pip install -r requirements.txt
```

Every time you change *any* file in your project, Docker re-runs `pip install` — even if `requirements.txt` didn't change. That's slow.

But if you split it:

```dockerfile
COPY requirements.txt .   # Only this file
RUN pip install ...       # Only rebuilds if requirements.txt changed
COPY . .                  # Copy everything else (fast layer rebuild)
```

Now changing your app code is instant — `pip install` is cached.

**Rule of thumb:** Copy the things that change rarely first, build on them, then copy things that change often.

---

## 5. The .dockerignore File

Just like `.gitignore` tells Git what to ignore, `.dockerignore` tells Docker what to ignore during builds.

Create `.dockerignore` in your project folder:

```
__pycache__
*.pyc
.env
.git
.DS_Store
*.log
```

This keeps your build context small and fast. Without it, Docker might send your entire `.git` folder (which could be hundreds of MB) to the build process for no reason.

---

## 6. Dockerfile Instructions Cheat Sheet

| Instruction | What it does | Example |
|---|---|---|
| `FROM` | Base image to start from | `FROM python:3.12-slim` |
| `WORKDIR` | Set working directory | `WORKDIR /app` |
| `COPY` | Copy files into the image | `COPY app.py .` |
| `RUN` | Run a command during build | `RUN pip install flask` |
| `EXPOSE` | Document which port the app uses | `EXPOSE 5000` |
| `CMD` | Default command when container starts | `CMD ["python", "app.py"]` |
| `ENV` | Set environment variable | `ENV FLASK_ENV=production` |

---

## 🚨 Common Mistakes

**1. Binding to the wrong host**
In Flask: `app.run(host='0.0.0.0')` — not `127.0.0.1` or `localhost`. Inside a container, `localhost` means the container itself, not your machine. `0.0.0.0` means "listen on all interfaces," which lets Docker forward traffic from outside.

**2. Forgetting `.dockerignore`**
Without it, pip install might be copying your venv, node_modules, or .git folder. Your builds will be slow and your images huge.

**3. Installing unnecessary packages**
Use `python:3.12-slim` instead of `python:3.12` unless you really need compiler tools. The slim version is 90% smaller.

**4. Running as root**
By default, containers run as root. For production, you should create a user:

```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

---

## 🔨 Your Turn

1. Modify the Flask app to return your name instead of "Hello from Docker!"
2. Rebuild and re-run (remember to stop the old container first with `docker rm -f my-flask`)
3. Add a second route — `@app.route('/about')` — that returns a short bio. Rebuild.
4. Check if the `pip install` step was cached (it should be, since you only changed `app.py`)
5. Try removing `0.0.0.0` from `app.run()` — just `app.run(port=5000)`. Rebuild and visit `localhost:5000`. What happens? Fix it and move on.

**Continue to [Lesson 4: Docker Compose: Running Multiple Services](04-docker-compose.md)**

> **Next up:** Lesson 04 — Docker Compose: running multiple containers together.
