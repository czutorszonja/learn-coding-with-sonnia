# Python Lesson 15: Building Your Own API 🚀

**← Back to [Lesson 14: Testing Your Code](14-testing.md)**

---

## What is a REST API?

**Plain English:** A REST API lets other programs access your data over HTTP.

**Real-world analogy:** You own a restaurant:
- **Your kitchen** = Your database/data
- **Menu** = API documentation (what's available)
- **Waiters** = API endpoints (how to order)
- **Customers** = Other developers/apps

---

## Why Build an API?

- Let others use your data
- Create mobile app backends
- Connect different services
- Monetize your data

**Examples:**
- Twitter API (post tweets programmatically)
- Stripe API (process payments)
- Weather API (get forecasts)

---

## Introduction to FastAPI

FastAPI is modern, fast, and easy to use:

**Install:**
```bash
pip install fastapi uvicorn
```

**Your first API:**
```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

**Run:**
```bash
uvicorn main:app --reload
```

**Visit:** `http://127.0.0.1:8000/`

---

## API Endpoints

### GET — Retrieve data

```python
@app.get("/users")
def get_users():
    return {"users": ["Alice", "Bob", "Charlie"]}
```

**Response:**
```json
{"users": ["Alice", "Bob", "Charlie"]}
```

---

### POST — Create data

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

@app.post("/users")
def create_user(user: User):
    return {"message": f"User {user.name} created!"}
```

**Request body:**
```json
{"name": "Alice", "age": 30}
```

---

### PUT — Update data

```python
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    return {"message": f"User {user_id} updated!"}
```

---

### DELETE — Remove data

```python
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    return {"message": f"User {user_id} deleted!"}
```

---

## Path Parameters

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/users/{user_id}/posts/{post_id}")
def get_user_post(user_id: int, post_id: int):
    return {"user_id": user_id, "post_id": post_id}
```

**URLs:**
- `/users/123`
- `/users/123/posts/456`

---

## Query Parameters

```python
@app.get("/items")
def get_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

**URLs:**
- `/items` → `{"skip": 0, "limit": 10}`
- `/items?skip=20&limit=5` → `{"skip": 20, "limit": 5}`

---

## Request Body with Pydantic

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    description: str | None = None
    in_stock: bool = True

@app.post("/products")
def create_product(product: Product):
    return {"message": f"Product {product.name} created!", "price": product.price}
```

**Request:**
```json
{
    "name": "Laptop",
    "price": 999.99,
    "description": "High-performance laptop",
    "in_stock": true
}
```

---

## Connecting to a Database

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Database connection
def get_db():
    conn = sqlite3.connect("blog.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table
def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

class Post(BaseModel):
    title: str
    content: str

@app.post("/posts")
def create_post(post: Post):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO posts (title, content) VALUES (?, ?)",
        (post.title, post.content)
    )
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()
    return {"id": post_id, "message": "Post created!"}

@app.get("/posts")
def get_posts():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    conn.close()
    return {"posts": [dict(p) for p in posts]}

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    conn.close()
    
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found!")
    
    return dict(post)

# Initialize database on startup
init_db()
```

---

## Error Handling

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Invalid item ID!")
    
    # ... fetch item ...
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found!")
    
    return item
```

---

## API Documentation

FastAPI auto-generates docs!

**Interactive docs:**
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

**Features:**
- Try endpoints directly in browser
- See request/response schemas
- Auto-generated from your code!

---

## Practice Exercise

### Scenario: You're building a book library API!

**Your task:**
1. Install FastAPI and uvicorn
2. Create a FastAPI app
3. Create a Pydantic model called `Book` with `title`, `author`, and `year` fields
4. Create an in-memory list to store books
5. Add a GET `/` endpoint that returns a welcome message
6. Add a GET `/books` endpoint that returns all books
7. Add a POST `/books` endpoint that adds a new book
8. Add a GET `/books/{book_id}` endpoint that returns a specific book
9. Test all endpoints with Swagger UI (`/docs`)

**Try it yourself first!** Scroll down when ready.

---

## Solutions

### Solution 1: Build a Book Library API

```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Book model
class Book(BaseModel):
    title: str
    author: str
    year: int

# In-memory storage
books = []

# Welcome endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Library!"}

# Get all books
@app.get("/books")
def get_books():
    return {"books": books}

# Add a book
@app.post("/books")
def create_book(book: Book):
    book_dict = book.dict()
    book_dict["id"] = len(books)
    books.append(book_dict)
    return book_dict

# Get specific book
@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id < 0 or book_id >= len(books):
        raise HTTPException(status_code=404, detail="Book not found!")
    return books[book_id]
```

**Run:**
```bash
uvicorn main:app --reload
```

**Test:**
1. Visit `http://127.0.0.1:8000/docs`
2. Try GET `/` → Welcome message
3. Try POST `/books` with `{"title": "1984", "author": "George Orwell", "year": 1949}`
4. Try GET `/books` → See all books
5. Try GET `/books/0` → Get first book

---

## Quick Recap

- **REST API** = Let others access your data
- **FastAPI** = Modern, fast Python framework
- **Endpoints** = GET (read), POST (create), PUT (update), DELETE (delete)
- **Pydantic** = Validate request data
- **Path parameters** = `/users/{id}`
- **Query parameters** = `/items?skip=0&limit=10`
- **Swagger UI** = Auto-generated docs at `/docs`
- **SQLite** = Simple database for small projects

---

## What's Next?

**Congratulations!** You've completed the Python fundamentals course! 🎉

**Next steps:**
- Build a real project with what you've learned
- Learn about deployment (Docker, cloud services)
- Explore advanced topics (async/await, websockets, GraphQL)
- Contribute to open source!

**Keep coding!** 💛🌞

---

