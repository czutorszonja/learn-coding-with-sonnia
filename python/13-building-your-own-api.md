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

## Updating Data with PUT

**PUT** lets you update existing data in your API:

```python
# app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Emma"},
    {"id": 2, "name": "Arthur"}
]

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    user['name'] = data.get('name', user['name'])
    
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=True)
```

**Test with curl (macOS/Linux):**
```bash
curl -X PUT http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Emma Updated"}'
```

**Test with curl (Windows PowerShell):**
```powershell
curl.exe -X PUT http://localhost:5000/users/1 `
  -H "Content-Type: application/json" `
  -d '{"name": "Emma Updated"}'
```

**Test with PowerShell Invoke-RestMethod (Windows):**
```powershell
$body = @{ name = "Emma Updated" } | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:5000/users/1 -Method PUT -Body $body -ContentType "application/json"
```

**Test with Python (Cross-platform):**
```python
import requests

url = "http://localhost:5000/users/1"
data = {"name": "Emma Updated"}

response = requests.put(url, json=data)
print(f"Updated: {response.json()}")
print(f"Status: {response.status_code}")
```

**Expected output:**
```json
{"id": 1, "name": "Emma Updated"}
```
Status code: 200

---

## Deleting Data with DELETE

**DELETE** lets you remove data from your API:

```python
# app.py
from flask import Flask, jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "Emma"},
    {"id": 2, "name": "Arthur"}
]

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    user = next((u for u in users if u['id'] == user_id), None)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    users = [u for u in users if u['id'] != user_id]
    
    return jsonify({"message": "User deleted"})

if __name__ == '__main__':
    app.run(debug=True)
```

**Test with curl (macOS/Linux):**
```bash
curl -X DELETE http://localhost:5000/users/1
```

**Test with curl (Windows PowerShell):**
```powershell
curl.exe -X DELETE http://localhost:5000/users/1
```

**Test with PowerShell Invoke-RestMethod (Windows):**
```powershell
Invoke-RestMethod -Uri http://localhost:5000/users/1 -Method DELETE
```

**Test with Python (Cross-platform):**
```python
import requests

url = "http://localhost:5000/users/1"

response = requests.delete(url)
print(f"Deleted: {response.json()}")
print(f"Status: {response.status_code}")
```

**Expected output:**
```json
{"message": "User deleted"}
```
Status code: 200

---

## Testing All Methods Together

Here's the complete API with all methods put together using the `users` resource:

```python
# users_api.py
from flask import Flask, jsonify, request

app = Flask(__name__)

users = []
user_id_counter = 1

@app.route('/users', methods=['GET'])
def get_users():
    """Return all users."""
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Return a specific user."""
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    global user_id_counter
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    new_user = {
        "id": user_id_counter,
        "name": data['name'],
        "email": data.get('email', '')
    }
    users.append(new_user)
    user_id_counter += 1
    return jsonify(new_user), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user's details."""
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    if data:
        user.update(data)
    return jsonify(user)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user."""
    global users
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    users = [u for u in users if u['id'] != user_id]
    return jsonify({"message": "User deleted"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Note:** The `PUT` method here uses `user.update(data)` — this lets you update *any* field the request sends (not just one hardcoded field). That's a more flexible approach than the example in the previous section.

**Test with Python (Cross-platform - works on all systems):**
```python
# test_full_api.py
import requests

BASE = "http://localhost:5000"

# 1. Create a user (POST)
print("1. Create user...")
r = requests.post(f"{BASE}/users", json={
    "name": "Alice",
    "email": "alice@example.com"
})
print(f"   Created: {r.json()}, Status: {r.status_code}")

# 2. Get all users (GET)
print("\n2. Get all users...")
r = requests.get(f"{BASE}/users")
print(f"   Users: {r.json()}")

# 3. Get specific user (GET)
print("\n3. Get user #1...")
r = requests.get(f"{BASE}/users/1")
print(f"   User: {r.json()}, Status: {r.status_code}")

# 4. Update user (PUT)
print("\n4. Update user #1 email...")
r = requests.put(f"{BASE}/users/1", json={"email": "newalice@example.com"})
print(f"   Updated: {r.json()}, Status: {r.status_code}")

# 5. Delete user (DELETE)
print("\n5. Delete user #1...")
r = requests.delete(f"{BASE}/users/1")
print(f"   Deleted: {r.json()}, Status: {r.status_code}")

# 6. Try to get deleted user (should be 404)
print("\n6. Try to get deleted user...")
r = requests.get(f"{BASE}/users/1")
print(f"   Response: {r.json()}, Status: {r.status_code}")
```

**Expected output:**
```
1. Create user...
   Created: {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'}, Status: 201

2. Get all users...
   Users: [{'id': 1, 'name': 'Alice', 'email': 'alice@example.com'}]

3. Get user #1...
   User: {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'}, Status: 200

4. Update user #1 email...
   Updated: {'id': 1, 'name': 'Alice', 'email': 'newalice@example.com'}, Status: 200

5. Delete user #1...
   Deleted: {'message': 'User deleted'}, Status: 200

6. Try to get deleted user...
   Response: {'error': 'User not found'}, Status: 404
```

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

**Scenario:** You're building a user management API for an app!

**Your task:**
1. Create a Flask app called `users_api.py`
2. Create an in-memory list to store users
3. Create these endpoints:
   - `GET /users` — Returns all users
   - `GET /users/<int:user_id>` — Returns a specific user
   - `POST /users` — Creates a new user (takes `name` and `email` as JSON)
   - `PUT /users/<int:user_id>` — Updates a user's details
   - `DELETE /users/<int:user_id>` — Deletes a user
4. Each user should have: `id`, `name`, `email`
5. Test all endpoints using curl, PowerShell, or Postman
6. Add error handling (return 404 if user not found)

**Testing tools:**
- **Postman** (GUI tool, works on all platforms): https://www.postman.com/downloads/
- **curl** (command line, built into macOS/Linux)
- **PowerShell Invoke-RestMethod** (built into Windows)

**Example curl commands (macOS/Linux):**
```bash
# Create a user
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'

# Get all users
curl http://localhost:5000/users

# Update a user's email
curl -X PUT http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"email": "newalice@example.com"}'

# Delete a user
curl -X DELETE http://localhost:5000/users/1
```

**Example PowerShell commands (Windows):**
```powershell
# Create a user
$body = @{ name = "Alice"; email = "alice@example.com" } | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:5000/users -Method POST -Body $body -ContentType "application/json"

# Get all users
Invoke-RestMethod -Uri http://localhost:5000/users

# Update a user's email
$body = @{ email = "newalice@example.com" } | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:5000/users/1 -Method PUT -Body $body -ContentType "application/json"

# Delete a user
Invoke-RestMethod -Uri http://localhost:5000/users/1 -Method DELETE
```

**Try it yourself first!** Solution below.

---

## Solution

```python
# users_api.py

from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory user storage
users = []
user_id_counter = 1


@app.route('/users', methods=['GET'])
def get_users():
    """Return all users."""
    return jsonify(users)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Return a specific user."""
    user = next((u for u in users if u['id'] == user_id), None)
    
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    global user_id_counter
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    new_user = {
        "id": user_id_counter,
        "name": data['name'],
        "email": data.get('email', '')
    }
    
    users.append(new_user)
    user_id_counter += 1
    
    return jsonify(new_user), 201


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user's details."""
    user = next((u for u in users if u['id'] == user_id), None)
    
    if user:
        data = request.get_json()
        if data:
            user.update(data)
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user."""
    global users
    user = next((u for u in users if u['id'] == user_id), None)
    
    if user:
        users = [u for u in users if u['id'] != user_id]
        return jsonify({"message": "User deleted"})
    else:
        return jsonify({"error": "User not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Testing the solution (cross-platform):**

**Option 1: Python test script (works everywhere)**
```python
# test_api.py
import requests

BASE_URL = "http://localhost:5000"

# Create a user
print("Creating user...")
response = requests.post(f"{BASE_URL}/users", json={
    "name": "Alice",
    "email": "alice@example.com"
})
print(f"Created: {response.json()}")
print(f"Status: {response.status_code}")

# Get all users
print("\nGetting all users...")
response = requests.get(f"{BASE_URL}/users")
print(f"Users: {response.json()}")

# Update a user's email
print("\nUpdating user #1 email...")
response = requests.put(f"{BASE_URL}/users/1", json={"email": "newalice@example.com"})
print(f"Updated: {response.json()}")

# Delete user
print("\nDeleting user...")
response = requests.delete(f"{BASE_URL}/users/1")
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
