# 08 — Docker Project: Build a Real-World App

**← Back to [Lesson 7: Docker Best Practices](07-docker-best-practices.md)**


This lesson brings together everything you've learned. We're building a **URL shortener** — a service that turns long URLs into short links (like bit.ly or TinyURL).

This is a real project that uses:
- A **Flask API** (the app)
- **PostgreSQL** (storage)
- **Redis** (caching)
- **Docker Compose** (tying it together)
- **Volumes** (persisting data)
- **Networking** (service discovery)
- **Best practices** (non-root user, .dockerignore, health checks)

---

## Project Structure

```
url-shortener/
├── .dockerignore
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   └── init.sql
```

---

## 1. The App — `backend/app.py`

```python
import os
import random
import string
import redis
import psycopg2
import psycopg2.extras
from flask import Flask, request, redirect, jsonify

app = Flask(__name__)

# ── Database helpers ──

def get_db():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        database=os.getenv('DB_NAME', 'urlshortener'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'secret')
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id SERIAL PRIMARY KEY,
            short_code VARCHAR(10) UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Connect to Redis
cache = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=6379,
    decode_responses=True
)

# ── Helper ──

def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

# ── Routes ──

@app.route('/shorten', methods=['POST'])
def shorten():
    """Create a short URL."""
    data = request.get_json()
    original = data.get('url')
    if not original:
        return jsonify({'error': 'url is required'}), 400

    # Generate a unique short code
    code = generate_code()
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO urls (short_code, original_url) VALUES (%s, %s)',
            (code, original)
        )
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        code = generate_code()  # Try again
        cur.execute(
            'INSERT INTO urls (short_code, original_url) VALUES (%s, %s)',
            (code, original)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

    # Cache it
    cache.set(code, original)

    return jsonify({'short_url': f'http://localhost:5000/{code}'}), 201


@app.route('/<short_code>')
def redirect_url(short_code):
    """Redirect a short code to the original URL."""

    # Try cache first
    original = cache.get(short_code)

    if original is None:
        # Fall back to database
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            'SELECT original_url FROM urls WHERE short_code = %s',
            (short_code,)
        )
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row is None:
            return jsonify({'error': 'URL not found'}), 404

        original = row[0]
        cache.set(short_code, original)  # warm the cache

    return redirect(original)


@app.route('/stats/<short_code>')
def stats(short_code):
    """Show info about a short URL."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        'SELECT short_code, original_url, created_at FROM urls WHERE short_code = %s',
        (short_code,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row is None:
        return jsonify({'error': 'URL not found'}), 404

    return jsonify(dict(row))


@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
```

---

## 2. Dependencies — `backend/requirements.txt`

```
flask==3.1.0
psycopg2-binary==2.9.9
redis==5.2.0
gunicorn==22.0.0
```

---

## 3. SQL Init — `backend/init.sql` (optional, we use CREATE TABLE in code)

We're creating the table in `init_db()`, but if you wanted to use the Compose init mechanism:

```sql
CREATE TABLE IF NOT EXISTS urls (
    id SERIAL PRIMARY KEY,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    original_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 4. Dockerfile — `backend/Dockerfile`

```dockerfile
FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


FROM python:3.12-slim AS runtime

RUN groupadd -r appuser && useradd -r -g appuser -m -d /app appuser
WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY app.py .
COPY --chown=appuser:appuser app.py .

ENV PATH=/root/.local/bin:$PATH

USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

---

## 5. Docker Compose — `docker-compose.yml`

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: urlshortener
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  api:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      DB_HOST: db
      DB_NAME: urlshortener
      DB_USER: postgres
      DB_PASSWORD: secret
      REDIS_HOST: redis
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app    # bind mount for dev (overrides the COPY)
    restart: unless-stopped

volumes:
  pgdata:
  redis-data:
```

---

## 6. .dockerignore

```
__pycache__
*.pyc
.env
.git
.vscode
.DS_Store
*.log
```

---

## 7. Run It

```bash
cd url-shortener
docker compose up --build
```

> **💻 Cross-platform tip:** The curl commands below use Unix-style backslash continuations and single quotes. If you're on Windows, scroll down for PowerShell and Command Prompt alternatives.

Wait for all services to be healthy (check with `docker compose ps`).

```bash
# Shorten a URL
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://docs.docker.com"}'

# → {"short_url":"http://localhost:5000/aB3xYz"}

# Visit the short URL in your browser or:
curl -L http://localhost:5000/aB3xYz
# (the -L flag follows redirects)

# Check stats
curl http://localhost:5000/stats/aB3xYz
# → {"short_code": "aB3xYz", "original_url": "https://docs.docker.com", ...}
```

> **💡 Windows alternatives for curl commands**
>
> **PowerShell:**
> ```powershell
> # Shorten a URL (using curl.exe + variable)
> $body = '{"url": "https://docs.docker.com"}'
> curl.exe -X POST http://localhost:5000/shorten -H "Content-Type: application/json" -d $body
>
> # Or PowerShell-native:
> Invoke-RestMethod -Uri http://localhost:5000/shorten -Method Post -ContentType "application/json" -Body '{"url": "https://docs.docker.com"}'
>
> # Follow a redirect (PowerShell can't use -L like curl — use Invoke-WebRequest with -MaximumRedirection)
> Invoke-WebRequest -Uri http://localhost:5000/aB3xYz -MaximumRedirection 5
>
> # Check stats:
> Invoke-RestMethod -Uri http://localhost:5000/stats/aB3xYz
> ```
>
> **Command Prompt (cmd.exe):**
> ```cmd
> REM Escape double quotes with backslash — cmd.exe needs them
> curl -X POST http://localhost:5000/shorten -H "Content-Type: application/json" -d "{\"url\": \"https://docs.docker.com\"}"
> ```

**Test persistence:**

```bash
docker compose down
docker compose up
curl http://localhost:5000/aB3xYz   # Should still redirect!
```

**Test caching:**

```bash
docker compose exec api python -c "
import redis; r = redis.Redis(host='redis', decode_responses=True)
print('Cached keys:', r.keys())
"
```

---

## What This Project Demonstrates

| Concept | Where it appears |
|---|---|
| Dockerfile with multi-stage build | Separates pip install from runtime |
| Non-root user (`USER appuser`) | Security best practice |
| `.dockerignore` | Keeps build context clean |
| HEALTHCHECK | Both in Dockerfile and Compose |
| Named volumes (`pgdata`, `redis-data`) | Database and cache persist across restarts |
| Bind mount (`./backend:/app`) | Hot-reload during development |
| Docker Compose depends_on with health condition | API won't start until DB is ready |
| Service discovery (`DB_HOST=db`, `REDIS_HOST=redis`) | Containers find each other by name |
| Environment variables for config | No hardcoded secrets |
| Caching layer (Redis) | Reduces DB reads for popular short URLs |
| `restart: unless-stopped` | Auto-restart on crash |

---

## 🔨 Your Turn

1. Shorten 3 different URLs. Visit each one in your browser.
2. Add a `DELETE /<short_code>` endpoint that removes a short URL (you'll need to write the SQL yourself).
3. Add a visit counter: each time someone visits a URL, increment a `visit_count` column. Return it in the stats endpoint.
4. Run `docker compose logs` — can you spot the health check pings?
5. Stop Redis (`docker compose stop redis`). Try visiting a short URL you already visited. Does it still work? What about a new one?

**Continue to [Lesson 01: Welcome to the Cloud: AWS Basics ☁️](../02-aws/01-aws-intro.md)**
