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
