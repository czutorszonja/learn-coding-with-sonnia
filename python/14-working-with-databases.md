# Python Lesson 14: Working with Databases — Storing Data Permanently 🗄️

**← Back to [Lesson 13: Building Your Own API](13-building-your-own-api.md)**

---

## What is a Database?

**Plain English:** A database is like a digital filing cabinet that stores data in an organized way.

**Real-world analogy:** Think of a library:
- Books = Data
- Shelves = Tables
- Catalog system = Database management
- Librarian = Database software (MySQL, PostgreSQL, etc.)

Databases let you store, organize, and retrieve data efficiently!

---

## Why Use Databases?

**Without databases:**
```python
# Data lost when program ends!
users = [{"name": "Szonja", "email": "szonja@example.com"}]
# Save to file manually
```

**With databases:**
```python
# Data saved permanently!
cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", 
               ("Szonja", "szonja@example.com"))
# Data persists even after program ends!
```

---

## What is SQLite?

**SQLite** is a lightweight database that stores data in a single file.

**Why SQLite?**
- No server needed
- Built into Python
- Perfect for learning
- Used in phones, browsers, and apps

---

## Connecting to MySQL

**MySQL** is a full database server (more common in real projects than SQLite).

**Install the MySQL connector:**
```bash
pip install mysql-connector-python
```

**Connect to MySQL:**
```python
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)
cursor = conn.cursor()

# Use the same commands as SQLite after this
cursor.execute("SELECT * FROM users")
results = cursor.fetchall()

conn.close()
```

**Note:** Never write your username and password directly in the code! Use a **config file** (see below).

---

## Using a Config File

**Why?** Your database credentials are private. If you share your code on GitHub, anyone can steal them.

**Solution:** Store them in a separate config file that is **not committed** to GitHub.

**`config.json`** (never share this file):
```json
{
    "host": "localhost",
    "user": "szonja",
    "password": "secretpassword123",
    "database": "hairdresser_db"
}
```

**Load it in your code:**
```python
import json
import mysql.connector

def get_config():
    """Load database credentials from config.json."""
    with open("config.json", "r") as f:
        return json.load(f)

def get_connection():
    """Create a database connection using config.json."""
    config = get_config()
    return mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )

# Use it
conn = get_connection()
cursor = conn.cursor()
print("Connected!")
conn.close()
```

**In your `.gitignore` file (add this line):**
```
config.json
```

This means Git will completely ignore the file and never upload it.

---

## Connecting to a Database

```python
import sqlite3

# Connect to database (creates file if it doesn't exist)
conn = sqlite3.connect('myapp.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE
    )
''')

# Save changes
conn.commit()

# Close connection
conn.close()
```

---

## Inserting Data

```python
import sqlite3

conn = sqlite3.connect('myapp.db')
cursor = conn.cursor()

# Insert a user
cursor.execute('''
    INSERT INTO users (name, email) VALUES (?, ?)
''', ("Szonja", "szonja@example.com"))

# Save changes
conn.commit()
conn.close()
```

**Key points:**
- `?` placeholders prevent SQL injection
- `conn.commit()` saves changes
- Always close connection when done

---

## Querying Data

```python
import sqlite3

conn = sqlite3.connect('myapp.db')
cursor = conn.cursor()

# Get all users
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

for user in users:
    print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")

conn.close()
```

**Query methods:**
- `fetchone()` — Get one row
- `fetchall()` — Get all rows
- `fetchmany(n)` — Get n rows

---

## Exception Handling for Database Operations

Databases can fail — the server might be down, a table doesn't exist, or a query is wrong. Always handle this!

**Basic pattern with try/except:**
```python
import sqlite3

def get_user(user_id):
    """Get a user by ID. Returns None if not found or if an error occurs."""
    try:
        conn = sqlite3.connect('myapp.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        conn.close()
        
        return user
    except Exception as e:
        print(f"Database error: {e}")
        return None
```

**Better pattern — return a tuple with status and data:**
```python
def get_user(user_id):
    """Get a user by ID. Returns (success, data_or_error)."""
    try:
        conn = sqlite3.connect('myapp.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        conn.close()
        
        if user:
            return (True, {"id": user[0], "name": user[1], "email": user[2]})
        else:
            return (False, "User not found")
            
    except Exception as e:
        return (False, str(e))


# Use it
success, result = get_user(1)
if success:
    print(f"Found: {result['name']}")
else:
    print(f"Error: {result}")
```

**Handling write errors (INSERT, UPDATE, DELETE):**
```python
def add_user(name, email):
    """Add a new user. Returns (success, message)."""
    try:
        conn = sqlite3.connect('myapp.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (name, email)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        return (True, f"User added with ID {user_id}")
        
    except Exception as e:
        return (False, f"Error adding user: {e}")


# Use it
success, message = add_user("Szonja", "szonja@example.com")
if success:
    print(message)
else:
    print(f"Failed: {message}")
```

---

## The db_utils Pattern — One File to Rule Them All

A `db_utils.py` file keeps all your database code in one place. Other files import from it instead of talking to the database directly.

**`db_utils.py`:**
```python
import sqlite3

def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect('myapp.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_user(user_id):
    """Get a user by ID. Returns dict or None."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    except Exception as e:
        print(f"Database error: {e}")
        return None

def get_all_users():
    """Get all users. Returns list of dicts."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Database error: {e}")
        return []

def add_user(name, email):
    """Add a user. Returns new user ID or None on error."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (name, email)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except Exception as e:
        print(f"Database error: {e}")
        return None

def update_user(user_id, name=None, email=None):
    """Update a user's name and/or email. Returns True/False."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Build the update dynamically
        updates = []
        params = []
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if email is not None:
            updates.append("email = ?")
            params.append(email)
        
        if not updates:
            return False
        
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        
        cursor.execute(query, params)
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        
        return rows_affected > 0
    except Exception as e:
        print(f"Database error: {e}")
        return False

def delete_user(user_id):
    """Delete a user. Returns True/False."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected > 0
    except Exception as e:
        print(f"Database error: {e}")
        return False
```

**Use it in `main.py` or any other file:**
```python
from db_utils import get_user, get_all_users, add_user, update_user

# Get all users
users = get_all_users()
for user in users:
    print(f"{user['id']}: {user['name']} ({user['email']})")

# Add a user
new_id = add_user("Arthur", "arthur@example.com")
print(f"Added user with ID: {new_id}")

# Update a user
updated = update_user(new_id, email="newarthur@example.com")
print(f"Updated: {updated}")

# Delete a user
deleted = delete_user(new_id)
print(f"Deleted: {deleted}")
```

---

## Practice Exercise

**Scenario:** You're building a book tracking system for a personal library!

**Your task:**
1. Create a database file called `library.db`
2. Create a `books` table with these columns:
   - `id` (INTEGER PRIMARY KEY)
   - `title` (TEXT NOT NULL)
   - `author` (TEXT NOT NULL)
   - `year_published` (INTEGER)
   - `rating` (REAL) — 0.0 to 5.0
3. Create a function called `add_book` that takes title, author, year, and rating
4. Create a function called `get_all_books` that returns all books
5. Create a function called `get_books_by_author` that takes author name and returns matching books
6. Create a function called `update_rating` that updates a book's rating by ID
7. Create a function called `delete_book` that removes a book by ID
8. Test all functions with sample data

**Example usage:**
```python
add_book("Python Crash Course", "Eric Matthes", 2019, 4.5)
add_book("Fluent Python", "Luciano Ramalho", 2015, 5.0)

books = get_all_books()
for book in books:
    print(f"{book['title']} by {book['author']} ({book['year_published']}) - Rating: {book['rating']}")

update_rating(1, 5.0)
delete_book(2)
```

**Try it yourself first!** Solution below.

---

## Solution

```python
# library.py

import sqlite3


def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn


def create_table():
    """Create the books table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year_published INTEGER,
            rating REAL
        )
    ''')
    
    conn.commit()
    conn.close()


def add_book(title, author, year_published, rating):
    """Add a new book to the library."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO books (title, author, year_published, rating)
        VALUES (?, ?, ?, ?)
    ''', (title, author, year_published, rating))
    
    book_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return book_id


def get_all_books():
    """Return all books in the library."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM books ORDER BY title")
    books = cursor.fetchall()
    
    conn.close()
    return [dict(book) for book in books]


def get_books_by_author(author):
    """Return all books by a specific author."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM books WHERE author = ?
    ''', (author,))
    
    books = cursor.fetchall()
    conn.close()
    
    return [dict(book) for book in books]


def update_rating(book_id, new_rating):
    """Update the rating of a book."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE books SET rating = ? WHERE id = ?
    ''', (new_rating, book_id))
    
    conn.commit()
    conn.close()


def delete_book(book_id):
    """Delete a book from the library."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM books WHERE id = ?
    ''', (book_id,))
    
    conn.commit()
    conn.close()


# Test the functions
if __name__ == '__main__':
    create_table()
    add_book("Python Crash Course", "Eric Matthes", 2019, 4.5)
    books = get_all_books()
    for book in books:
        print(f"{book['title']} by {book['author']}")
```

---

## Quick Recap

- **SQLite** — Lightweight database stored in a file
- **`sqlite3.connect()`** — Connect to database
- **`cursor`** — Object to execute SQL commands
- **`CREATE TABLE`** — Create a new table
- **`INSERT INTO`** — Add data
- **`SELECT`** — Query data
- **`UPDATE`** — Modify data
- **`DELETE`** — Remove data
- **`conn.commit()`** — Save changes
- **Always close connections!**

---

## What's Next?

Ready for more? Continue to **[Lesson 15: Advanced Database Operations](15-advanced-database-operations.md)**! 🚀

---

**Your turn:** Try the library exercise! Add features like searching by year range or calculating average rating! 🗄️💛
