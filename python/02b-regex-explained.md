# Python Lesson 2b: Regex — Finding Patterns in Text

**← Back to [Lesson 2: Operations](02-operations-with-variables.md)**

---

## What is Regex?

**Plain English:** Regex (short for **regular expressions**) is a powerful way to **find patterns in text** — not exact matches, but *patterns*.

**Real-world analogy:** Think of a search in your email for all messages from `"@gmail.com"` addresses. You're not searching for one specific email — you're searching for a *pattern* (anything ending in `@gmail.com`). Regex does exactly that, but far more powerful.

Without regex, you'd have to check each character by hand:
```python
# Tedious without regex — check every character manually
email = "user@gmail.com"
at_index = None
for i, char in enumerate(email):
    if char == "@":
        at_index = i
        break
domain = email[at_index + 1:] if at_index else ""
print("gmail.com" in domain)   # True
```

With regex, it's one clean line:
```python
import re
email = "user@gmail.com"
result = re.search(r"@(\w+\.\w+)", email)
if result:
    print(result.group(1))  # gmail.com — extracted automatically!
```

---

## When to Use Regex (and When Not To)

**Reach for regex when:**
- You need to find a pattern in messy text (emails, phone numbers, postcodes)
- You want to **extract** specific parts of a string
- You need to **validate** that a string follows a format
- Simple `in` string checks aren't precise enough

**Stick to string methods when:**
- You just need to check if a substring exists: `"@" in email`
- You're doing simple splits: `text.split(",")`
- You're just checking character types: `char.isdigit()`, `char.isalpha()`

**Rule of thumb:** If a regex would be more complex than a string method, use the string method. Regex is powerful but can be hard to read — use the right tool for the job.

---

## First Steps: `re.search()`

Before you can search for a pattern, you need to tell Python to use regex. That's what `import re` does.

```python
import re
```

`re.search(pattern, string)` — finds the **first match** of a pattern anywhere in the string:

```python
# Find a phone number in messy text
message = "Call me on 07900 900123 or 0207 123 4567"
match = re.search(r"\d+", message)    # \d = "any digit"
print(match)         # <re.Match object> — not the text itself!
print(match.group()) # '07900' — the actual matched text
```

### What's that `r"..."` about?

The `r` before the quotes means **raw string** — it stops Python from interpreting backslashes in special ways. Always use `r"..."` for regex patterns. It's just how regex strings work in Python.

### `.group()` — Getting the Matched Text

`re.search()` returns a **Match object** (or `None` if nothing matched). You get the actual text with `.group()`:

```python
text = "The price is £49.99"

# Find the digits (price)
price = re.search(r"[\d.]+", text)    # \d = digit, . = literal dot
print(price.group())  # 49.99
```

---

## Basic Patterns

### Literals — Match Exact Characters

```python
# Find the word "python" in any text
text = "I love Python and python!"
match = re.search(r"python", text)
print(match.group())  # python (finds only the first one)
```

### `.` — Match Any Single Character

```python
# "c.t" means: c, then any character, then t
text = "cat cot cut"
match = re.search(r"c.t", text)
print(match.group())  # cat
```

### `\d` — Any Digit (0–9)
```python
text = "Room 42"
match = re.search(r"\d+", text)    # \d+ = one or more digits
print(match.group())  # 42
```

### `\w` — Any Word Character (letter, digit, underscore)
```python
text = "user_name123"
match = re.search(r"\w+", text)    # \w+ = one or more word characters
print(match.group())  # user_name123
```

### `\s` — Any Whitespace (space, tab, newline)
```python
text = "hello   world"
match = re.search(r"\s+", text)    # \s+ = one or more spaces
print(match.group())  # '   ' (three spaces)
```

### `\D`, `\W`, `\S` — The Opposites (NOT a digit, NOT a word char, NOT whitespace)
```python
text = "abc123xyz"
print(re.search(r"\D+", text).group())  # abc   (all the non-digits)
```

---

## Quantifiers — How Many Times?

| Symbol | Meaning |
|--------|---------|
| `+` | One or more times |
| `*` | Zero or more times |
| `?` | Zero or one time (optional) |
| `{3}` | Exactly 3 times |
| `{2,5}` | Between 2 and 5 times |

```python
# \d+ = one or more digits
re.search(r"\d+", "abc123def")     # '123'
re.search(r"\d+", "abcabcdef")     # None (no digits!)

# \d* = zero or more digits
re.search(r"\d*", "abc123def")     # '' (empty string — zero digits before 'a')

# {3} = exactly 3
re.search(r"\d{3}", "abc1234")     # '123' (finds first 3 digits)

# {2,4} = between 2 and 4
re.search(r"\d{2,4}", "abc123456") # '1234' (up to 4)
```

---

## Character Classes — Match One of Many

Square brackets `[ ]` mean "match ONE of these characters":

```python
# Find any vowel
text = "The quick brown fox"
vowels = re.findall(r"[aeiou]", text)  # findall returns ALL matches as a list
print(vowels)  # ['e', 'u', 'i', 'o']

# Find any digit (0-9)
re.findall(r"[0-9]", "abc123xyz")  # ['1', '2', '3']

# Find any lowercase letter
re.findall(r"[a-z]", "Hello World")  # ['e', 'l', 'l', 'o', 'o', 'r', 'l', 'd']

# Find any letter or digit
re.findall(r"[a-zA-Z0-9]", "!Abc?")   # ['A', 'b', 'c']
```

### Negated Character Classes — Match Anything EXCEPT

```python
# [^abc] = "anything except a, b, or c"
re.findall(r"[^aeiou]", "hello")   # ['h', 'l', 'l'] — consonants only
re.findall(r"[^0-9]", "a1b2c3")    # ['a', 'b', 'c'] — non-digits
```

---

## Grouping — Extract Parts of a Match

Parentheses `( )` **capture** a part of the pattern so you can extract it separately:

```python
# Extract the domain from an email
email = "szonja@gmail.com"
match = re.search(r"@(.+)", email)     # .+ = one or more of anything
print(match.group())      # @gmail.com  (the whole match)
print(match.group(1))     # gmail.com   (just the part in parentheses!)
```

This is *incredibly* useful. You can extract specific pieces without having to manually split the string afterward.

### Multiple Groups
```python
# Parse a date: "2024-05-08"
date_text = "2024-05-08"
match = re.search(r"(\d{4})-(\d{2})-(\d{2})", date_text)
print(match.group(1))  # '2024' — year
print(match.group(2))  # '05'   — month
print(match.group(3))  # '08'   — day
```

---

## `re.findall()` — Find All Matches

`re.findall()` returns a **list** of every match (not Match objects — just the strings):

```python
text = "My phone is 07900 900123 and his is 0207 123 4567"

# Find all phone numbers (sequences of digits)
all_numbers = re.findall(r"\d+", text)
print(all_numbers)  # ['07900', '900123', '0207', '123', '4567'] — all digit groups

# Find all words
all_words = re.findall(r"\w+", text)
print(all_words)    # ['My', 'phone', 'is', '07900', '900123', 'and', ...]
```

---

## `re.sub()` — Find and Replace

`re.sub(pattern, replacement, string)` — find all matches and replace them:

```python
text = "The cat sat on the cat"

# Replace all occurrences of "cat" with "dog"
result = re.sub(r"cat", "dog", text)
print(result)  # The dog sat on the dog

# Replace multiple spaces with a single space
messy = "Hello    World   !"
clean = re.sub(r"\s+", " ", messy)
print(clean)  # Hello World !
```

### Using Groups in Replacement
```python
# Swap first and last names: "Doe, John" → "John Doe"
name = "Doe, John"
formatted = re.sub(r"(\w+), (\w+)", r"\2 \1", name)
print(formatted)  # John Doe
# \1 and \2 refer back to the captured groups
```

---

## `re.split()` — Split by Pattern

Instead of splitting on a fixed character, split on a **pattern**:

```python
text = "one1two2three3four"

# Split on digits
parts = re.split(r"\d", text)
print(parts)  # ['one', 'two', 'three', 'four']

# Split on sequences of whitespace
messy = "apple\tbanana\ncherry   grape"
words = re.split(r"\s+", messy)
print(words)  # ['apple', 'banana', 'cherry', 'grape']
```

---

## Validation — Does the Whole String Match?

Sometimes you want to check if an entire string matches a pattern (e.g., for form validation). Use `re.fullmatch()`:

```python
# Check if it's a valid UK postcode (rough pattern)
def is_valid_postcode(code):
    return bool(re.fullmatch(r"[A-Z]{1,2}\d{1,2}[A-Z]?\s\d[A-Z]{2}", code))

print(is_valid_postcode("N7 0FQ"))    # True
print(is_valid_postcode("hello"))     # False
print(is_valid_postcode("N7"))        # False

# Check if it's a valid email
def is_valid_email(email):
    return bool(re.fullmatch(r"[\w.]+@[\w.]+\.\w+", email))

print(is_valid_email("szonja@gmail.com"))    # True
print(is_valid_email("hello@world"))         # False (no .com)
print(is_valid_email("not an email"))        # False
```

---

## Common Patterns to Memorise

| What you want | Pattern |
|---------------|---------|
| Any digit | `\d` |
| Any non-digit | `\D` |
| Any word character | `\w` |
| Whitespace | `\s` |
| One or more of X | `X+` |
| Zero or more of X | `X*` |
| Between n and m of X | `X{n,m}` |
| Start of string | `^` |
| End of string | `$` |
| Exact word (escaped) | `word` (literal) |
| Dot (literal) | `\.` |

---

## A Real Example: Phone Number Formatter

Let's build the phone number formatter from the exam challenges using regex:

```python
import re

def format_phone(raw_number):
    # Step 1: extract all digits only
    digits = re.findall(r"\d", raw_number)     # get every digit
    digits = "".join(digits)

    if len(digits) < 10:
        return "Invalid phone number"

    # Step 2: ensure it starts with country code (1)
    if len(digits) == 10:
        digits = "1" + digits

    # Step 3: format it
    area = digits[-10:-7]
    first = digits[-7:-4]
    last = digits[-4:]
    return f"+{digits[0]} ({area}) {first}-{last}"

print(format_phone("+1 (555) 123-4567"))   # +1 (555) 123-4567
print(format_phone("555-123-4567"))        # +1 (555) 123-4567
print(format_phone("abc"))                 # Invalid phone number
```

---

## Practice Exercise

**Scenario:** You're building a data-cleaning script for a messy customer database.

1. A record contains this text: `"ID: 12345, Email: szonja@gmail.com, Postcode: N7 0FQ"`
   Extract the **ID**, **email**, and **postcode** using regex groups.

2. You have a list of phone numbers in various formats: `"+44 7700 900123"`, `"07700900123"`, `"07700-900-123"`
   Extract all **digit sequences** from each. (You don't need to format them — just pull out the numbers.)

3. A product code looks like `"PROD-2024-XL"`. Validate it using `re.fullmatch()` — it must have:
   - `"PROD-"` literally
   - A 4-digit year
   - A dash
   - Any uppercase word (like `"XL"`, `"SALE"`, `"NEW"`)

4. **Challenge:** Given this messy text: `"Name:  John Smith  |  Age:  30  |  City:  London"`
   Use `re.sub()` to:
   - Remove all extra spaces (multiple spaces → single space)
   - Trim the leading/trailing spaces

5. **Challenge 2 (exam style!):** Write a function `extract_domain(email)` that uses regex groups to extract just the domain part of an email address (e.g. `"user@gmail.com"` → `"gmail.com"`). Use the pattern `@(.+)`.

**Try it yourself first!** Scroll down when ready.

---

## Solution

```python
import re

# 1. Extract ID, email, postcode using groups
record = "ID: 12345, Email: szonja@gmail.com, Postcode: N7 0FQ"
match = re.search(r"ID: (\d+), Email: (\S+), Postcode: (\S+)", record)
print(f"ID: {match.group(1)}, Email: {match.group(2)}, Postcode: {match.group(3)}")
# Output: ID: 12345, Email: szonja@gmail.com, Postcode: N7

# 2. Extract digit sequences from phone numbers
numbers = ["+44 7700 900123", "07700900123", "07700-900-123"]
for num in numbers:
    digits = re.findall(r"\d", num)
    print(f"{num} → {''.join(digits)}")
# +44 7700 900123 → 447700900123
# 07700900123 → 07700900123
# 07700-900-123 → 07700900123

# 3. Validate product code format
def valid_product_code(code):
    return bool(re.fullmatch(r"PROD-\d{4}-[A-Z]+", code))

print(valid_product_code("PROD-2024-XL"))     # True
print(valid_product_code("prod-2024-xl"))     # False (lowercase)
print(valid_product_code("PROD-24-XL"))       # False (only 2 digits)

# 4. Clean up messy text
messy = "Name:  John Smith  |  Age:  30  |  City:  London"
clean = re.sub(r"\s+", " ", messy).strip()    # \s+ → single space, then strip ends
print(clean)
# Output: Name: John Smith | Age: 30 | City: London

# 5. Extract domain from email
def extract_domain(email):
    match = re.search(r"@(.+)", email)
    if match:
        return match.group(1)
    return None

print(extract_domain("szonja@gmail.com"))    # gmail.com
print(extract_domain("arthur@outlook.com"))  # outlook.com
```

---

## Quick Recap

- **Import:** `import re`
- **`re.search(r"pattern", text)`** — find first match, returns Match object → use `.group()` to get text
- **`re.findall(r"pattern", text)`** — find ALL matches, returns a list of strings
- **`re.sub(r"pattern", "replacement", text)`** — find and replace
- **`re.split(r"pattern", text)`** — split by regex pattern
- **`re.fullmatch(r"pattern", text)`** — does the *whole* string match? (for validation)
- **`\d` = digit, `\w` = word char, `\s` = whitespace** — use `+` for one or more
- **`[abc]` = one of a, b, or c** — `[0-9]` = any digit
- **`( )` = capture group** — use `.group(1)` to extract the first captured part
- **`r"string"`** — always use raw strings for regex patterns

---

## What's Next?

Regex is your power tool for pattern matching in strings. Now let's look at another way to work with groups of data — **[Lesson 3: Lists](03-lists-explained.md)** where we'll store multiple items in order! 🚀

---