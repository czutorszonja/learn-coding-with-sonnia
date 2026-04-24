# Python Lesson 16: Regular Expressions (Regex) 🔍

**← Back to [Lesson 15: Building Your Own API](15-building-api.md)**

---

## What are Regular Expressions?

**Plain English:** Regular expressions (regex) are patterns used to match text.

**Real-world analogy:** Think of regex like a search feature with superpowers:
- **Normal search** = Find exact word "cat"
- **Regex search** = Find any word that matches a pattern (e.g., 3-letter words ending in "t")

---

## Why Use Regex?

- Validate email addresses, phone numbers, passwords
- Extract data from text (URLs, dates, prices)
- Search and replace with patterns
- Parse log files

**Examples:**
- Check if password is strong enough
- Extract all emails from a document
- Validate credit card format

---

## The `re` Module

Python has a built-in `re` module for regex:

```python
import re

text = "Hello, my name is Alice. My email is alice@example.com"

# Search for a pattern
match = re.search(r"Alice", text)

if match:
    print("Found it!")
```

**Important:** Always prefix regex patterns with `r` (raw string) — e.g., `r"pattern"`

---

## Basic Patterns

### Literal Characters

```python
import re

text = "The cat in the hat"

# Match "cat"
match = re.search(r"cat", text)
print(match.group())  # Output: cat
```

### Special Characters

| Character | Meaning | Example |
|-----------|---------|---------|
| `.` | Any character | `a.c` matches "abc", "adc", "a c" |
| `^` | Start of string | `^Hello` matches "Hello" at start |
| `$` | End of string | `world$` matches "world" at end |
| `*` | 0 or more occurrences | `ab*c` matches "ac", "abc", "abbc" |
| `+` | 1 or more occurrences | `ab+c` matches "abc", "abbc" (not "ac") |
| `?` | 0 or 1 occurrence | `ab?c` matches "ac" or "abc" |
| `[]` | Set of characters | `[abc]` matches "a", "b", or "c" |
| `|` | OR operator | `cat|dog` matches "cat" or "dog" |

---

## Character Classes

### Predefined Classes

| Pattern | Meaning |
|---------|---------|
| `\d` | Any digit (0-9) |
| `\D` | Any non-digit |
| `\w` | Any word character (a-z, A-Z, 0-9, _) |
| `\W` | Any non-word character |
| `\s` | Any whitespace (space, tab, newline) |
| `\S` | Any non-whitespace |

### Examples:

```python
import re

text = "Price: £50"

# Find any digit
match = re.search(r"\d", text)
print(match.group())  # Output: 5

# Find any word character
match = re.search(r"\w+", text)
print(match.group())  # Output: Price
```

---

## Quantifiers

| Pattern | Meaning |
|---------|---------|
| `{n}` | Exactly n times |
| `{n,}` | At least n times |
| `{n,m}` | Between n and m times |

### Examples:

```python
import re

# Match exactly 3 digits
re.search(r"\d{3}", "1234")  # Matches "123"

# Match 2-4 digits
re.search(r"\d{2,4}", "12345")  # Matches "1234"

# Match 1 or more digits
re.search(r"\d+", "abc123")  # Matches "123"
```

---

## Common Regex Patterns

### Email Validation

```python
import re

email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

email = "user@example.com"
match = re.search(email_pattern, email)

if match:
    print("Valid email!")
```

### Phone Number Validation

```python
import re

# UK phone number pattern
phone_pattern = r"^\+?44\d{10}$"

phone = "+447123456789"
match = re.search(phone_pattern, phone)

if match:
    print("Valid UK phone number!")
```

### Password Strength

```python
import re

# At least 8 chars, one uppercase, one lowercase, one digit
password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"

password = "Secure123"
match = re.search(password_pattern, password)

if match:
    print("Strong password!")
```

---

## Regex Methods

### `re.search()` — Find first match

```python
import re

text = "My phone is 123-456-7890"
match = re.search(r"\d{3}-\d{3}-\d{4}", text)

if match:
    print(f"Found: {match.group()}")  # Output: Found: 123-456-7890
```

### `re.findall()` — Find all matches

```python
import re

text = "Call me at 123-456-7890 or 098-765-4321"
matches = re.findall(r"\d{3}-\d{3}-\d{4}", text)

print(matches)  # Output: ['123-456-7890', '098-765-4321']
```

### `re.match()` — Match at start only

```python
import re

text = "Hello, World!"
match = re.match(r"Hello", text)

if match:
    print("Starts with Hello!")
```

### `re.sub()` — Replace matches

```python
import re

text = "I have 3 cats and 2 dogs"
result = re.sub(r"\d", "many", text)

print(result)  # Output: I have many cats and many dogs
```

### `re.split()` — Split by pattern

```python
import re

text = "apple,banana;orange|grape"
result = re.split(r"[,;|]", text)

print(result)  # Output: ['apple', 'banana', 'orange', 'grape']
```

---

## Groups and Capturing

### Basic Groups

```python
import re

text = "John Doe, Email: john@example.com"
pattern = r"(\w+) (\w+), Email: ([\w.]+@[\w.]+)"

match = re.search(pattern, text)

if match:
    print(f"First name: {match.group(1)}")  # John
    print(f"Last name: {match.group(2)}")   # Doe
    print(f"Email: {match.group(3)}")       # john@example.com
```

### Named Groups

```python
import re

text = "2024-01-15"
pattern = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"

match = re.search(pattern, text)

if match:
    print(f"Year: {match.group('year')}")
    print(f"Month: {match.group('month')}")
    print(f"Day: {match.group('day')}")
```

---

## Flags

### `re.IGNORECASE` — Case-insensitive matching

```python
import re

text = "Hello WORLD"
match = re.search(r"hello", text, re.IGNORECASE)

if match:
    print("Found 'hello' (case-insensitive)!")
```

### `re.MULTILINE` — Match each line separately

```python
import re

text = """First line
Second line
Third line"""

# Match pattern at start of each line
matches = re.findall(r"^Second", text, re.MULTILINE)
print(matches)  # Output: ['Second']
```

---

## Practice Exercise

### Scenario: You're analyzing a server log file!

**Your task:**
1. Import the `re` module
2. Create a text variable with log entries containing IP addresses, dates, and error codes
3. Use `re.findall()` to extract all IP addresses
4. Use `re.findall()` to extract all dates
5. Use `re.findall()` to extract all error codes
6. Print each category of findings separately
7. Count and print the total number of errors found

**Try it yourself first!** Scroll down when ready.

---

## Solutions

### Solution 1: Build a Log File Analyzer

```python
import re

# Sample log text
log_text = """
Server started at 2024-01-15
Connection from 192.168.1.100
ERROR: 404 - Page not found
Connection from 10.0.0.1
ERROR: 500 - Internal server error
Request completed on 2024-01-16
Connection from 192.168.1.101
ERROR: 403 - Forbidden
"""

# Find all IP addresses
ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", log_text)
print("IP Addresses found:")
for ip in ips:
    print(f"  {ip}")

# Find all dates
dates = re.findall(r"\d{4}-\d{2}-\d{2}", log_text)
print("\nDates found:")
for date in dates:
    print(f"  {date}")

# Find all error codes
errors = re.findall(r"ERROR: \d+", log_text)
print("\nErrors found:")
for error in errors:
    print(f"  {error}")

# Count total errors
print(f"\nTotal errors: {len(errors)}")
```

**Output:**
```
IP Addresses found:
  192.168.1.100
  10.0.0.1
  192.168.1.101

Dates found:
  2024-01-15
  2024-01-16

Errors found:
  ERROR: 404
  ERROR: 500
  ERROR: 403

Total errors: 3
```

---

## Quick Recap

- **Regex** = Patterns for matching text
- **`re` module** = Python's regex library
- **`re.search()`** — Find first match
- **`re.findall()`** — Find all matches
- **`re.sub()`** — Replace matches
- **Special characters** = `.`, `^`, `$`, `*`, `+`, `?`, `[]`, `|`
- **Character classes** = `\d`, `\w`, `\s` (and uppercase versions)
- **Quantifiers** = `{n}`, `{n,}`, `{n,m}`
- **Groups** = Capture parts of match with `()`
- **Flags** = `re.IGNORECASE`, `re.MULTILINE`

---

## What's Next?

Ready for more? Continue to **[Lesson 17: Virtual Environments and Packages](17-virtual-environments.md)** — learn to manage project dependencies and set up professional projects! 📦

---

