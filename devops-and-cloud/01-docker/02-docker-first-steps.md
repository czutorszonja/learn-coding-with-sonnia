# 02 — Docker First Steps: Running Containers

**← Back to [Lesson 1: What Is Docker and Why Does It Matter?](01-docker-intro.md)**


In lesson 01 we talked about what Docker *is*. Now let's actually use it.

By the end of this lesson, you'll have Docker running on your machine and you'll have started a few real containers.

---

## 1. Install Docker

Go to [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/) and download Docker Desktop for your operating system.

- **Mac:** Download the Mac version, drag the whale icon to Applications, open it
- **Windows:** Download the Windows installer, enable WSL 2 when prompted
- **Linux:** You'll use the command-line install — but odds are you already know that

Once installed, open a terminal and check:

```
docker --version
```

If you see something like `Docker version 27.x.x`, you're good.

**Stuck?** Search "install Docker Desktop [your OS]" — there are thousands of walkthroughs. The Docker docs are excellent too.

---

## 2. Hello, World (Docker Style)

Let's run our first container:

```
docker run hello-world
```

You'll see a message like:

```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

**What just happened:**

1. Docker looked for an image called `hello-world` on your machine
2. It wasn't there, so Docker downloaded it from Docker Hub (the public image library)
3. Docker created a container from that image and ran it
4. The container printed the message and exited

That's it. You just ran a container.

---

## 3. Running Real Software in Containers

Now let's do something useful. Run an actual web server:

```
docker run -d -p 8080:80 nginx
```

The flags:
- `-d` — run in the **background** (detached mode). You get your terminal back.
- `-p 8080:80` — **port mapping**. Container port 80 (where nginx serves web pages) is mapped to port 8080 on your machine.

Open your browser and go to [http://localhost:8080](http://localhost:8080). You'll see the Nginx welcome page.

```
             Your Machine                    Container
          ┌──────────────┐             ┌──────────────┐
          │  Port 8080   │────────────▶│  Port 80     │
          │  (browser)   │             │  (nginx)     │
          └──────────────┘             └──────────────┘
```

The `-p` flag connects a port on your machine to a port inside the container. Your browser talks to 8080, Docker forwards the traffic to nginx.

---

## 4. Port Mapping — How `-p` Really Works

The `-p` flag uses the format `host_port:container_port`:

```
-p 8080:80
  │     │
  │     └── Container port (what the app listens on inside)
  └── Host port (what you type in your browser)
```

- The **right side** is the port the application listens on (nginx listens on 80, Redis on 6379, PostgreSQL on 5432)
- The **left side** is the port you want to use on your own machine

You can pick any free port on your machine. If you wanted nginx on port 9090 instead:

```bash
docker run -d -p 9090:80 nginx
```

If you write only `-p 6379` (without the colon), Docker assigns a **random** port on your machine — useful sometimes, but usually you want to control it.

---

## 5. Managing Containers

Here are the commands you'll use constantly:

```bash
# List running containers
docker ps

# List ALL containers (including stopped ones)
docker ps -a

# Stop a container
docker stop <container-id or name>

# Start a stopped container
docker start <container-id or name>

# Remove a container
docker rm <container-id or name>

# Remove a container immediately (stop + remove)
docker rm -f <container-id or name>
```

Try it with your nginx container:

```bash
docker ps                # See it running
docker stop <id>         # Stop it
docker ps                # Gone from running list
docker ps -a             # Still exists but stopped
docker rm <id>           # Delete it completely
docker ps -a             # Now it's gone
```

**Important: `docker stop` does NOT free the container name.** If you stop a container named `my-redis`, that name is still taken. To reuse it, you need `docker rm` first, or use `docker rm -f` to stop and remove in one go.

---

## 6. Naming Containers

Docker assigns random names like `silly_babbage` or `pensive_curie`. You can name your own:

```bash
docker run -d -p 8080:80 --name my-website nginx
```

Now `docker stop my-website` and `docker start my-website` work with a real name you chose.

The `--name` flag goes **before** the image name. If you accidentally put a name where the image goes, Docker will try to pull it as an image and fail with "pull access denied".

---

## 7. Image Tags — What's the `:alpine` For?

You've seen `nginx`, `redis:alpine`, and `hello-world`. Image names can have a **tag** after a colon:

| Image name | What it is |
|---|---|
| `nginx` | Short for `nginx:latest` — the default, full-sized nginx |
| `nginx:alpine` | nginx built on Alpine Linux (much smaller) |
| `redis:alpine` | Redis on Alpine Linux (lightweight) |
| `python:3.12` | Python 3.12 with full OS |
| `python:3.12-slim` | Python 3.12 with a minimal OS (smaller download) |

The `:alpine` tag means the image is built on **Alpine Linux** — a tiny Linux distro (~5 MB) instead of a full OS. Most images offer an `alpine` variant that's 50-80% smaller. When no tag is given, Docker uses `:latest` by default.

---

## 8. Looking Inside a Running Container

`docker exec` runs a command **inside** a running container. You always need to give it a command to run:

```bash
# List files in the container's web root
docker exec my-nginx ls /usr/share/nginx/html/

# Start a shell inside the container (interactive)
docker exec -it my-nginx /bin/bash
```

`-it` means "interactive terminal" — it gives you a shell prompt inside the container. You can explore, check files, or install things:

```bash
root@abc123:/# ls
root@abc123:/# cat /usr/share/nginx/html/index.html
root@abc123:/# exit   # back to your machine
```

**Note:** `docker exec my-nginx` without a command will give you an error — it's asking "do what?" You always need to specify the command to run.

### Running a One-Liner Command

You can also run a single command without opening a full shell:

```bash
docker exec my-nginx sh -c "echo 'Hello!'"
```

This runs the command inside the container and returns the output. Breaking it down:
- `docker exec` — enter a running container
- `my-nginx` — which container
- `sh -c "..."` — run this shell command inside it (`sh` is the shell, `-c` says "here's a command")

**Why `sh -c` matters:** If you write `docker exec my-nginx echo 'Hello!' > file`, the `> file` part runs on **your** machine, not inside the container. Wrapping the whole thing in `sh -c` makes sure everything happens inside.

**⚠️ Windows / PowerShell users:** PowerShell intercepts the `>` character before Docker can see it. Always wrap your `sh -c` command in **double quotes**:

```powershell
# ✅ Correct — quotes keep '>' inside the container
docker exec my-nginx sh -c "echo 'Hello!' > /tmp/file"

# ❌ Wrong — PowerShell steals the '>' and tries to write to C:\tmp\file
docker exec my-nginx sh -c echo 'Hello!' > /tmp/file
```

Any changes you make inside a container are **lost when the container is removed** — containers start fresh from the image every time. That's why we have volumes (lesson 05) and Dockerfiles (lesson 03).

---

## 9. Viewing Logs

```bash
# See the logs of a container
docker logs my-nginx

# Follow logs in real time (like tail -f)
docker logs -f my-nginx

# See the last 50 lines
docker logs --tail 50 my-nginx
```

---

## 10. Images vs Containers — The Mental Model

| | Image | Container |
|---|---|---|
| **What it is** | A blueprint (frozen snapshot) | A running instance of that blueprint |
| **Analogy** | A cake recipe | A cake being eaten |
| **Can you modify it?** | No — you build a new one | Yes — but changes are temporary |
| **File size** | Large (GB) | Small (just runtime state) |
| **Lifecycle** | Persistent (stays on disk) | Ephemeral (dies when stopped) |

You can create many containers from the same image — just like you can bake many cakes from the same recipe.

---

## 🔨 Your Turn

1. Run an nginx container on port 9090 instead of 8080. Visit `http://localhost:9090`. Did it work?

2. Run `docker ps -a` and look at the container that ran `hello-world`. What status does it show?

3. Run a container named `my-redis` with `redis:alpine` in the background on port 6379.

4. Use `docker exec` to connect to your nginx container and change the welcome message in `/usr/share/nginx/html/index.html` using `echo "Hello from Sonnia!" > /usr/share/nginx/html/index.html`. Refresh the browser — what changed?

5. Remove the nginx container and run a new one using the same command as before. Is your custom message still there?

**Continue to [Lesson 3: Dockerfiles: Baking Your Own Images](03-dockerfiles.md)**
