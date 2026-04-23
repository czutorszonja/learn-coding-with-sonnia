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

## Practice Exercises

### Exercise 1: Read a File

**Scenario:** You have a file with a list of names!

**Your task:**
1. Create a file called `names.txt` with 5 names (one per line)
2. Write code to read the file
3. Print each name
4. Print the total number of names

**Try it yourself first!** Scroll down when ready.

---

### Exercise 2: Write a Diary Entry

**Scenario:** You want to save your thoughts to a file!

**Your task:**
1. Ask the user for their diary entry (use `input()`)
2. Get the current date and time
3. Save both to a file called `diary.txt` (append mode)
4. Confirm it was saved

**Hint:** Use `datetime.now()` to get the current time!

**Try it yourself first!** Scroll down when ready.

---

### Exercise 3: Copy a File

**Scenario:** You need to copy contents from one file to another!

**Your task:**
1. Create a file called `source.txt` with some text
2. Read the contents of `source.txt`
3. Write the contents to `destination.txt`
4. Print a success message

**Try it yourself first!** Scroll down when ready.

---

### Exercise 4: Count Words in a File

**Scenario:** You need to analyze a text file!

**Your task:**
1. Create a file called `story.txt` with a paragraph of text
2. Read the file
3. Count the total number of words
4. Count the total number of lines
5. Print the statistics

**Hint:** Use `.split()` to split text into words!

**Try it yourself first!** Scroll down when ready.

---

## Solutions

### Solution 1: Read a File

```python
# Read names from file
with open("names.txt", "r") as file:
    names = file.readlines()

# Print each name
print("Names in the file:")
for name in names:
    print(name.strip())

# Print total count
print(f"\nTotal names: {len(names)}")
```

**Output:**
```
Names in the file:
Alice
Bob
Charlie
Diana
Eve

Total names: 5
```

---

### Solution 2: Write a Diary Entry

```python
from datetime import datetime

# Get user input
entry = input("What's on your mind? ")

# Get current timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Write to file (append mode)
with open("diary.txt", "a") as file:
    file.write(f"[{timestamp}] {entry}\n")

print("Diary entry saved!")
```

**Output:**
```
What's on your mind? Today was a great day!
Diary entry saved!
```

---

### Solution 3: Copy a File

```python
# Read from source file
with open("source.txt", "r") as source:
    content = source.read()

# Write to destination file
with open("destination.txt", "w") as dest:
    dest.write(content)

print("File copied successfully!")
```

**Output:**
```
File copied successfully!
```

---

### Solution 4: Count Words in a File

```python
# Read the file
with open("story.txt", "r") as file:
    content = file.read()

# Count words and lines
words = content.split()
lines = content.splitlines()

print("File Statistics:")
print(f"Total words: {len(words)}")
print(f"Total lines: {len(lines)}")
```

**Output:**
```
File Statistics:
Total words: 42
Total lines: 3
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

---

**Your turn:** Try the exercises above! File handling is essential for real-world applications. Ask if you get stuck! 💛🌞
