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

## Practice Exercises

### Exercise 1: Find All Numbers

**Scenario:** You need to extract all numbers from a text!

**Your task:**
1. Import the `re` module
2. Create a text string with several numbers in it
3. Use `re.findall()` to find all digits
4. Print the list of numbers found

**Try it yourself first!** Scroll down when ready.

---

### Exercise 2: Validate Email Address

**Scenario:** You need to check if an email is valid!

**Your task:**
1. Create a regex pattern for email validation
2. Test it with a valid email (e.g., "user@example.com")
3. Test it with an invalid email (e.g., "invalid-email")
4. Print whether each email is valid or not

**Try it yourself first!** Scroll down when ready.

---

### Exercise 3: Extract Dates

**Scenario:** You need to extract dates from a document!

**Your task:**
1. Create a text with dates in YYYY-MM-DD format
2. Use `re.findall()` to extract all dates
3. Print the list of dates found

**Try it yourself first!** Scroll down when ready.

---

### Exercise 4: Replace Sensitive Data

**Scenario:** You need to redact credit card numbers from text!

**Your task:**
1. Create a text with credit card numbers (16 digits)
2. Use `re.sub()` to replace card numbers with "****"
3. Print the redacted text

**Try it yourself first!** Scroll down when ready.

---

## Solutions

### Solution 1: Find All Numbers

```python
import re

text = "I have 3 apples, 5 oranges, and 10 bananas"

# Find all digits
numbers = re.findall(r"\d+", text)

print(numbers)  # Output: ['3', '5', '10']
```

---

### Solution 2: Validate Email Address

```python
import re

def validate_email(email):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(pattern, email)
    return match is not None

# Test with valid email
email1 = "user@example.com"
print(f"{email1}: {validate_email(email1)}")  # True

# Test with invalid email
email2 = "invalid-email"
print(f"{email2}: {validate_email(email2)}")  # False
```

---

### Solution 3: Extract Dates

```python
import re

text = """
Meeting scheduled for 2024-01-15
Follow-up on 2024-02-20
Deadline: 2024-03-30
"""

# Find all dates in YYYY-MM-DD format
dates = re.findall(r"\d{4}-\d{2}-\d{2}", text)

print(dates)  # Output: ['2024-01-15', '2024-02-20', '2024-03-30']
```

---

### Solution 4: Replace Sensitive Data

```python
import re

text = """
Customer paid with card 1234567890123456
Another card: 9876543210987654
"""

# Replace 16-digit card numbers with ****
redacted = re.sub(r"\d{16}", "****", text)

print(redacted)
# Output:
# Customer paid with card ****
# Another card: ****
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

**Your turn:** Try the exercises above! Regex is powerful for text processing. Ask if you get stuck! 💛🌞
