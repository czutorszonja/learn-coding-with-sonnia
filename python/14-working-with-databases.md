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
cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", 
               ("Szonja", "szonja@example.com"))
# Data persists even after program ends!
```

---

## MySQL vs SQLite

**MySQL** is a full database server — it runs separately and multiple applications can connect to it at once. This is what most real-world projects use.

**SQLite** stores everything in a single file on your computer — no server needed. Good for simple apps, but not what professionals use day-to-day.

**In this lesson:** We use **MySQL only** with the `mysql.connector` library. This is what you'll encounter in most real jobs.

---

## Installing MySQL Connector

```bash
pip install mysql-connector-python
```

---

## Your Database Config File

**Why?** Never write passwords directly in your code! Use a config file that Git ignores.

**`config.json`** (create this in your project folder):
```json
{
    "host": "localhost",
    "port": 3306,
    "user": "your_username",
    "password": "your_password",
    "database": "your_database"
}
```

**Add to `.gitignore`:**
```
config.json
```

**Load it in your code:**
```python
import json

def get_config():
    """Load database credentials from config.json."""
    with open("config.json", "r") as f:
        return json.load(f)
```

**Why this matters:** If you push code to GitHub with your password written in it, anyone can steal your data. The config file stays on your computer.

---

## Connecting to MySQL

```python
import mysql.connector
from mysql.connector import Error

def get_connection():
    """Create and return a database connection using config.json."""
    config = get_config()
    return mysql.connector.connect(**config)
```

**Use it:**
```python
conn = get_connection()
print("Connected to MySQL!")

cursor = conn.cursor()
cursor.execute("SELECT VERSION()")
result = cursor.fetchone()
print(f"MySQL Version: {result[0]}")

cursor.close()
conn.close()
```

**Why `cursor.close()` and `conn.close()`?** Connections use server resources. Always close them when you're done — like turning off the lights when you leave a room.

---

## Creating a Database

Before creating tables, you need a database to put them in:

```python
def create_database(database_name):
    """Create a new database if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"Database '{database_name}' ready!")
    except Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
```

**Why `IF NOT EXISTS`?** Without it, running the code again would give you an error — the database already exists. This way, it creates it if needed and does nothing if it's already there.

---

## Creating a Table

```python
def create_books_table():
    """Create the books table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("USE library_db")  # Switch to our database
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                year_published INT,
                rating DECIMAL(2,1),
                available BOOLEAN DEFAULT TRUE
            )
        """)
        conn.commit()  # SAVE the table creation
        print("Books table created!")
    except Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
```

**Key points:**
- `INT AUTO_INCREMENT PRIMARY KEY` — MySQL auto-generates unique IDs
- `VARCHAR(255)` — Text field with max 255 characters
- `DECIMAL(2,1)` — A number like 4.5 (2 digits total, 1 after decimal)
- `BOOLEAN DEFAULT TRUE` — True/False, defaults to True
- `conn.commit()` — **NEEDED** here because we're creating a table (writing to the database)

---

## Inserting Data

```python
def add_book(title, author, year_published, rating):
    """Add a new book to the library."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("USE library_db")
        query = """INSERT INTO books (title, author, year_published, rating)
                   VALUES (%s, %s, %s, %s)"""
        cursor.execute(query, (title, author, year_published, rating))
        conn.commit()  # SAVE the insert — THIS IS IMPORTANT!
        
        book_id = cursor.lastrowid  # Get the ID MySQL just generated
        print(f"Added '{title}' with ID: {book_id}")
        return book_id
    except Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        conn.close()
```

**Why `%s` placeholders?** This prevents SQL injection — a hacking technique where people try to break your database by inserting malicious code through form inputs. Parameterized queries make it impossible.

**Why `conn.commit()`?** INSERT writes data to the database. Without commit(), your insert vanishes when the connection closes — it's like saving a document but never clicking "Save".

---

## Inserting Multiple Books at Once (Bulk Insert)

What if you have 150 books? Calling `add_book()` 150 times works, but it's slow — each call opens a connection, inserts one row, and closes again.

Instead, use `executemany()` to insert many rows in one go:

```python
def add_books_bulk(books_list):
    """Add multiple books at once. books_list is a list of tuples."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("USE library_db")
        query = """INSERT INTO books (title, author, year_published, rating)
                   VALUES (%s, %s, %s, %s)"""
        
        # executemany does ALL the inserts in one call!
        cursor.executemany(query, books_list)
        conn.commit()  # Commit once for ALL inserts
        
        count = cursor.rowcount
        print(f"Added {count} books successfully!")
        return count
    except Error as err:
        print(f"Error: {err}")
        return 0
    finally:
        cursor.close()
        conn.close()
```

**How it works:**

```python
# Make a list of book data as tuples
books_to_add = [
    ("Fluent Python", "Luciano Ramalho", 2015, 5.0),
    ("Python Crash Course", "Eric Matthes", 2019, 4.5),
    ("Automate the Boring Stuff", "Al Sweigart", 2015, 4.8),
    ("Clean Code", "Robert Martin", 2008, 4.2),
    ("The Pragmatic Programmer", "David Thomas", 1999, 4.7),
]

# Insert all of them at once
add_books_bulk(books_to_add)
```

**The magic:** `executemany()` loops through your list and inserts each tuple. One connection, one commit, 150 rows added. Much faster than calling `add_book()` in a loop!

**When to use bulk insert:**
- Seeding a database with initial data
- Importing data from a CSV or API
- Any time you have more than a handful of records to add

---

## Querying Data

```python
def get_all_books():
    """Return all books in the library."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # Return rows as dictionaries
    
    try:
        cursor.execute("USE library_db")
        cursor.execute("SELECT * FROM books ORDER BY title")
        books = cursor.fetchall()
        return books
    except Error as err:
        print(f"Error: {err}")
        return []
    finally:
        cursor.close()
        conn.close()
```

**`dictionary=True`:** Without this, rows come back as tuples `("Book Title", "Author", 2020)`. With it, they come back as dictionaries `{"title": "Book Title", "author": "Author", ...}` — much easier to work with.

**No `conn.commit()`?** Correct! SELECT only reads data — it doesn't change anything. Commit is only for INSERT, UPDATE, DELETE, CREATE, DROP.

---

## Getting One Book

```python
def get_book_by_id(book_id):
    """Get a single book by its ID."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("USE library_db")
        cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()
        return book if book else None
    except Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        conn.close()
```

**`fetchone()` vs `fetchall()`:** fetchone() returns the first row (or None if no rows). fetchall() returns a list of all matching rows.

---

## Updating Data

```python
def update_book_rating(book_id, new_rating):
    """Update a book's rating."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("USE library_db")
        cursor.execute("UPDATE books SET rating = %s WHERE id = %s",
                      (new_rating, book_id))
        conn.commit()  # SAVE the update
        
        if cursor.rowcount > 0:
            print(f"Updated book {book_id} rating to {new_rating}")
            return True
        else:
            print(f"Book {book_id} not found")
            return False
    except Error as err:
        print(f"Error: {err}")
        return False
    finally:
        cursor.close()
        conn.close()
```

**`cursor.rowcount`:** Tells you how many rows were changed. Useful for checking if your update actually found something to update.

---

## Deleting Data

```python
def delete_book(book_id):
    """Delete a book from the library."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("USE library_db")
        cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
        conn.commit()  # SAVE the delete
        
        if cursor.rowcount > 0:
            print(f"Deleted book {book_id}")
            return True
        else:
            print(f"Book {book_id} not found")
            return False
    except Error as err:
        print(f"Error: {err}")
        return False
    finally:
        cursor.close()
        conn.close()
```

---

## Using TRY/FINALLY — Clean Resource Management

Notice how every function follows this pattern:

```python
def get_all_books():
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Do your database work here
        cursor.execute("USE library_db")
        cursor.execute("SELECT ...")
        results = cursor.fetchall()
        return results
    except Error as err:
        print(f"Error: {err}")
        return []
    finally:
        # This ALWAYS runs — even if there's an error
        cursor.close()
        conn.close()
```

**Why this matters:** If your code hits an error mid-function, the connection might never close. The `finally` block guarantees cleanup — error or not.

---

## The db_utils Pattern — One File to Rule Them All

Instead of repeating connection code in every file, put it all in `db_utils.py`:

**`db_utils.py`:**
```python
import mysql.connector
from mysql.connector import Error
import json

def get_config():
    """Load credentials from config.json."""
    with open("config.json", "r") as f:
        return json.load(f)

def get_connection():
    """Create and return a database connection."""
    return mysql.connector.connect(**get_config())

def get_all_books():
    """Return all books."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("USE library_db")
        cursor.execute("SELECT * FROM books ORDER BY title")
        return cursor.fetchall()
    except Error as err:
        print(f"Error: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def add_book(title, author, year_published, rating):
    """Add a book. Returns new book ID or None."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("USE library_db")
        cursor.execute("""INSERT INTO books (title, author, year_published, rating)
                          VALUES (%s, %s, %s, %s)""",
                      (title, author, year_published, rating))
        conn.commit()
        return cursor.lastrowid
    except Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

def delete_book(book_id):
    """Delete a book. Returns True/False."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("USE library_db")
        cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as err:
        print(f"Error: {err}")
        return False
    finally:
        cursor.close()
        conn.close()
```

**Use it anywhere in your project:**
```python
from db_utils import get_all_books, add_book, delete_book

# Get all books
books = get_all_books()
for book in books:
    print(f"{book['title']} by {book['author']}")

# Add a book
new_id = add_book("Fluent Python", "Luciano Ramalho", 2015, 5.0)
print(f"Added book with ID: {new_id}")

# Delete a book
deleted = delete_book(new_id)
print(f"Deleted: {deleted}")
```

---

## Quick Recap

| Action | SQL Command | Needs commit? |
|--------|-------------|----------------|
| Create table | `CREATE TABLE...` | ✅ Yes |
| Insert | `INSERT INTO...` | ✅ Yes |
| Read | `SELECT...` | ❌ No |
| Update | `UPDATE... SET...` | ✅ Yes |
| Delete | `DELETE FROM...` | ✅ Yes |

**Remember:**
- `%s` placeholders for safe queries
- `cursor.close()` + `conn.close()` always
- `try/finally` for guaranteed cleanup
- `mysql.connector.Error` for error handling

---

## Practice Exercise

**Scenario:** You're building a book tracking system for a personal library! Your cousin is learning programming and wants to track books they've read.

**Your task:**
1. Create a `config.json` file with your MySQL credentials
2. Create a `db_utils.py` file with these functions:
   - `get_connection()` — connects to MySQL using config
   - `create_database()` — creates `library_db` database if it doesn't exist
   - `create_books_table()` — creates a `books` table with: id, title, author, year_published, rating, available
3. Create these functions in `db_utils.py`:
   - `add_book(title, author, year_published, rating)` — inserts a book, returns the new ID
   - `get_all_books()` — returns all books as dictionaries
   - `get_books_by_author(author)` — returns books matching the author name
   - `update_book_rating(book_id, new_rating)` — updates rating, returns True/False
   - `delete_book(book_id)` — deletes a book by ID, returns True/False
   - `search_books(keyword)` — returns books where title OR author contains the keyword
4. Create a `main.py` that:
   - Sets up the database and table
   - Adds 3 books of your choice
   - Prints all books
   - Updates one book's rating
   - Searches for books by keyword
   - Deletes one book
   - Prints all books again to show changes

**Example usage:**
```python
# From main.py
from db_utils import add_book, get_all_books, update_book_rating, search_books, delete_book

add_book("Python Crash Course", "Eric Matthes", 2019, 4.5)
add_book("Fluent Python", "Luciano Ramalho", 2015, 5.0)

books = get_all_books()
for book in books:
    print(f"{book['title']} by {book['author']} ({book['year_published']})")

update_book_rating(1, 5.0)

results = search_books("Python")
for book in results:
    print(f"Found: {book['title']}")

delete_book(2)
```

**Try it yourself first!** Solution below.

---

## Solution

**`config.json`:**
```json
{
    "host": "localhost",
    "port": 3306,
    "user": "szonja",
    "password": "your_password",
    "database": "library_db"
}
```

**`db_utils.py`:**
```python
import mysql.connector
from mysql.connector import Error
import json

def get_config():
    """Load database credentials from config.json."""
    with open("config.json", "r") as f:
        return json.load(f)

def get_connection():
    """Create and return a database connection."""
    return mysql.connector.connect(**get_config())

def create_database():
    """Create the library_db database if it doesn't exist."""
    # Connect WITHOUT specifying database — we need to create it first
    conn = mysql.connector.connect(
        host=get_config()["host"],
        user=get_config()["user"],
        password=get_config()["password"]
    )
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
        print("Database 'library_db' ready!")
    except Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def create_books_table():
    """Create the books table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("USE library_db")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                year_published INT,
                rating DECIMAL(2,1),
                available BOOLEAN DEFAULT TRUE
            )
        """)
        conn.commit()
        print("Books table ready!")
    except Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def add_book(title, author, year_published, rating):
    """Add a book. Returns the new book ID or None."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("USE library_db")
        cursor.execute("""INSERT INTO books (title, author, year_published, rating)
                          VALUES (%s, %s, %s, %s)""",
                      (title, author, year_published, rating))
        conn.commit()
        book_id = cursor.lastrowid
        print(f"Added '{title}' with ID: {book_id}")
        return book_id
    except Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_books():
    """Return all books as a list of dictionaries."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("USE library_db")
        cursor.execute("SELECT * FROM books ORDER BY title")
        return cursor.fetchall()
    except Error as err:
        print(f"Error: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_books_by_author(author):
    """Return all books by the given author."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("USE library_db")
        cursor.execute("SELECT * FROM books WHERE author LIKE %s ORDER BY title",
                      (f"%{author}%",))
        return cursor.fetchall()
    except Error as err:
        print(f"Error: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def update_book_rating(book_id, new_rating):
    """Update a book's rating. Returns True if found, False if not."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("USE library_db")
        cursor.execute("UPDATE books SET rating = %s WHERE id = %s",
                      (new_rating, book_id))
        conn.commit()
        return cursor.rowcount > 0
    except Error as err:
        print(f"Error: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_book(book_id):
    """Delete a book by ID. Returns True if found, False if not."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("USE library_db")
        cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as err:
        print(f"Error: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def search_books(keyword):
    """Search books by title or author containing the keyword."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("USE library_db")
        cursor.execute("""SELECT * FROM books 
                          WHERE title LIKE %s OR author LIKE %s
                          ORDER BY title""",
                      (f"%{keyword}%", f"%{keyword}%"))
        return cursor.fetchall()
    except Error as err:
        print(f"Error: {err}")
        return []
    finally:
        cursor.close()
        conn.close()
```

**`main.py`:**
```python
from db_utils import (
    create_database, create_books_table,
    add_book, get_all_books, get_books_by_author,
    update_book_rating, delete_book, search_books
)

def main():
    # Set up database and table
    print("Setting up database...")
    create_database()
    create_books_table()
    
    # Add some books
    print("\nAdding books...")
    book1_id = add_book("Python Crash Course", "Eric Matthes", 2019, 4.5)
    book2_id = add_book("Fluent Python", "Luciano Ramalho", 2015, 5.0)
    book3_id = add_book("Automate the Boring Stuff", "Al Sweigart", 2015, 4.8)
    
    # Get all books
    print("\nAll books:")
    books = get_all_books()
    for book in books:
        print(f"  {book['id']}: {book['title']} by {book['author']}")
    
    # Update a rating
    print(f"\nUpdating book {book1_id} rating to 5.0...")
    update_book_rating(book1_id, 5.0)
    
    # Search for books
    print("\nSearching for 'Python' books:")
    results = search_books("Python")
    for book in results:
        print(f"  {book['title']} by {book['author']}")
    
    # Delete a book
    print(f"\nDeleting book {book3_id}...")
    delete_book(book3_id)
    
    # Show remaining books
    print("\nRemaining books:")
    books = get_all_books()
    for book in books:
        print(f"  {book['id']}: {book['title']} by {book['author']}")

if __name__ == '__main__':
    main()
```

**Output:**
```
Setting up database...
Database 'library_db' ready!
Books table ready!

Adding books...
Added 'Python Crash Course' with ID: 1
Added 'Fluent Python' with ID: 2
Added 'Automate the Boring Stuff' with ID: 3

All books:
  1: Python Crash Course by Eric Matthes
  2: Fluent Python by Luciano Ramalho
  3: Automate the Boring Stuff by Al Sweigart

Updating book 1 rating to 5.0...

Searching for 'Python' books:
  1: Python Crash Course by Eric Matthes
  2: Fluent Python by Luciano Ramalho

Deleting book 3...

Remaining books:
  1: Python Crash Course by Eric Matthes
  2: Fluent Python by Luciano Ramalho
```

---

## What's Next?

Ready for more? Continue to **[Lesson 15: Advanced Database Operations](15-advanced-database-operations.md)**! 🚀

---

**Your turn:** Try the library exercise! Add features like searching by year range, calculating average ratings, or adding more columns to the books table! 🗄️💛