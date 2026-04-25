# Python Lesson 17: Deployment — Putting Your App Online 🌍

**← Back to [Lesson 16: Authentication and Security](16-authentication-and-security.md)**

---

## What is Deployment?

**Plain English:** Deployment means putting your app on a server so others can use it on the internet.

**Real-world analogy:** Think of opening a shop:
- Building the shop = Writing code
- Opening doors = Deploying
- Customers can now visit!

Deployment makes your app accessible to the world!

---

## Why Deploy?

**Without deployment:**
```python
# Only runs on YOUR computer
python app.py
# Others can't access it!
```

**With deployment:**
```python
# Runs on a server
# Anyone with internet can access it!
# https://yourapp.com
```

---

## What You Need to Deploy

1. **A web framework** — Flask (you already know this!)
2. **A database** — SQLite (works for small apps)
3. **Requirements file** — List of packages
4. **A hosting service** — Heroku, Railway, PythonAnywhere

---

## Creating requirements.txt

**requirements.txt** lists all packages your app needs:

```txt
Flask==3.0.0
gunicorn==21.2.0
```

**Create it:**
```bash
pip freeze > requirements.txt
```

---

## Preparing Your Flask App

**Structure:**
```
myapp/
├── app.py
├── requirements.txt
├── .gitignore
└── instance/
    └── users.db
```

**app.py:**
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
```

---

## Using Environment Variables

**NEVER commit passwords or secrets to Git!**

**Use environment variables:**
```python
import os
from flask import Flask

app = Flask(__name__)

# Get secret key from environment
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key')

# Get database URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///users.db')

@app.route('/')
def home():
    return "Hello, World!"
```

**Create `.env` file (locally):**
```
SECRET_KEY=my-super-secret-key
DATABASE_URL=sqlite:///users.db
```

**Add to `.gitignore`:**
```
.env
*.db
__pycache__/
```

---

## Practice Exercise

**Scenario:** You're deploying your task management API to the cloud!

**Your task:**
1. Create a Flask app called `deploy_app.py` with:
   - A home route `/` that returns a welcome message
   - A `/tasks` GET endpoint that returns all tasks
   - A `/tasks` POST endpoint that creates a task
   - Use SQLite for database
2. Create a `requirements.txt` file
3. Create a `.gitignore` file
4. Add environment variable support for:
   - `SECRET_KEY` — for session security
   - `DATABASE_URL` — for database location
5. Create a `Procfile` (for deployment) with:
   ```
   web: gunicorn deploy_app:app
   ```
6. Test locally with:
   ```bash
   pip install -r requirements.txt
   python deploy_app.py
   ```
7. Create a README with deployment instructions

**Example structure:**
```
task-api/
├── deploy_app.py
├── requirements.txt
├── .gitignore
├── Procfile
├── .env
└── instance/
    └── tasks.db
```

**Try it yourself first!** Solution below.

---

## Solution

```python
# deploy_app.py

import os
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Configuration from environment
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key')
DATABASE = os.environ.get('DATABASE_URL', 'tasks.db')


def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            priority TEXT DEFAULT 'medium',
            completed BOOLEAN DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()


@app.route('/')
def home():
    """Home page."""
    return jsonify({
        "message": "Welcome to Task API!",
        "endpoints": {
            "GET /tasks": "Get all tasks",
            "POST /tasks": "Create a task"
        }
    })


@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()
    
    conn.close()
    
    return jsonify([dict(task) for task in tasks])


@app.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    title = data['title']
    priority = data.get('priority', 'medium')
    
    cursor.execute('''
        INSERT INTO tasks (title, priority) VALUES (?, ?)
    ''', (title, priority))
    
    task_id = cursor.lastrowid
    conn.commit()
    
    # Get the created task
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    
    conn.close()
    
    return jsonify(dict(task)), 201


# Initialize database
init_db()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
```

**requirements.txt:**
```txt
Flask==3.0.0
gunicorn==21.2.0
```

**.gitignore:**
```
.env
*.db
__pycache__/
*.pyc
instance/
```

**Procfile:**
```
web: gunicorn deploy_app:app
```

**.env (local testing only):**
```
SECRET_KEY=my-super-secret-key
DATABASE_URL=tasks.db
```

**README.md:**
```markdown
# Task API

A simple task management API.

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:
   ```bash
   python deploy_app.py
   ```

3. Visit: http://localhost:5000

## Deployment

This app is ready to deploy on Heroku, Railway, or PythonAnywhere.

### Heroku

```bash
heroku create
git push heroku main
```

### Railway

Connect your GitHub repo and deploy!

### PythonAnywhere

Upload files and run:
```bash
pip install -r requirements.txt
```

## API Endpoints

- `GET /` — Welcome message
- `GET /tasks` — Get all tasks
- `POST /tasks` — Create a task
```

**To test locally:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python deploy_app.py

# Test endpoints
curl http://localhost:5000/
curl http://localhost:5000/tasks
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn deployment", "priority": "high"}'
```

---

## Quick Recap

- **Deployment** — Put app on server for others to use
- **requirements.txt** — List of packages
- **Environment variables** — Store secrets safely
- **`.env`** — Local environment config (don't commit!)
- **`.gitignore`** — Files to exclude from Git
- **Procfile** — Tells host how to run your app
- **gunicorn** — Production server for Flask

---

## What's Next?

Ready for more? Continue to **[Lesson 18: Project Best Practices](18-project-best-practices.md)**! 🚀

---

**Your turn:** Try the deployment exercise! Deploy to a free host like Railway or PythonAnywhere! 🌍💛
