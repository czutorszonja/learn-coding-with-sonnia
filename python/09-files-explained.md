# Python Lesson 9: File Handling — Reading and Writing Files 📄

**← Back to [Lesson 8: Dictionaries](08-dictionaries-explained.md)**

---

## What is File Handling?

**Plain English:** File handling means reading from and writing to files on your computer using Python.

**Real-world analogy:** Think of a file like a notebook:
- You can **read** what's written in it
- You can **write** new content to it
- You can **append** (add to the end) without erasing what's already there

Python lets you do all of this with code!

---

## Why Use Files?

**Without files:**
```python
# Data disappears when program ends!
names = ["Alice", "Bob", "Charlie"]
print(names)
# When you run again, data is gone!
```

**With files:**
```python
# Data saves permanently!
with open("names.txt", "w") as f:
    f.write("Alice\n")
    f.write("Bob\n")
    f.write("Charlie\n")

# Next time you run, data is still there!
```

---

## Opening a File

Use the `open()` function:

```python
# Open a file for reading
file = open("example.txt", "r")

# Do something with the file
content = file.read()
print(content)

# Close the file
file.close()
```

**Key parts:**
- `"example.txt"` — the file name
- `"r"` — mode: "r" means read, "w" means write, "a" means append
- `file.close()` — always close files when done!

---

## The `with` Statement (Better Way!)

**Use this instead!** It automatically closes the file:

```python
with open("example.txt", "r") as file:
    content = file.read()
    print(content)
# File is automatically closed here!
```

**Why it's better:**
- No need to call `close()`
- File closes even if there's an error
- Cleaner code

---

## Reading Files

### Read the entire file:
```python
with open("example.txt", "r") as file:
    content = file.read()
    print(content)
```

### Read line by line:
```python
with open("example.txt", "r") as file:
    for line in file:
        print(line)
```

### Read all lines into a list:
```python
with open("example.txt", "r") as file:
    lines = file.readlines()
    print(lines)
# Output: ["Line 1\n", "Line 2\n", "Line 3\n"]
```

---

## Writing to Files

**Important:** Writing to a file **replaces** everything that was there!

```python
with open("example.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write("This is a new file.\n")
```

**Note:** `\n` creates a new line (like pressing Enter).

---

## Appending to Files

Use `"a"` mode to add to the end without deleting:

```python
# First write (creates file)
with open("diary.txt", "w") as file:
    file.write("Day 1: Started learning Python!\n")

# Append (adds to end)
with open("diary.txt", "a") as file:
    file.write("Day 2: Learned about loops!\n")
    file.write("Day 3: Now learning file handling!\n")
```

**Result:**
```
Day 1: Started learning Python!
Day 2: Learned about loops!
Day 3: Now learning file handling!
```

---

## File Modes

| Mode | Name | What it does |
|------|------|--------------|
| `"r"` | Read | Opens file for reading (default) |
| `"w"` | Write | Opens file for writing (overwrites!) |
| `"a"` | Append | Opens file for appending (adds to end) |
| `"r+"` | Read + Write | Opens for both reading and writing |

---

## Practice Exercise

**Scenario:** You're building a simple note-taking app!

**Your task:**
1. Create a function called `save_note` that takes two parameters: `filename` and `note`
2. The function should open the file in append mode and add the note
3. Create a function called `read_notes` that takes one parameter: `filename`
4. The function should read and return all notes from the file
5. Test it by saving a few notes and reading them back

**Try it yourself first!** Solution below.

---

## Solution

```python
def save_note(filename, note):
    """Save a note to a file."""
    with open(filename, "a") as file:
        file.write(note + "\n")
    print(f"Note saved to {filename}")

def read_notes(filename):
    """Read all notes from a file."""
    notes = []
    with open(filename, "r") as file:
        for line in file:
            notes.append(line.strip())
    return notes

# Test the functions
save_note("notes.txt", "Learn Python")
save_note("notes.txt", "Build something cool")
save_note("notes.txt", "Practice every day")

# Read and display notes
print("\nYour Notes:")
all_notes = read_notes("notes.txt")
for note in all_notes:
    print(f"- {note}")
```

**Output:**
```
Note saved to notes.txt
Note saved to notes.txt
Note saved to notes.txt

Your Notes:
- Learn Python
- Build something cool
- Practice every day
```

**Note:** `line.strip()` removes the newline character from each line!

---

## Quick Recap

- **`open()`** — opens a file
- **Modes:** `"r"` (read), `"w"` (write), `"a"` (append)
- **`file.read()`** — reads entire file
- **`file.readlines()`** — reads all lines into a list
- **`file.write()`** — writes to file
- **`with` statement** — automatically closes files
- **Always close files!** Or use `with`

---

## What's Next?

Ready for more? Continue to **[Lesson 10: Error Handling](10-error-handling.md)**! 🚀

---

**Your turn:** Try the note-taking exercise! Maybe add features like numbering notes or deleting notes! 📝💛
