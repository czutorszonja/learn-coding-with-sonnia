# Exam Prep: Python Practice Challenges 🌞

**Your level:** You've completed Lessons 1–18. You're solid on fundamentals, functions, lists, strings, loops, conditionals, error handling, files, and APIs. This session is designed to mirror what could come up in your exam — written in the style of HackerRank/easy-to-medium challenges.

---

## How to Use This (Open-Book Exam)

Since this is an **open-book exam**, I've written each challenge to include:
- **Problem statement** — what you need to do
- **Starter code stub** — the function you'll fill in
- **Example input → expected output** — so you can verify your answer
- **🔖 Reference pattern** — the key concept/technique you can look up in the lesson files

The reference pattern tells you which lesson has the relevant technique. Go find it, copy the pattern, adapt it to the problem.

---

## Format of Each Challenge

```
## Challenge N: [Name]
**Topic:** [Category] | **Difficulty:** Easy / Medium

**Problem:**
[What the code should do]

**Starter code:**
```python
def solve():
    pass
```

**Examples:**
Input:  `3` → Output:  `3`
Input:  `hello` → Output:  `HELLO`

**🔖 Reference:** Lesson 3 (Lists) / Lesson 6 (Functions)
```

---

---

# 🔥 WARM-UP ROUND

---

## Challenge 1: Leap Year Checker
**Topic:** Conditionals | **Difficulty:** Easy

**Problem:**
Write a function `is_leap_year(year)` that returns `True` if the year is a leap year, `False` otherwise.

A year is a leap year if:
- It is divisible by 400, OR
- It is divisible by 4 AND not divisible by 100

**Starter code:**
```python
def is_leap_year(year):
    # your code here
    pass
```

**Examples:**
| Input | Output |
|-------|--------|
| 2000 | True (divisible by 400) |
| 1900 | False (divisible by 100 but not 400) |
| 2024 | True (divisible by 4, not by 100) |
| 2023 | False |

**🔖 Reference:** Lesson 5 — `if / elif / else` conditions

---

## Challenge 2: FizzBuzz
**Topic:** Loops + Conditionals | **Difficulty:** Easy

**Problem:**
Write a function `fizzbuzz(n)` that returns a list of strings for numbers 1 to n:
- `"Fizz"` for multiples of 3
- `"Buzz"` for multiples of 5
- `"FizzBuzz"` for multiples of both 3 and 5
- The number as a string otherwise

**Starter code:**
```python
def fizzbuzz(n):
    result = []
    # your code here
    return result
```

**Examples:**
`fizzbuzz(5)` → `['1', '2', 'Fizz', '4', 'Buzz']`
`fizzbuzz(15)` → `['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz']`

**🔖 Reference:** Lesson 4 (Loops) + Lesson 5 (Conditionals)

---

## Challenge 3: Sum of Even Numbers
**Topic:** Loops | **Difficulty:** Easy

**Problem:**
Write a function `sum_even(numbers)` that takes a list of numbers and returns the sum of all **even** numbers in the list.

**Starter code:**
```python
def sum_even(numbers):
    total = 0
    # your code here
    return total
```

**Examples:**
`sum_even([1, 2, 3, 4, 5, 6])` → `12`
`sum_even([1, 3, 5])` → `0`
`sum_even([10, 10, 10])` → `30`

**🔖 Reference:** Lesson 4 — `for` loops over lists

---

---

# 💬 STRING ROUND

---

## Challenge 4: Swap Case
**Topic:** Strings | **Difficulty:** Easy

**Problem:**
Write a function `swap_case(text)` that returns a new string where every lowercase letter becomes uppercase, and every uppercase letter becomes lowercase. Leave all other characters unchanged.

**Starter code:**
```python
def swap_case(text):
    result = ""
    # your code here
    return result
```

**Examples:**
`swap_case("Hello World")` → `"hELLO wORLD"`
`swap_case("Python 3.0")` → `"pYTHON 3.0"`
`swap_case("Sz")` → `"sZ"`

**🔖 Reference:** Lesson 2 — string `+` and `*`, f-strings

**💡 Hint:** Compare each character to its lowercase and uppercase version to tell which case it is:
```python
if char == char.lower() and char != char.upper():
    # it's lowercase — make it uppercase
    result += char.upper()
```

---

## Challenge 5: Count Word Occurrences
**Topic:** Strings | **Difficulty:** Easy

**Problem:**
Write a function `count_word(text, word)` that counts how many times `word` appears in `text`. The search should be **case-insensitive**.

**Starter code:**
```python
def count_word(text, word):
    # your code here
    pass
```

**Examples:**
`count_word("The cat sat on the mat", "the")` → `2`
`count_word("Hello hello HELLO", "hello")` → `3`
`count_word("apple apple apple", "banana")` → `0`

**🔖 Reference:** Lesson 2 — string methods, `str.lower()`, `str.count()`

**💡 Hint:** Convert both strings to lowercase before counting or searching.

---

## Challenge 6: Validate a Username
**Topic:** Strings + Conditionals | **Difficulty:** Easy

**Problem:**
Write a function `valid_username(username)` that returns `True` if the username is valid, `False` otherwise. A valid username:
- Is between 3 and 16 characters (inclusive)
- Contains only alphanumeric characters (letters or digits)
- Does not contain spaces

**Starter code:**
```python
def valid_username(username):
    # your code here
    pass
```

**Examples:**
`valid_username("szonja")` → `True`
`valid_username("Arthur123")` → `True`
`valid_username("ab")` → `False` (too short)
`valid_username("Arthur Drozdov")` → `False` (space)
`valid_username("szonja!")` → `False` (non-alphanumeric)

**🔖 Reference:** Lesson 2 — `str.isalnum()`, length with `len()`

---

---

# 📋 LIST ROUND

---

## Challenge 7: Second Largest Number
**Topic:** Lists | **Difficulty:** Easy

**Problem:**
Write a function `second_largest(numbers)` that returns the **second largest** distinct number in a list. The list will always have at least 2 distinct numbers.

**Starter code:**
```python
def second_largest(numbers):
    # your code here
    pass
```

**Examples:**
`second_largest([1, 2, 3, 4, 5])` → `4`
`second_largest([10, 20, 20, 30])` → `20` (distinct — duplicates are ignored)
`second_largest([5, 5])` → `5`
`second_largest([1, 3, 3, 7, 9, 9])` → `7`

**🔖 Reference:** Lesson 3 — `sorted()`, sets, list indexing

**💡 Hint:** Convert to `set()` to remove duplicates, then sort.

---

## Challenge 8: Filter Passing Grades
**Topic:** List Comprehensions | **Difficulty:** Easy

**Problem:**
Write a function `passing_grades(grades)` that takes a list of numeric grades (0–100) and returns only the grades that are **40 or above**, sorted in ascending order.

**Starter code:**
```python
def passing_grades(grades):
    # your code here
    pass
```

**Examples:**
`passing_grades([30, 45, 60, 35, 90])` → `[45, 60, 90]`
`passing_grades([10, 20, 30])` → `[]`
`passing_grades([100, 100, 40])` → `[40, 100, 100]`

**🔖 Reference:** Lesson 3 — list comprehensions with `if` filter

**💡 Hint:**
```python
# Basic list comprehension with a filter:
passing = [g for g in grades if g >= 40]
```

---

## Challenge 9: Merge Two Lists Into a Dictionary
**Topic:** Lists + Dictionaries | **Difficulty:** Medium

**Problem:**
Write a function `merge_to_dict(keys, values)` that takes two lists of equal length and returns a dictionary where each key from `keys` is paired with its corresponding value from `values`.

**Starter code:**
```python
def merge_to_dict(keys, values):
    # your code here
    pass
```

**Examples:**
`merge_to_dict(["name", "age", "city"], ["Szonja", "28", "London"])` → `{'name': 'Szonja', 'age': '28', 'city': 'London'}`
`merge_to_dict(["a", "b"], [1, 2])` → `{'a': 1, 'b': 2}`

**🔖 Reference:** Lesson 3 (Lists) + Lesson 8 (Dictionaries)

**💡 Hint:** Use `zip()` to iterate over both lists simultaneously:
```python
for key, value in zip(keys, values):
    result[key] = value
```

---

---

# ⚠️ ERROR HANDLING ROUND

---

## Challenge 10: Safe Division
**Topic:** Exceptions | **Difficulty:** Easy

**Problem:**
Write a function `safe_divide(a, b)` that divides `a` by `b`. If `b` is zero, return the string `"Cannot divide by zero"` instead of crashing.

**Starter code:**
```python
def safe_divide(a, b):
    # your code here
    pass
```

**Examples:**
`safe_divide(10, 2)` → `5`
`safe_divide(10, 3)` → `3.333...`
`safe_divide(10, 0)` → `"Cannot divide by zero"`
`safe_divide(0, 5)` → `0`

**🔖 Reference:** Lesson 10 — `try / except` blocks

**💡 Hint:**
```python
try:
    result = a / b
except ZeroDivisionError:
    return "Cannot divide by zero"
```

---

## Challenge 11: Validate and Parse Age
**Topic:** Exceptions + Conditionals | **Difficulty:** Medium

**Problem:**
Write a function `parse_age(age_input)` that:
- Attempts to convert `age_input` to an integer
- If it succeeds, validates the age is between 0 and 150 (inclusive) — return the integer if valid, or `"Invalid age"` if out of range
- If it fails to convert (e.g., the input is the string `"twenty"`), return `"Invalid input"`

**Starter code:**
```python
def parse_age(age_input):
    # your code here
    pass
```

**Examples:**
`parse_age(25)` → `25`
`parse_age("25")` → `25`
`parse_age("twenty")` → `"Invalid input"`
`parse_age(-5)` → `"Invalid age"`
`parse_age(200)` → `"Invalid age"`

**🔖 Reference:** Lesson 10 — `try / except ValueError`

---

---

# 📁 FILE ROUND

---

## Challenge 12: Count Lines in a File
**Topic:** File Handling | **Difficulty:** Easy

**Problem:**
Write a function `count_lines(filepath)` that returns the number of lines in a text file. If the file doesn't exist, return `-1`.

**Starter code:**
```python
def count_lines(filepath):
    # your code here
    pass
```

**🔖 Reference:** Lesson 9 — `try / except FileNotFoundError`, `open()`, `.readlines()`

---

## Challenge 13: Write and Read Students
**Topic:** File Handling + Strings | **Difficulty:** Medium

**Problem:**
Write a function `save_student_grades(filepath, data)` that writes student records to a CSV-style text file (one line per student in the format `name,grade`), and a function `load_student_grades(filepath)` that reads the file back and returns a list of dictionaries with `name` and `grade` keys.

`data` is a list of `{"name": "...", "grade": ...}` dictionaries.

**Starter code:**
```python
def save_student_grades(filepath, data):
    # your code here
    pass

def load_student_grades(filepath):
    # your code here
    pass
```

**🔖 Reference:** Lesson 9 — file `open()` with `w` and `r` modes, string `.split(",")`

---

---

# 🔧 PUTTING IT TOGETHER (Medium Challenges)

---

## Challenge 14: Word Frequency Counter
**Topic:** Strings + Dictionaries | **Difficulty:** Medium

**Problem:**
Write a function `word_frequency(sentence)` that takes a sentence and returns a dictionary of each word's frequency. Convert all words to lowercase and ignore punctuation (`.`, `!`, `?`, `,`).

**Starter code:**
```python
def word_frequency(sentence):
    # your code here
    pass
```

**Examples:**
`word_frequency("The cat sat on the mat.")` → `{'the': 2, 'cat': 1, 'sat': 1, 'on': 1, 'mat': 1}`
`word_frequency("hello HELLO Hello")` → `{'hello': 3}`

**🔖 Reference:** Lesson 8 (Dictionaries) + Lesson 2 (String methods)

**💡 Hint:** Use a dictionary to count: `counts[word] = counts.get(word, 0) + 1`

---

## Challenge 15: Phone Number Formatter
**Topic:** Strings + Functions | **Difficulty:** Medium

**Problem:**
Write a function `format_phone(raw_number)` that takes a string that may contain spaces, dashes, and parentheses — and extracts only the digits. Then format it as `+1 (XXX) XXX-XXXX` (assume a US number starting with digit `1`). If the extracted number has fewer than 10 digits, return `"Invalid phone number"`.

**Starter code:**
```python
def format_phone(raw_number):
    # your code here
    pass
```

**Examples:**
`format_phone("+1 (555) 123-4567")` → `"+1 (555) 123-4567"`
`format_phone("555-123-4567")` → `"+1 (555) 123-4567"`
`format_phone("abc")` → `"Invalid phone number"`

**🔖 Reference:** Lesson 2 (Strings) + Lesson 6 (Functions)

**💡 Hint:** Use `str.isdigit()` to filter digits, or a regex pattern (see Lesson 11 if you've covered APIs and regex).

---

## Challenge 16: Grade Statistics
**Topic:** Lists + Functions + Conditionals | **Difficulty:** Medium

**Problem:**
Write a function `grade_stats(grades)` that takes a list of numeric grades (0–100) and returns a dictionary with:
- `"passing"` — count of grades ≥ 40
- `"failing"` — count of grades < 40
- `"highest"` — the highest grade
- `"lowest"` — the lowest grade
- `"average"` — the average grade, rounded to 1 decimal place

**Starter code:**
```python
def grade_stats(grades):
    # your code here
    pass
```

**Examples:**
`grade_stats([30, 45, 60, 35, 90])` → `{'passing': 3, 'failing': 2, 'highest': 90, 'lowest': 30, 'average': 52.0}`
`grade_stats([100, 100, 100])` → `{'passing': 3, 'failing': 0, 'highest': 100, 'lowest': 100, 'average': 100.0}`

**🔖 Reference:** Lesson 3 (Lists) + Lesson 8 (Dictionaries) + Lesson 4 (Loops)

---

## Challenge 17: Password Strength Checker
**Topic:** Strings + Functions + Conditionals | **Difficulty:** Medium

**Problem:**
Write a function `password_strength(password)` that returns a score from 0 to 4:
- `0` — very weak (fails all criteria)
- `1` — weak (passes 1 criterion)
- `2` — fair (passes 2 criteria)
- `3` — strong (passes 3 criteria)
- `4` — very strong (passes all 4 criteria)

Criteria:
1. At least 8 characters
2. Contains at least one digit
3. Contains at least one uppercase letter
4. Contains at least one lowercase letter

**Starter code:**
```python
def password_strength(password):
    score = 0
    # your code here
    return score
```

**Examples:**
`password_strength("abc")` → `0`
`password_strength("password")` → `1` (lowercase only → criterion 3 and 4 but not 1 or 2 → wait, check yourself!)
`password_strength("Password1")` → `4` (all 4 criteria met)
`password_strength("password1")` → `3` (missing uppercase)

**🔖 Reference:** Lesson 16 (Auth/Security) — validation patterns

---

## Challenge 18: Build a Tiny Todo App
**Topic:** Everything combined | **Difficulty:** Medium–Hard

**Problem:**
Write a `TodoList` class (or just a set of functions) with these operations:

```python
def create_todo(title, priority="medium"):
    # Returns a todo dictionary with: title, priority, completed=False, created_at=timestamp

def mark_complete(todos, title):
    # Marks the first matching todo as completed=True

def filter_by_priority(todos, priority):
    # Returns all todos with that priority

def summary(todos):
    # Returns a string: "X total, Y completed, Z pending"
```

**Starter code:**
```python
from datetime import datetime

def create_todo(title, priority="medium"):
    pass

def mark_complete(todos, title):
    pass

def filter_by_priority(todos, priority):
    pass

def summary(todos):
    pass

# Test it:
todos = []
todos.append(create_todo("Revise loops", "high"))
todos.append(create_todo("Read error handling", "medium"))
todos.append(create_todo("Practice strings", "low"))
todos = mark_complete(todos, "Revise loops")

print(summary(todos))  # "3 total, 1 completed, 2 pending"
print(filter_by_priority(todos, "high"))  # [{"title": "Revise loops", ...}]
```

**🔖 Reference:** Lessons 3, 6 (functions), 8 (dicts), 16 (validation), 10 (error handling)

---

---

# 📊 QUICK REFERENCE — "What Do I Look Up?"

| Problem | Look Up |
|---------|---------|
| `is_leap_year` | Lesson 5 — if/elif/else |
| `fizzbuzz` | Lessons 4+5 — loops + conditionals |
| `sum_even` | Lesson 4 — for loops |
| `swap_case` | Lesson 2 — string methods |
| `count_word` | Lesson 2 — `str.count()`, `str.lower()` |
| `valid_username` | Lesson 2 — `str.isalnum()`, `len()` |
| `second_largest` | Lesson 3 — `sorted()`, `set()` |
| `passing_grades` | Lesson 3 — list comprehensions |
| `merge_to_dict` | Lessons 3+8 — `zip()`, dicts |
| `safe_divide` | Lesson 10 — `try/except ZeroDivisionError` |
| `parse_age` | Lesson 10 — `try/except ValueError` |
| `count_lines` | Lesson 9 — file handling, `FileNotFoundError` |
| `save/load_student_grades` | Lesson 9 — file read/write |
| `word_frequency` | Lesson 8 — dictionaries, `.get()` |
| `format_phone` | Lesson 2 — string slicing/methods |
| `grade_stats` | Lessons 3+4+8 — lists + dicts |
| `password_strength` | Lesson 16 — validation |
| `TodoList` | Everything combined! |

---

# ✅ Solutions

<details>
<summary>Click to reveal solutions — try the problems first!</summary>

## Challenge 1: Leap Year
```python
def is_leap_year(year):
    if year % 400 == 0:
        return True
    elif year % 4 == 0 and year % 100 != 0:
        return True
    else:
        return False
```

## Challenge 2: FizzBuzz
```python
def fizzbuzz(n):
    result = []
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result
```

## Challenge 3: Sum of Even Numbers
```python
def sum_even(numbers):
    return sum(n for n in numbers if n % 2 == 0)
    # Or verbose:
    # total = 0
    # for n in numbers:
    #     if n % 2 == 0:
    #         total += n
    # return total
```

## Challenge 4: Swap Case
```python
def swap_case(text):
    result = ""
    for char in text:
        if char.islower():
            result += char.upper()
        elif char.isupper():
            result += char.lower()
        else:
            result += char
    return result
    # Or one-liner: return text.swapcase()
```

## Challenge 5: Count Word Occurrences
```python
def count_word(text, word):
    return text.lower().count(word.lower())
    # Or manual:
    # text_lower = text.lower()
    # word_lower = word.lower()
    # words = text_lower.split()
    # return words.count(word_lower)
```

## Challenge 6: Valid Username
```python
def valid_username(username):
    if not (3 <= len(username) <= 16):
        return False
    if not username.isalnum():
        return False
    return True
```

## Challenge 7: Second Largest
```python
def second_largest(numbers):
    unique = set(numbers)
    sorted_nums = sorted(unique, reverse=True)
    return sorted_nums[1]
```

## Challenge 8: Filter Passing Grades
```python
def passing_grades(grades):
    return sorted([g for g in grades if g >= 40])
```

## Challenge 9: Merge to Dictionary
```python
def merge_to_dict(keys, values):
    return dict(zip(keys, values))
    # Or manual:
    # result = {}
    # for key, value in zip(keys, values):
    #     result[key] = value
    # return result
```

## Challenge 10: Safe Division
```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"
```

## Challenge 11: Validate and Parse Age
```python
def parse_age(age_input):
    try:
        age = int(age_input)
    except (ValueError, TypeError):
        return "Invalid input"
    if 0 <= age <= 150:
        return age
    else:
        return "Invalid age"
```

## Challenge 12: Count Lines in File
```python
def count_lines(filepath):
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
        return len(lines)
    except FileNotFoundError:
        return -1
```

## Challenge 13: Student Grades File
```python
def save_student_grades(filepath, data):
    with open(filepath, "w") as f:
        for student in data:
            line = f"{student['name']},{student['grade']}\n"
            f.write(line)

def load_student_grades(filepath):
    todos = []
    with open(filepath, "r") as f:
        for line in f:
            name, grade = line.strip().split(",")
            todos.append({"name": name, "grade": int(grade)})
    return todos
```

## Challenge 14: Word Frequency
```python
def word_frequency(sentence):
    # Remove punctuation
    for punct in ".,!?":
        sentence = sentence.replace(punct, "")
    words = sentence.lower().split()
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts
```

## Challenge 15: Phone Formatter
```python
def format_phone(raw_number):
    digits = "".join(c for c in raw_number if c.isdigit())
    if len(digits) < 10:
        return "Invalid phone number"
    if len(digits) == 10:
        digits = "1" + digits  # add country code
    area = digits[-10:-7]
    first = digits[-7:-4]
    last = digits[-4:]
    return f"+{digits[0]} ({area}) {first}-{last}"
```

## Challenge 16: Grade Statistics
```python
def grade_stats(grades):
    return {
        "passing": sum(1 for g in grades if g >= 40),
        "failing": sum(1 for g in grades if g < 40),
        "highest": max(grades),
        "lowest": min(grades),
        "average": round(sum(grades) / len(grades), 1)
    }
```

## Challenge 17: Password Strength
```python
def password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    return score
```

## Challenge 18: Tiny Todo App
```python
from datetime import datetime

def create_todo(title, priority="medium"):
    return {
        "title": title,
        "priority": priority,
        "completed": False,
        "created_at": datetime.now().isoformat()
    }

def mark_complete(todos, title):
    for todo in todos:
        if todo["title"] == title:
            todo["completed"] = True
            break
    return todos

def filter_by_priority(todos, priority):
    return [t for t in todos if t["priority"] == priority]

def summary(todos):
    total = len(todos)
    completed = sum(1 for t in todos if t["completed"])
    pending = total - completed
    return f"{total} total, {completed} completed, {pending} pending"
```

</details>

---

Good luck, Szonja! You've got all the tools — the exam just wants to see you use them. 💛