# Python Lesson 11: File Handling — Reading and Writing Files 📁

**← Back to [Lesson 10: Sets Explained](10-sets-explained.md)**

---

## What is File Handling?

**Plain English:** File handling lets you read data from files and write data to files on your computer.

**Real-world analogy:** Think of files like documents in a filing cabinet:
- **Reading** a file = Taking out a document and reading it
- **Writing** to a file = Creating a new document or editing an existing one
- **Closing** a file = Putting the document back in the cabinet

---

## Why Use File Handling?

**Without files:**
```python
# Data is lost when the program ends!
names = ["Alice", "Bob", "Charlie"]
print(names)
```

**With files:**
```python
# Data is saved permanently!
with open("names.txt", "w") as f:
    f.write("Alice\n")
    f.write("Bob\n")
    f.write("Charlie\n")
```

Now the data persists even after the program ends!

---

## Opening a File

Use the `open()` function:

```python
# Open a file for reading
file = open("example.txt", "r")

# Do something with the file
content = file.read()
print(content)

# Close the file (IMPORTANT!)
file.close()
```

**Better way — using `with`:**
```python
# Automatically closes the file when done
with open("example.txt", "r") as file:
    content = file.read()
    print(content)
# File is automatically closed here!
```

**Why use `with`?**
- ✅ Automatically closes the file
- ✅ Handles errors gracefully
- ✅ Cleaner code

---

## File Modes

| Mode | Description | Creates file if not exists? |
|------|-------------|----------------------------|
| `"r"` | Read (default) | ❌ No (error if file doesn't exist) |
| `"w"` | Write | ✅ Yes (overwrites if exists!) |
| `"a"` | Append | ✅ Yes (adds to end) |
| `"r+"` | Read and write | ❌ No |
| `"b"` | Binary mode | - |

**Examples:**
```python
# Read a file
with open("data.txt", "r") as f:
    content = f.read()

# Write to a file (overwrites existing content!)
with open("data.txt", "w") as f:
    f.write("Hello, World!")

# Append to a file (adds to end)
with open("data.txt", "a") as f:
    f.write("\nAnother line!")
```

---

## Reading Files

### Read entire file with `.read()`

```python
with open("example.txt", "r") as file:
    content = file.read()
    print(content)
# Output: Entire file content as one string
```

### Read line by line with `.readline()`

```python
with open("example.txt", "r") as file:
    line1 = file.readline()
    line2 = file.readline()
    print(line1)
    print(line2)
```

### Read all lines with `.readlines()`

```python
with open("example.txt", "r") as file:
    lines = file.readlines()
    print(lines)
# Output: List of strings (one per line)
```

### Loop through file (BEST for large files)

```python
with open("example.txt", "r") as file:
    for line in file:
        print(line.strip())  # .strip() removes newline characters
```

---

## Writing to Files

### Write a single string

```python
with open("output.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write("This is line 2.\n")
```

### Write multiple lines with `.writelines()`

```python
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]

with open("output.txt", "w") as file:
    file.writelines(lines)
```

**Important:** `.writelines()` doesn't add newlines automatically!

---

## Working with Paths

### Using `pathlib` (Modern way)

```python
from pathlib import Path

# Create a Path object
file_path = Path("data/example.txt")

# Check if file exists
if file_path.exists():
    print("File exists!")

# Read file
content = file_path.read_text()
print(content)

# Write to file
file_path.write_text("New content!")
```

### Using `os` module (Traditional way)

```python
import os

# Check if file exists
if os.path.exists("data/example.txt"):
    print("File exists!")

# Get current working directory
cwd = os.getcwd()
print(f"Current directory: {cwd}")

# List files in directory
files = os.listdir(".")
print(files)
```

---

## Real-World Examples

### Example 1: Reading a Configuration File

```python
# config.txt contains:
# debug=true
# timeout=30

config = {}

with open("config.txt", "r") as file:
    for line in file:
        key, value = line.strip().split("=")
        config[key] = value

print(config)
# Output: {'debug': 'true', 'timeout': '30'}
```

### Example 2: Writing a Log File

```python
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("app.log", "a") as file:
        file.write(f"[{timestamp}] {message}\n")

# Usage
log_message("User logged in")
log_message("Data saved")
```

### Example 3: Processing a CSV File

```python
# data.csv contains:
# name,age,city
# Alice,30,London
# Bob,25,Paris

with open("data.csv", "r") as file:
    # Skip header
    next(file)
    
    for line in file:
        name, age, city = line.strip().split(",")
        print(f"{name} is {age} and lives in {city}")
```

**Output:**
```
Alice is 30 and lives in London
Bob is 25 and lives in Paris
```

---

## Error Handling with Files

Always handle potential errors:

```python
try:
    with open("nonexistent.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("File not found!")
except PermissionError:
    print("Permission denied!")
except Exception as e:
    print(f"An error occurred: {e}")
```

---

## Practice Exercise

### Scenario: You're managing a guest list file!

**Your task:**
1. Create a file called `guests.txt` with 5 guest names (one per line)
2. Read the file and print each guest name
3. Count and print the total number of guests
4. Append 2 more guests to the file
5. Read the file again and print the updated list
6. Print the new total count

**Try it yourself first!** Scroll down when ready.

---

## Solutions

### Solution 1: Manage a Guest List File

```python
# Step 1: Create file with 5 guests
with open("guests.txt", "w") as file:
    file.write("Alice\n")
    file.write("Bob\n")
    file.write("Charlie\n")
    file.write("Diana\n")
    file.write("Eve\n")

# Step 2: Read and print each guest
with open("guests.txt", "r") as file:
    guests = file.readlines()
    print("Guest list:")
    for guest in guests:
        print(guest.strip())

# Step 3: Count total guests
print(f"\nTotal guests: {len(guests)}")

# Step 4: Append 2 more guests
with open("guests.txt", "a") as file:
    file.write("Frank\n")
    file.write("Grace\n")

# Step 5: Read updated list
with open("guests.txt", "r") as file:
    updated_guests = file.readlines()
    print("\nUpdated guest list:")
    for guest in updated_guests:
        print(guest.strip())

# Step 6: Print new total
print(f"\nNew total: {len(updated_guests)}")
```

**Output:**
```
Guest list:
Alice
Bob
Charlie
Diana
Eve

Total guests: 5

Updated guest list:
Alice
Bob
Charlie
Diana
Eve
Frank
Grace

New total: 7
```

---

## Quick Recap

- **`open()`** — Open a file
- **`with` statement** — Automatically closes files
- **File modes:** `"r"` (read), `"w"` (write), `"a"` (append)
- **`.read()`** — Read entire file
- **`.readline()`** — Read one line
- **`.readlines()`** — Read all lines into a list
- **`.write()`** — Write to a file
- **`.writelines()`** — Write multiple lines
- **`pathlib`** — Modern way to work with file paths
- **Error handling** — Always handle `FileNotFoundError`!

---

## What's Next?

Ready for more? Continue to **[Lesson 12: Error Handling and Debugging](12-error-handling.md)** — learn to handle errors gracefully and debug your code! 🐛
