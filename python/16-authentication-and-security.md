# Python Lesson 16: Authentication and Security — Keeping Data Safe 🔐

**← Back to [Lesson 15: Advanced Database Operations](15-advanced-database-operations.md)**

---

## What is Authentication?

**Plain English:** Authentication is verifying who someone is (like showing ID at a club).

**Real-world analogy:** Think of logging into email:
- You enter username and password
- System checks if they match
- If correct, you're in!
- If wrong, access denied!

Authentication protects user accounts!

---

## Why Hash Passwords?

**NEVER store passwords as plain text!**

**Bad way:**
```python
# DON'T DO THIS!
users = [
    {"username": "szonja", "password": "mypassword123"}
]
# If database is hacked, all passwords are exposed!
```

**Good way:**
```python
# Hash passwords before storing
import hashlib
password = "mypassword123"
hashed = hashlib.sha256(password.encode()).hexdigest()
# Store the hash, not the password!
```

**Hashing** converts passwords into random-looking strings that can't be reversed!

---

## Hashing Passwords

```python
import hashlib

def hash_password(password):
    """Hash a password for storing."""
    # Convert password to bytes and hash it
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return hashed

def verify_password(password, hashed):
    """Verify a password against a hash."""
    # Hash the input and compare to stored hash
    return hash_password(password) == hashed

# Example usage
password = "mypassword123"
hashed = hash_password(password)
print(f"Hashed: {hashed}")

# Verify
is_valid = verify_password("mypassword123", hashed)
print(f"Valid: {is_valid}")  # True

# Wrong password
is_valid = verify_password("wrongpassword", hashed)
print(f"Valid: {is_valid}")  # False
```

---

## Building a Login System

```python
import hashlib
import sqlite3

def hash_password(password):
    """Hash a password."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    """Create a new user."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    hashed = hash_password(password)
    
    cursor.execute('''
        INSERT INTO users (username, password) VALUES (?, ?)
    ''', (username, hashed))
    
    conn.commit()
    conn.close()

def login(username, password):
    """Authenticate a user."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Get user by username
    cursor.execute('''
        SELECT password FROM users WHERE username = ?
    ''', (username,))
    result = cursor.fetchone()
    
    if not result:
        return False  # User doesn't exist
    
    stored_hash = result[0]
    conn.close()
    
    # Verify password
    return hash_password(password) == stored_hash

# Test
create_user("szonja", "SecurePass123!")

if login("szonja", "SecurePass123!"):
    print("Login successful!")
else:
    print("Login failed!")
```

---

## Practice Exercise

**Scenario:** You're building a secure user registration and login system for a website!

**Your task:**
1. Create a database file called `users.db`
2. Create a `users` table with:
   - `id` (INTEGER PRIMARY KEY)
   - `username` (TEXT UNIQUE NOT NULL)
   - `password` (TEXT NOT NULL) — this will store the HASH
   - `email` (TEXT)
   - `created_at` (TEXT) — timestamp
3. Create functions:
   - `register_user(username, password, email)` — Register a new user (hash the password!)
   - `login_user(username, password)` — Authenticate user (return True/False)
   - `change_password(username, old_password, new_password)` — Change password (verify old first!)
   - `delete_user(username)` — Delete a user account
   - `get_all_users()` — Return all usernames (NOT passwords!)
4. Add validation:
   - Username must be at least 3 characters
   - Password must be at least 8 characters
   - Email must contain "@"
5. Test with multiple users

**Example usage:**
```python
# Register users
register_user("szonja", "SecurePass123!", "szonja@example.com")
register_user("arthur", "PythonRocks2024", "arthur@example.com")

# Login
if login_user("szonja", "SecurePass123!"):
    print("Login successful!")
else:
    print("Login failed!")

# Try wrong password
if login_user("szonja", "WrongPassword"):
    print("Login successful!")
else:
    print("Login failed!")  # This should print

# Change password
change_password("szonja", "SecurePass123!", "NewSecurePass456!")

# Get all users
users = get_all_users()
print("Registered users:")
for user in users:
    print(f"  - {user['username']}")
```

**Try it yourself first!** Solution below.

---

## Solution

```python
# auth_system.py

import hashlib
import sqlite3
from datetime import datetime


def get_connection():
    """Create database connection."""
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    """Create users table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            created_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()


def hash_password(password):
    """Hash a password."""
    return hashlib.sha256(password.encode()).hexdigest()


def validate_username(username):
    """Validate username."""
    return len(username) >= 3


def validate_password(password):
    """Validate password."""
    return len(password) >= 8


def validate_email(email):
    """Validate email."""
    return '@' in email


def register_user(username, password, email):
    """Register a new user."""
    # Validate inputs
    if not validate_username(username):
        return {"success": False, "error": "Username must be at least 3 characters"}
    
    if not validate_password(password):
        return {"success": False, "error": "Password must be at least 8 characters"}
    
    if not validate_email(email):
        return {"success": False, "error": "Invalid email format"}
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        hashed = hash_password(password)
        created_at = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO users (username, password, email, created_at)
            VALUES (?, ?, ?, ?)
        ''', (username, hashed, email, created_at))
        
        conn.commit()
        return {"success": True, "message": "User registered successfully"}
    
    except sqlite3.IntegrityError:
        return {"success": False, "error": "Username already exists"}
    
    finally:
        conn.close()


def login_user(username, password):
    """Authenticate a user."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT password FROM users WHERE username = ?
    ''', (username,))
    
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return False
    
    stored_hash = result['password']
    return hash_password(password) == stored_hash


def change_password(username, old_password, new_password):
    """Change user password."""
    if not validate_password(new_password):
        return {"success": False, "error": "New password must be at least 8 characters"}
    
    # Verify old password
    if not login_user(username, old_password):
        return {"success": False, "error": "Invalid credentials"}
    
    conn = get_connection()
    cursor = conn.cursor()
    
    hashed = hash_password(new_password)
    
    cursor.execute('''
        UPDATE users SET password = ? WHERE username = ?
    ''', (hashed, username))
    
    conn.commit()
    conn.close()
    
    return {"success": True, "message": "Password changed successfully"}


def delete_user(username):
    """Delete a user."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM users WHERE username = ?
    ''', (username,))
    
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return deleted


def get_all_users():
    """Get all usernames (not passwords!)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT username, email, created_at FROM users
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    return [dict(user) for user in results]


# Test the system
if __name__ == '__main__':
    create_table()
    
    print("=== User Registration ===")
    # Register users
    result = register_user("szonja", "SecurePass123!", "szonja@example.com")
    print(f"Register szonja: {result}")
    
    result = register_user("arthur", "PythonRocks2024", "arthur@example.com")
    print(f"Register arthur: {result}")
    
    # Try invalid registration
    result = register_user("ab", "short", "invalid")
    print(f"Register invalid: {result}")
    
    print("\n=== Login Tests ===")
    # Test login
    if login_user("szonja", "SecurePass123!"):
        print("szonja login: SUCCESS")
    else:
        print("szonja login: FAILED")
    
    # Test wrong password
    if login_user("szonja", "WrongPassword"):
        print("Wrong password login: SUCCESS (should be FAILED!)")
    else:
        print("Wrong password login: FAILED (correct!)")
    
    print("\n=== Change Password ===")
    result = change_password("szonja", "SecurePass123!", "NewSecurePass456!")
    print(f"Change password: {result}")
    
    # Test new password
    if login_user("szonja", "NewSecurePass456!"):
        print("Login with new password: SUCCESS")
    
    print("\n=== All Users ===")
    users = get_all_users()
    for user in users:
        print(f"  - {user['username']} ({user['email']})")
```

**To run:**
```bash
python auth_system.py
```

---

## Quick Recap

- **NEVER store plain passwords** — Always hash!
- **`hashlib.sha256()`** — Hash passwords
- **Salt** — Add random data before hashing (advanced)
- **Validation** — Check username, password, email format
- **Login** — Hash input and compare to stored hash
- **Security first** — Protect user data!

---

## What's Next?

Ready for more? Continue to **[Lesson 17: Deployment](17-deployment.md)**! 🚀

---

**Your turn:** Try the auth system exercise! Add features like password strength checking or login attempt limits! 🔐💛
