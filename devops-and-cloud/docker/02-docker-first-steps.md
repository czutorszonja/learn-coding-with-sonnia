# 02 — Docker First Steps: Running Containers

In lesson 01 we talked about what Docker *is*. Now let's actually use it.

By the end of this lesson, you'll have Docker running on your machine and you'll have started a few real containers. No imagination needed — all of this is copy-paste-and-run.

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

Let's break down what happened:

```
             Your Machine                    Container
          ┌──────────────┐             ┌──────────────┐
          │  Port 8080   │────────────▶│  Port 80     │
          │  (browser)   │             │  (nginx)     │
          └──────────────┘             └──────────────┘
```

The `-p` flag connects port 8080 on your machine to port 80 inside the container. Your browser talks to 8080, Docker forwards the traffic to nginx.

---

## 4. Managing Containers

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

---

## 5. Naming Containers

Docker assigns random names like `silly_babbage` or `pensive_curie`. You can name your own:

```bash
docker run -d -p 8080:80 --name my-website nginx
```

Now `docker stop my-website` and `docker start my-website` work with a real name.

---

## 6. Looking Inside a Running Container

Sometimes you need to peek inside a container to debug what's happening:

```bash
# Run nginx in the background
docker run -d -p 8080:80 --name my-nginx nginx

# See what processes are running inside
docker exec my-nginx ps aux

# Start a shell inside the container
docker exec -it my-nginx /bin/bash
```

`-it` means "interactive terminal" — it gives you a shell prompt *inside* the container. You can explore the filesystem, check logs, or install things.

```bash
# Inside the container, you can explore:
root@abc123:/# ls
root@abc123:/# cd /usr/share/nginx/html
root@abc123:/# cat index.html
root@abc123:/# exit   # back to your machine
```

Any changes you make inside a container are **lost when the container is removed**. That's why we have volumes (lesson 05) and Dockerfiles (lesson 03).

---

## 7. Viewing Logs

```bash
# See the logs of a container
docker logs my-nginx

# Follow logs in real time (like tail -f)
docker logs -f my-nginx

# See the last 50 lines
docker logs --tail 50 my-nginx
```

---

## 8. Images vs Containers — The Mental Model

At this point you've used both images and containers. Let's make the distinction crystal clear:

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
3. Run a container named `my-redis` with `redis:alpine` (a lightweight Redis image) in the background on port 6379.
4. Use `docker exec` to connect to your nginx container and change the welcome message in `/usr/share/nginx/html/index.html` using `echo "Hello from Sonnia!" > /usr/share/nginx/html/index.html`. Refresh the browser — what changed?
5. Remove the nginx container and run a new one. Is your custom message still there? (Spoiler: it won't be.)

> **Next up:** Lesson 03 — Dockerfiles: baking your own images.
