# Python Lesson 13: Building Your Own API — Creating Web Services 🌐

**← Back to [Lesson 12: Testing Your Code](12-testing-your-code.md)**

---

## What is an API?

**Plain English:** An API (Application Programming Interface) lets other programs talk to your program.

**Real-world analogy:** Think of a restaurant:
- **Kitchen** = Your code with data and functions
- **Menu** = The API (shows what's available)
- **Customer** = Other programs that want to use your data
- **Waiter** = The API that takes orders and brings food

You create the menu (API) so customers (other programs) can order what they want!

---

## Why Build an API?

**Without an API:**
```python
# Only you can use your code directly
data = get_users()
print(data)
```

**With an API:**
```python
# Anyone can access your data from anywhere!
# Other programs make HTTP requests to your API
GET /users → Returns list of users
POST /users → Creates new user
```

**Real-world examples:**
- Twitter API — Lets apps post tweets
- Google Maps API — Lets apps show maps
- Payment APIs — Lets websites process payments

---

## Understanding HTTP Methods

APIs use HTTP methods to specify what action to take:

| Method | Purpose | Example |
|--------|---------|---------|
| `GET` | Fetch data | Get all users |
| `POST` | Create data | Add a new user |
| `PUT` | Update data | Edit a user |
| `DELETE` | Remove data | Delete a user |

**Memory trick:** Think **CRUD** (Create, Read, Update, Delete)

---

## Understanding HTTP Status Codes

Status codes tell you what happened with your request:

| Code | Meaning | When it's used |
|------|---------|----------------|
| `200` | OK | Request succeeded |
| `201` | Created | Resource created successfully |
| `400` | Bad Request | Invalid data sent |
| `404` | Not Found | Resource doesn't exist |
| `500` | Server Error | Something broke on the server |

**Categories:**
- `2xx` = Success ✅
- `4xx` = Client error (you sent bad data) ❌
- `5xx` = Server error (their code broke) ❌

---

## What is Flask?

**Flask** is a Python framework for building APIs and web apps.

**Install Flask:**
```bash
# macOS/Linux
pip install flask

# Windows (PowerShell)
pip install flask
```

**Verify installation:**
```bash
pip show flask
```

---

## Your First Flask API

**Basic Flask app:**
```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
```

**Run it:**
```bash
# macOS/Linux
python app.py

# Windows (PowerShell)
python app.py
```

**Expected output:**
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

**Visit:** `http://127.0.0.1:5000/` in your browser

**Stop the server:** Press `Ctrl+C` in the terminal

---

## Creating API Endpoints

**Endpoints** are URLs that return data:

```python
# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
    users = [
        {"id": 1, "name": "Szonja"},
        {"id": 2, "name": "Arthur"}
    ]
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = {"id": user_id, "name": "Szonja"}
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=True)
```

**Run it:**
```bash
python app.py
```

**Test it:**

**Option 1: Browser (for GET requests)**
- Visit: `http://127.0.0.1:5000/users`
- Visit: `http://127.0.0.1:5000/users/1`

**Option 2: Using curl (macOS/Linux)**
```bash
# Get all users
curl http://localhost:5000/users

# Get user with ID 1
curl http://localhost:5000/users/1
```

**Option 3: Using curl (Windows PowerShell)**
```powershell
# Get all users
curl.exe http://localhost:5000/users

# Get user with ID 1
curl.exe http://localhost:5000/users/1
```

**Option 4: Using PowerShell Invoke-RestMethod (Windows)**
```powershell
# Get all users
Invoke-RestMethod -Uri http://localhost:5000/users

# Get user with ID 1
Invoke-RestMethod -Uri http://localhost:5000/users/1
```

**Expected output:**
```json
[{"id": 1, "name": "Szonja"}, {"id": 2, "name": "Arthur"}]
```

---

## Adding Data with POST

**POST** lets you send data to your API:

```python
# app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

users = []

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    
    new_user = {
        "id": len(users) + 1,
        "name": name
    }
    users.append(new_user)
    
    return jsonify(new_user), 201

if __name__ == '__main__':
    app.run(debug=True)
```

**Test with curl (macOS/Linux):**
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Emma"}'
```

**Test with curl (Windows PowerShell):**
```powershell
curl.exe -X POST http://localhost:5000/users `
  -H "Content-Type: application/json" `
  -d '{"name": "Emma"}'
```

**Test with PowerShell Invoke-RestMethod (Windows):**
```powershell
$body = @{ name = "Emma" } | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:5000/users -Method POST -Body $body -ContentType "application/json"
```

**Test with Python (Cross-platform):**
```python
# test_post.py
import requests

url = "http://localhost:5000/users"
data = {"name": "Emma"}

response = requests.post(url, json=data)
print(response.json())
print(f"Status code: {response.status_code}")
```

**Expected output:**
```json
{"id": 1, "name": "Emma"}
```
Status code: 201

---

## Understanding JSON

**JSON** (JavaScript Object Notation) is how data is sent in APIs.

**Python dict vs JSON:**
```python
# Python dictionary
user = {"name": "Szonja", "age": 30}

# JSON string (what gets sent over the internet)
'{"name": "Szonja", "age": 30}'
```

**Flask handles conversion automatically:**
- `jsonify()` — Python dict → JSON (for responses)
- `request.get_json()` — JSON → Python dict (for requests)

---

## Practice Exercise

**Scenario:** You're building a task management API for a todo app!

**Your task:**
1. Create a Flask app called `task_api.py`
2. Create an in-memory list to store tasks
3. Create these endpoints:
   - `GET /tasks` — Returns all tasks
   - `GET /tasks/<int:task_id>` — Returns a specific task
   - `POST /tasks` — Creates a new task (takes `title` and `priority` as JSON)
   - `PUT /tasks/<int:task_id>` — Marks a task as complete
   - `DELETE /tasks/<int:task_id>` — Deletes a task
4. Each task should have: `id`, `title`, `priority`, `completed` (boolean)
5. Test all endpoints using curl, PowerShell, or Postman
6. Add error handling (return 404 if task not found)

**Testing tools:**
- **Postman** (GUI tool, works on all platforms): https://www.postman.com/downloads/
- **curl** (command line, built into macOS/Linux)
- **PowerShell Invoke-RestMethod** (built into Windows)

**Example curl commands (macOS/Linux):**
```bash
# Create a task
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Python", "priority": "high"}'

# Get all tasks
curl http://localhost:5000/tasks

# Mark task as complete
curl -X PUT http://localhost:5000/tasks/1

# Delete a task
curl -X DELETE http://localhost:5000/tasks/1
```

**Example PowerShell commands (Windows):**
```powershell
# Create a task
$body = @{ title = "Learn Python"; priority = "high" } | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:5000/tasks -Method POST -Body $body -ContentType "application/json"

# Get all tasks
Invoke-RestMethod -Uri http://localhost:5000/tasks

# Mark task as complete
Invoke-RestMethod -Uri http://localhost:5000/tasks/1 -Method PUT

# Delete a task
Invoke-RestMethod -Uri http://localhost:5000/tasks/1 -Method DELETE
```

**Try it yourself first!** Solution below.

---

## Solution

```python
# task_api.py

from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory task storage
tasks = []
task_id_counter = 1


@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Return all tasks."""
    return jsonify(tasks)


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Return a specific task."""
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if task:
        return jsonify(task)
    else:
        return jsonify({"error": "Task not found"}), 404


@app.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    global task_id_counter
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    new_task = {
        "id": task_id_counter,
        "title": data['title'],
        "priority": data.get('priority', 'medium'),
        "completed": False
    }
    
    tasks.append(new_task)
    task_id_counter += 1
    
    return jsonify(new_task), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def complete_task(task_id):
    """Mark a task as complete."""
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if task:
        task['completed'] = True
        return jsonify(task)
    else:
        return jsonify({"error": "Task not found"}), 404


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if task:
        tasks = [t for t in tasks if t['id'] != task_id]
        return jsonify({"message": "Task deleted"})
    else:
        return jsonify({"error": "Task not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Testing the solution (cross-platform):**

**Option 1: Python test script (works everywhere)**
```python
# test_api.py
import requests

BASE_URL = "http://localhost:5000"

# Create a task
print("Creating task...")
response = requests.post(f"{BASE_URL}/tasks", json={
    "title": "Learn Python",
    "priority": "high"
})
print(f"Created: {response.json()}")
print(f"Status: {response.status_code}")

# Get all tasks
print("\nGetting all tasks...")
response = requests.get(f"{BASE_URL}/tasks")
print(f"Tasks: {response.json()}")

# Mark task as complete
print("\nMarking task as complete...")
response = requests.put(f"{BASE_URL}/tasks/1")
print(f"Updated: {response.json()}")

# Delete task
print("\nDeleting task...")
response = requests.delete(f"{BASE_URL}/tasks/1")
print(f"Deleted: {response.json()}")
```

**Run the test:**
```bash
# Make sure your Flask app is running in one terminal
python test_api.py
```

---

## Common Mistakes and Warnings

### Mistake 1: Forgetting to Import request

**Wrong:**
```python
from flask import Flask

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()  # NameError: name 'request' is not defined!
```

**Right:**
```python
from flask import Flask, request

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()  # Works!
```

---

### Mistake 2: Returning Wrong Status Code

**Wrong:**
```python
@app.route('/users', methods=['POST'])
def create_user():
    # Returns 200 (OK) but should return 201 (Created)
    return jsonify(new_user)
```

**Right:**
```python
@app.route('/users', methods=['POST'])
def create_user():
    # Returns 201 (Created) - correct!
    return jsonify(new_user), 201
```

---

### Mistake 3: Not Handling Missing Data

**Wrong:**
```python
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data['name']  # KeyError if 'name' is missing!
```

**Right:**
```python
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    name = data['name']
```

---

### Mistake 4: Confusing request and requests

**Common confusion:**
- `request` (no 's') — Flask module for handling incoming requests
- `requests` (with 's') — Python library for making HTTP requests

**Correct usage:**
```python
# In your Flask API (handling incoming requests)
from flask import request

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()  # Flask's request

# In a test script (making outgoing requests)
import requests

response = requests.post(url, json=data)  # requests library
```

---

## Limitations of This Approach

**Important:** This API uses **in-memory storage**, which means:

❌ Data is lost when the server restarts
❌ Each server instance has its own copy of data
❌ Not suitable for production

**Example:**
```python
# This data disappears when server stops!
tasks = []
```

**Next lesson:** We'll learn how to use **databases** for permanent storage!

---

## Quick Recap

- **API** — Lets other programs talk to your program
- **Flask** — Python framework for building APIs
- **HTTP Methods** — GET (read), POST (create), PUT (update), DELETE (delete)
- **Status Codes** — 200 (OK), 201 (Created), 400 (Bad Request), 404 (Not Found)
- **`@app.route()`** — Decorator to define endpoints
- **`jsonify()`** — Convert Python dict to JSON response
- **`request.get_json()`** — Get JSON data from incoming request
- **In-memory storage** — Data lost on restart (use databases in production)

---

## What's Next?

Ready to make your data permanent? Continue to **[Lesson 14: Working with Databases](14-working-with-databases.md)**! 🚀

---

**Your turn:** Try the task API exercise! Test it with Python's `requests` library for cross-platform compatibility! 🌐💛
