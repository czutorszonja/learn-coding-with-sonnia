# 05 — Volumes: Keeping Data Alive When Containers Die

**← Back to [Lesson 4: Docker Compose: Running Multiple Services](04-docker-compose.md)**


There's a hard rule in Docker: **when a container is removed, everything inside it is gone forever.**

This is by design — containers are meant to be disposable. Need a newer version of your app? Remove the old container, start a new one. It's clean, reliable, and predictable.

But there's a problem: your **PostgreSQL database** lives inside a container. If you remove the container, you lose all your data. That's unacceptable.

**Volumes solve this.** They let data outlive containers.

---

## 1. The Problem

Run this:

```bash
docker run -d --name test-db -e POSTGRES_PASSWORD=secret postgres:16

# Connect and create a table
docker exec -it test-db psql -U postgres -c "CREATE TABLE cats (name TEXT);"
docker exec -it test-db psql -U postgres -c "INSERT INTO cats VALUES ('Whiskers');"
docker exec -it test-db psql -U postgres -c "SELECT * FROM cats;"
# → Whiskers ✓

# Now remove the container
docker rm -f test-db

# Start a fresh one
docker run -d --name test-db2 -e POSTGRES_PASSWORD=secret postgres:16

# Check if Whiskers is there
docker exec -it test-db2 psql -U postgres -c "SELECT * FROM cats;"
```

Error: `relation "cats" does not exist`.

**Whiskers is gone forever.** The new container started from a fresh copy of the postgres image, with no memory of the old one.

---

## 2. The Solution: Volumes

A **volume** is a storage folder managed by Docker, outside the container's filesystem. When you attach a volume to a container, data written to a specific path inside the container actually lands on the volume — which survives container deletion.

```bash
# Create a volume
docker volume create pgdata

# Run PostgreSQL with the volume attached
docker run -d --name test-db -e POSTGRES_PASSWORD=secret -v pgdata:/var/lib/postgresql/data postgres:16

# Now PostgreSQL stores its data on the 'pgdata' volume,
# NOT inside the container filesystem
```

> **💻 Windows PowerShell note:** The backslash (`\`) line continuation doesn't work in PowerShell. On Windows, put the whole command on one line (as shown above), or use the backtick (`` ` ``) as a line continuation:
>
> ```powershell
> docker run -d `
>   --name test-db `
>   -e POSTGRES_PASSWORD=secret `
>   -v pgdata:/var/lib/postgresql/data `
>   postgres:16
> ```

Try the experiment again:

```bash
# Create a table
docker exec -it test-db psql -U postgres -c "CREATE TABLE cats (name TEXT);"
docker exec -it test-db psql -U postgres -c "INSERT INTO cats VALUES ('Whiskers');"

# Remove the container
docker rm -f test-db

# Start a new one with the SAME volume
docker run -d --name test-db2 -e POSTGRES_PASSWORD=secret -v pgdata:/var/lib/postgresql/data postgres:16

# Check for Whiskers (give it a second to start)
docker exec -it test-db2 psql -U postgres -c "SELECT * FROM cats;"
# → Whiskers ✓
```

**Whiskers survived!** 🐱 The data lives on the volume, not in the container.

---

## 3. Named Volumes vs Bind Mounts

There are two ways to persist data:

### Named Volumes (Docker-managed)

```bash
docker volume create my-data
docker run -v my-data:/app/data my-image
```

- Docker creates and manages the folder
- Stored somewhere in `/var/lib/docker/volumes/` on your machine
- **Best for:** database data, caches, anything you don't want to touch directly

### Bind Mounts (your machine's filesystem)

```bash
docker run -v /absolute/path/on/host:/app/data my-image
```

- Maps a specific folder from your computer into the container
- You can edit files on your machine and the container sees the changes instantly
- **Best for:** development (hot-reload your code without rebuilding)

---

## 4. Bind Mounts for Development

This is the single most useful development trick in Docker.

Remember our Flask app from lesson 03? Every time we changed the code, we had to rebuild the image. With a **bind mount**, you can sync your local code folder into the container so changes take effect immediately.

```bash
# Run with a bind mount instead of COPY
# macOS / Linux:
docker run -d -p 5000:5000 -v $(pwd):/app flask-app

# Windows PowerShell:
# docker run -d -p 5000:5000 -v ${PWD}:/app flask-app
#
# Windows Command Prompt (cmd.exe):
# docker run -d -p 5000:5000 -v %cd%:/app flask-app
```

> 💻 **Cross-platform tip:** The `$(pwd)` syntax works on macOS and Linux but **not** on Windows. Use one of these instead — replace `C:\Users\Szonja\my-project` with your actual project folder:
>
> **PowerShell:**
> ```powershell
> docker run -d -p 5000:5000 -v ${PWD}:/app flask-app
> ```
>
> **Command Prompt (cmd.exe):**
> ```cmd
> docker run -d -p 5000:5000 -v %cd%:/app flask-app
> ```
>
> **Or use a full path (works everywhere):**
> ```bash
> docker run -d -p 5000:5000 -v /home/szonja/my-project:/app flask-app
> ```
> 
> ⚠️ Important: replace `/home/szonja/my-project` with your actual folder path — don't use it literally!

Now any change you make to `app.py` on your machine is instantly visible inside the container. If Flask is in debug mode, it auto-reloads. No rebuild needed.

**This is how professional developers use Docker in development:** build the image infrequently (just for new dependencies), use bind mounts for code changes.

---

## 5. Volumes in Docker Compose

In the note-taking API from lesson 04, we already used volumes:

```yaml
services:
  db:
    image: postgres:16
    volumes:
      - pgdata:/var/lib/postgresql/data    # named volume for database
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql  # bind mount for init script

  api:
    build: ./backend
    volumes:
      - ./backend:/app    # bind mount for hot-reload during development

volumes:
  pgdata:    # declare the named volume here
```

Two types of volume in one `docker-compose.yml`:
- **`pgdata:/var/lib/postgresql/data`** — named volume, persists database across restarts
- **`./backend:/app`** — bind mount, live code sync for development
- **`./db/init.sql:...`** — bind mount, injects a setup script into PostgreSQL's init folder

---

## 6. Volume Management

```bash
# List volumes
docker volume ls

# Inspect a volume (shows where it lives on your machine)
docker volume inspect pgdata

# Remove unused volumes
docker volume prune

# Remove a specific volume
docker volume rm pgdata

# Copy files between a container and your machine
# First find your actual container name:
docker compose ps
# The NAME column shows container names.
# Docker Compose names them: {your-folder}-{service}-1
#   e.g. Docker_compose_practice-api-1   ← if your folder is Docker_compose_practice
#         note-app-api-1                  ← if your folder is note-app

# Copy app.py FROM the API container TO your machine
docker cp docker_compose_practice-api-1:/app/app.py ./

# Move a local file INTO the container
docker cp ./app.py docker_compose_practice-api-1:/app/app.py

# You can also grab requirements.txt from the container
docker cp docker_compose_practice-api-1:/app/requirements.txt ./
```

> 💡 **Don't know your container name?** Run `docker compose ps` and look at the NAME column. It's always `{your-project-folder}-{service}-1`. With folder `Docker_compose_practice`, you get `docker_compose_practice-api-1`. With folder `note-app`, you'd get `note-app-api-1`.

---

## 7. When Containers Share Volumes

Multiple containers can mount the same volume simultaneously:

```yaml
services:
  app:
    image: my-app
    volumes:
      - shared-data:/app/uploads

  backup:
    image: busybox
    volumes:
      - shared-data:/backup
    command: sh -c "cp -r /backup/* /backups/"

volumes:
  shared-data:
```

The backup container can access the same files the app writes. This is how you'd add a log processor, thumbnail generator, or database backup service.

---

## 8. Production Warning

In development, bind mounts are great. In production, you rarely use them — instead you rely on **named volumes** (for databases) and **the image itself** (for code). In production, code lives inside the image from CI/CD, not synced from a developer's laptop.

---

## 🔨 Your Turn

1. Create a named volume called `mydata`. Run a container that writes the current date to `/data/date.txt` on that volume. Remove the container. Run another container that reads that file — is it still there?
2. Try a bind mount: create a local folder `./logs`, mount it to `/app/logs` in a container, have the container write a log file. Verify the file appears on your machine.
3. In the note-taking Compose project from lesson 04, remove the `pgdata` volume config from the database service. Run `docker compose down -v` and `docker compose up`. Create a note, then down and up again. What happened to the note?

## 📝 Solutions

### Exercise 1: Named volume persistence

```bash
# Step 1: Create the volume
docker volume create mydata

# Step 2: Run a container that writes the date to /data/date.txt
docker run --rm -v mydata:/data alpine sh -c "date > /data/date.txt && echo 'Date written!'"

# Step 3: Run another container to read the file
docker run --rm -v mydata:/data alpine cat /data/date.txt
# Output: Thu Jul 30 15:30:00 UTC 2026 (or whatever the current date is)
```

The file **is still there** because even though the first container was deleted (`--rm` removes it automatically), the named volume persists. The second container mounted the same volume and found the file.

### Exercise 2: Bind mount for logs

```bash
# Step 1: Create a local folder
mkdir -p ./logs

# Windows (PowerShell): New-Item -ItemType Directory -Path ./logs -Force
# Windows (CMD): mkdir logs

# Step 2: Run a container that writes a log file
# On macOS / Linux:
docker run --rm -v $(pwd)/logs:/app/logs alpine sh -c "echo 'App started at \$(date)' > /app/logs/app.log && ls -la /app/logs"

# For Windows PowerShell, replace $(pwd) with ${PWD}:
docker run --rm -v ${PWD}/logs:/app/logs alpine sh -c "echo 'App started at \$(date)' > /app/logs/app.log && ls -la /app/logs"

# For Windows CMD, replace $(pwd) with %cd%:
docker run --rm -v %cd%/logs:/app/logs alpine sh -c "echo 'App started at \$(date)' > /app/logs/app.log && ls -la /app/logs"

# Step 3: Verify the file exists on your machine
cat ./logs/app.log
# Output: App started at Thu Jul 30 15:30:00 UTC 2026

# Windows PowerShell:
Get-Content ./logs/app.log
```

The bind mount maps the `./logs` folder on your machine directly into the container at `/app/logs`. Anything the container writes there shows up on your computer.

### Exercise 3: Removing the volume from Compose

In your `docker-compose.yml`, find the `db` service and **remove** the `volumes` section:

```yaml
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: notes
      POSTGRES_PASSWORD: secret
    # Remove or comment out these lines:
    # volumes:
    #   - pgdata:/var/lib/postgresql/data
```

Then:

```bash
# Shut down and delete volumes
docker compose down -v

# Start fresh
docker compose up -d

# Create a note
curl -X POST http://localhost:5000/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","body":"Will this survive?"}'

# Shut down again
docker compose down

# Start again
docker compose up -d

# Check your notes — they're gone!
curl http://localhost:5000/notes
# Output: []
```

**What happened?** Without the `pgdata` named volume, PostgreSQL uses an **anonymous volume** or the container's internal filesystem. When you ran `docker compose down` (without `-v`), the anonymous volume was detached and a new one was created on restart — fresh database, no data. The note is lost.

This is why explicit named volumes are important — they let data survive container restarts.

---

**Continue to [Lesson 6: Docker Networking: Connecting Containers](06-docker-networking.md)**
