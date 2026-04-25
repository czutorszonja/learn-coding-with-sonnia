# Python Lesson 12: Testing Your Code — Making Sure It Works ✅

**← Back to [Lesson 11: Working with APIs](11-working-with-apis.md)**

---

## What is Testing?

**Plain English:** Testing means running your code with known inputs to check if it produces the expected outputs.

**Real-world analogy:** Imagine you're a chef:
- You taste your food before serving it
- You check if it has the right ingredients
- You make sure it's cooked properly

Testing is "tasting" your code before giving it to users!

---

## Why Test Your Code?

**Without testing:**
```python
# You manually test every time
result = add(2, 3)
print(result)  # Is 5 correct? Did I type it right?

# Change something? Test everything again manually!
```

**With testing:**
```python
# Automated tests run in seconds
def test_add():
    assert add(2, 3) == 5
    assert add(0, 0) == 0
    assert add(-1, 1) == 0

# Run all tests with one command!
```

**Benefits:**
- Catches bugs early
- Saves time (no manual testing)
- Gives confidence to make changes
- Documents what your code should do

---

## What is `pytest`?

**pytest** is a Python testing framework that makes writing tests simple.

**Install it:**
```bash
pip install pytest
```

**Run tests:**
```bash
pytest
```

---

## Writing Your First Test

**Test file naming:** Start with `test_` or end with `_test.py`

```python
# test_calculator.py

def add(a, b):
    """Add two numbers."""
    return a + b

def test_add():
    """Test that add function works correctly."""
    result = add(2, 3)
    assert result == 5
```

**Key parts:**
- Test function name starts with `test_`
- `assert` checks if something is true
- If assertion fails, test fails

---

## Understanding `assert`

**`assert`** checks if a condition is true:

```python
assert 2 + 2 == 4  # Passes (no output)
assert 2 + 2 == 5  # Fails (AssertionError!)
```

**If assertion fails:**
```
E   assert 4 == 5
```

**You can add custom messages:**
```python
result = add(2, 3)
assert result == 5, f"Expected 5, but got {result}"
```

---

## Running Tests

**Run all tests:**
```bash
pytest
```

**Run with details:**
```bash
pytest -v  # -v means verbose
```

**Output:**
```
============================= test session starts =============================
collected 2 items

test_calculator.py::test_add PASSED                                      [ 50%]
test_calculator.py::test_subtract PASSED                                 [100%]

============================== 2 passed in 0.05s ==============================
```

**Test results:**
- `PASSED` ✅ — Test succeeded
- `FAILED` ❌ — Test failed (check the error message)

---

## Testing Edge Cases

**Edge cases** are unusual inputs that might break your code:

```python
# test_calculator.py

def test_add_positive_numbers():
    """Test adding positive numbers."""
    assert add(2, 3) == 5

def test_add_zeros():
    """Test adding zeros (edge case)."""
    assert add(0, 0) == 0

def test_add_negative_numbers():
    """Test adding negative numbers."""
    assert add(-2, -3) == -5

def test_multiply_by_zero():
    """Test multiplying by zero."""
    assert multiply(5, 0) == 0
```

**Common edge cases:**
- Zero values: `add(0, 0)`
- Negative numbers: `add(-5, -3)`
- Empty strings: `greet("")`
- Empty lists: `sum_list([])`
- Very large numbers: `multiply(1000000, 1000000)`

---

## Testing Functions That Raise Errors

Some functions should raise errors for invalid input:

```python
# calculator.py
def divide(a, b):
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**Test it:**
```python
# test_calculator.py
import pytest

def test_divide_by_zero():
    """Test that dividing by zero raises an error."""
    with pytest.raises(ValueError):
        divide(10, 0)
```

**What it does:**
- Test passes if `ValueError` is raised
- Test fails if no error is raised

---

## Organising Tests

**Keep tests near your code:**
```
my_project/
├── calculator.py
├── test_calculator.py
├── utils.py
└── test_utils.py
```

**One test file per module:**
- `calculator.py` → `test_calculator.py`
- `utils.py` → `test_utils.py`

---

## Practice Exercise

**Scenario:** You've built a string utility library, and now you need to write tests for it!

**Your task:**
1. Create a file called `test_string_utils.py`
2. Write tests for these functions:
   - `test_reverse_string` — Test that `reverse_string("hello")` returns `"olleh"`
   - `test_is_palindrome` — Test that `is_palindrome("racecar")` returns `True`
   - `test_count_words` — Test that `count_words("Hello world")` returns `2`
   - `test_reverse_string_empty` — Test edge case: empty string returns empty string
   - `test_is_palindrome_sentence` — Test with a sentence (ignore spaces and case)
3. Run the tests with `pytest -v`
4. Fix any failing tests

**Try it yourself first!** Solution below.

---

## Solution

```python
# test_string_utils.py

import pytest
from string_utils import reverse_string, is_palindrome, count_words


def test_reverse_string():
    """Test reversing a string."""
    result = reverse_string("hello")
    assert result == "olleh"


def test_reverse_string_empty():
    """Test reversing an empty string (edge case)."""
    result = reverse_string("")
    assert result == ""


def test_is_palindrome():
    """Test palindrome detection."""
    result = is_palindrome("racecar")
    assert result == True


def test_is_palindrome_sentence():
    """Test palindrome with sentence (ignore spaces and case)."""
    result = is_palindrome("A man a plan a canal Panama")
    assert result == True


def test_count_words():
    """Test word counting."""
    result = count_words("Hello world")
    assert result == 2


def test_count_words_empty():
    """Test counting words in empty string."""
    result = count_words("")
    assert result == 0
```

**To run the tests:**
```bash
# First, create string_utils.py with the functions
# Then run:
pytest test_string_utils.py -v
```

**Expected output:**
```
============================= test session starts =============================
collected 6 items

test_string_utils.py::test_reverse_string PASSED                         [ 16%]
test_string_utils.py::test_reverse_string_empty PASSED                   [ 33%]
test_string_utils.py::test_is_palindrome PASSED                          [ 50%]
test_string_utils.py::test_is_palindrome_sentence PASSED                 [ 66%]
test_string_utils.py::test_count_words PASSED                            [ 83%]
test_string_utils.py::test_count_words_empty PASSED                      [100%]

============================== 6 passed in 0.03s ==============================
```

---

## Quick Recap

- **Testing** — Running code with known inputs to verify outputs
- **pytest** — Python testing framework
- **Test functions** — Start with `test_`
- **`assert`** — Checks if condition is true
- **Edge cases** — Test unusual inputs (zeros, negatives, empty values)
- **`pytest.raises()`** — Test that errors are raised
- **Run tests:** `pytest` or `pytest -v`

---

## What's Next?

Ready for more? Continue to **[Lesson 13: Building Your Own API](13-building-your-own-api.md)**! 🚀

---

**Your turn:** Try the string utils exercise! Then write tests for your own functions from previous lessons! ✅💛
