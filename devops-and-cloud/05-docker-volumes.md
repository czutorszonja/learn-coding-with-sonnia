# 05 — Volumes: Keeping Data Alive When Containers Die

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
docker run -d \
  --name test-db \
  -e POSTGRES_PASSWORD=secret \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16

# Now PostgreSQL stores its data on the 'pgdata' volume,
# NOT inside the container filesystem
```

Try the experiment again:

```bash
# Create a table
docker exec -it test-db psql -U postgres -c "CREATE TABLE cats (name TEXT);"
docker exec -it test-db psql -U postgres -c "INSERT INTO cats VALUES ('Whiskers');"

# Remove the container
docker rm -f test-db

# Start a new one with the SAME volume
docker run -d \
  --name test-db2 \
  -e POSTGRES_PASSWORD=secret \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16

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
docker run -d -p 5000:5000 \
  -v $(pwd):/app \
  flask-app
```

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

# Copy data between containers and volumes
docker cp my-api-container:/logs/app.log ./     # Copy out of container
docker cp ./config.json my-api-container:/app/  # Copy into container
```

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

> **Next up:** Lesson 06 — Networking: how containers talk to each other.
