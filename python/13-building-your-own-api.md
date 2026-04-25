# Python Lesson 13: Building Your Own API — Creating Web Services 🌐

**← Back to [Lesson 12: Testing Your Code](12-testing-your-code.md)**

---

## What is an API?

**Plain English:** An API (Application Programming Interface) lets other programs talk to your program.

**Real-world analogy:** Think of a restaurant menu:
- Kitchen = Your code with data and functions
- Menu = The API (shows what's available)
- Customer = Other programs that want to use your data

You create the menu (API) so others can order (make requests)!

---

## Why Build an API?

**Without an API:**
```python
# Only you can use your code
data = get_users()
print(data)
```

**With an API:**
```python
# Anyone can access your data from anywhere!
# Other programs can request data via HTTP
GET /users → Returns list of users
POST /users → Creates new user
```

---

## What is Flask?

**Flask** is a Python framework for building APIs and web apps.

**Install Flask:**
```bash
pip install flask
```

**Basic Flask app:**
```python
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
python app.py
```

**Visit:** `http://127.0.0.1:5000/`

---

## Creating API Endpoints

**Endpoints** are URLs that return data:

```python
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

**Test it:**
- `GET /users` → Returns all users
- `GET /users/1` → Returns user with ID 1

---

## Adding Data with POST

**POST** lets you send data to your API:

```python
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

**Test with curl:**
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Emma"}'
```

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
5. Test all endpoints using curl or Postman
6. Add error handling (return 404 if task not found)

**Example curl commands:**
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

---

## Quick Recap

- **Flask** — Python framework for building APIs
- **`@app.route()`** — Decorator to define endpoints
- **`GET`** — Fetch data
- **`POST`** — Create data
- **`PUT`** — Update data
- **`DELETE`** — Remove data
- **`jsonify()`** — Convert Python objects to JSON
- **`request.get_json()`** — Get JSON data from request
- **Status codes** — 200 OK, 201 Created, 404 Not Found, 400 Bad Request

---

## What's Next?

Ready for more? Continue to **[Lesson 14: Working with Databases](14-working-with-databases.md)**! 🚀

---

**Your turn:** Try the task API exercise! Add features like filtering by priority or sorting by date! 🌐💛
