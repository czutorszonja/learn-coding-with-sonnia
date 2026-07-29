# 04 — Docker Compose: Running Multiple Services

**← Back to [Lesson 3: Dockerfiles: Baking Your Own Images](03-dockerfiles.md)**


So far we've run one container at a time. But real apps are never just one thing.

A typical web app has:
- A **frontend** (React, Vue, etc.)
- A **backend API** (Flask, FastAPI, etc.)
- A **database** (PostgreSQL, MySQL, etc.)
- Maybe **Redis** for caching
- Maybe a **queue** like RabbitMQ

You *could* run each container manually with `docker run`. But you'd need to remember the ports, the volumes, the environment variables, and the right order. That gets old fast.

---

## 1. Enter Docker Compose

Docker Compose lets you define all your services in a single YAML file and start them with one command.

Instead of:

```bash
docker run -d --name db -e POSTGRES_PASSWORD=secret postgres:16
docker run -d --name api -p 5000:5000 --link db my-api
docker run -d --name frontend -p 3000:3000 --link api my-frontend
```

You write:

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: secret

  api:
    build: ./api
    ports:
      - "5000:5000"
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
```

And start everything with:

```bash
docker compose up
```

> 🔔 **Don't copy this example yet** — it's just to show the idea. The practice exercise below uses `backend/` instead of `api/` and `frontend/`. Follow that one step by step.

---

## 2. Our First Compose File

Let's build the note-taking API from scratch — a Flask backend + PostgreSQL database.

### 📁 Step 0: Create all the files first

Before we can run `docker compose up`, we need every file in place. Create a folder called `note-app` (or whatever you want), then create these files inside it:

```
note-app/
├── docker-compose.yml     ← The glue that ties everything together
├── backend/
│   ├── Dockerfile          ← How to build the Flask app image
│   ├── requirements.txt    ← Python dependencies
│   └── app.py              ← The Flask application code
└── db/
    └── init.sql            ← SQL to create the notes table
```

Create each one before moving on:

---

#### File 1: `backend/app.py`

```python
from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        database=os.getenv('DB_NAME', 'notes'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'secret')
    )

@app.route('/notes', methods=['GET'])
def list_notes():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, title, body FROM notes ORDER BY id')
    notes = [{'id': r[0], 'title': r[1], 'body': r[2]} for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(notes)

@app.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO notes (title, body) VALUES (%s, %s) RETURNING id',
        (data['title'], data['body'])
    )
    note_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': note_id, 'title': data['title'], 'body': data['body']}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

#### File 2: `backend/requirements.txt`

```
flask==3.1.0
psycopg2-binary==2.9.9
```

---

#### File 3: `backend/Dockerfile`

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

---

#### File 4: `db/init.sql`

```sql
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    body TEXT NOT NULL
);
```

---

#### File 5: `docker-compose.yml`

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: notes
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql

  api:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      DB_HOST: db
      DB_NAME: notes
      DB_USER: postgres
      DB_PASSWORD: secret
    depends_on:
      - db
    volumes:
      - ./backend:/app

volumes:
  pgdata:
```

---

### ▶️ Now run it

Once all 5 files exist, run:

```bash
docker compose up
```

Docker Compose will:
1. Create a network for all services to talk to each other
2. Start PostgreSQL with the notes table pre-created
3. Build and start the Flask API
4. Show logs from both services in real time

Test it:

> **💻 Cross-platform tip:** The commands below use Unix-style curl with backslash line breaks and single quotes. If you're on **Windows PowerShell**, see the Windows alternatives after the demo section.

```bash
# Create a note
curl -X POST http://localhost:5000/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Shopping","body":"Milk, eggs, bread"}'

# List all notes
curl http://localhost:5000/notes
```

> **💡 Windows PowerShell alternatives**
>
> PowerShell's built-in `curl` is actually `Invoke-WebRequest` — it won't work with these flags.
> Use one of these instead:
>
> ```powershell
> # A) Use curl.exe with a variable for the JSON body
> $body = '{"title":"Shopping","body":"Milk, eggs, bread"}'
> curl.exe -X POST http://localhost:5000/notes -H "Content-Type: application/json" -d $body
>
> # B) PowerShell-native (no curl needed)
> Invoke-RestMethod -Uri http://localhost:5000/notes -Method Post -ContentType "application/json" -Body '{"title":"Shopping","body":"Milk, eggs, bread"}'
>
> # To list notes:
> Invoke-RestMethod -Uri http://localhost:5000/notes
> ```

---

## 3. How Services Talk to Each Other

Inside Docker Compose, each service name acts as a hostname. The API connects to `db` (which it gets from `DB_HOST` environment variable) and Docker's built-in DNS resolves that to the database container's IP.

This is **automatic** — you don't need to know IP addresses. As long as both services are in the same `docker-compose.yml`, they can reach each other by service name.

```
    api container                          db container
  ┌────────────────┐                  ┌────────────────┐
  │ DB_HOST=db     │──────TCP──────▶ │ Postgres       │
  │ Port 5000      │   port 5432     │ Port 5432      │
  └────────────────┘                  └────────────────┘
        │  hostname "db" resolves inside Docker's network
        │  no IP addresses needed — Docker DNS handles it
```

---

## 4. The Compose File Breakdown

```yaml
services:          # Each service = one container
  db:              # Service name (also acts as hostname)
    image: ...     # Which image to use (or "build: ./path" for a Dockerfile)
    environment:   # Environment variables inside the container
    ports:         # Host:Container port mapping
    volumes:       # Persistent storage
    depends_on:    # Startup order hint

  api:
    build: ./backend  # Build from Dockerfile in this folder
    ...
```

**Key difference between `image` and `build`:**

| | When to use | Example |
|---|---|---|
| `image:` | Someone else's software (PostgreSQL, Redis, Nginx) | `image: postgres:16` |
| `build:` | Your own code | `build: ./backend` |

---

## 5. Useful Compose Commands

```bash
# Start everything (shows logs)
docker compose up

# Start in background
docker compose up -d

# Stop everything
docker compose down

# Stop and delete volumes too (⚠️ deletes database data)
docker compose down -v

# Rebuild images and start
docker compose up --build

# View logs
docker compose logs

# Follow logs from one service
docker compose logs -f api

# Run a one-off command inside a service
docker compose exec api python -c "print('hi')"

# List running services
docker compose ps
```

---

## 6. Real-World Scenario

**Problem:** You're building a web app and need a local environment that matches production. You don't want to install PostgreSQL on your machine (it's messy to clean up). You don't want to configure Redis manually.

**Solution with Compose:** Write a `docker-compose.yml` with all services. New team member joins? They clone the repo and run `docker compose up`. Done. No "oh, I'm on Windows and the Postgres installer failed" conversations.

This is how modern teams ship. Compose files are as standard as `package.json` or `requirements.txt`.

---

## 🔨 Your Turn

1. Add a third service: **Redis** (`redis:7-alpine`). No ports needed unless you want to connect from outside.
2. Modify the Flask app to use Redis for caching (just import `redis` and connect to host `redis`).
3. Add a `depends_on: - redis` to the API service.
4. Run `docker compose up --build` and verify all three services start.
5. Run `docker compose ps` — you should see three containers running.

**Continue to [Lesson 5: Volumes: Keeping Data Alive When Containers Die](05-docker-volumes.md)**
