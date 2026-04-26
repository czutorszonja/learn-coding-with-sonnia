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

## Manual Testing vs Automated Testing

### Manual Testing (using `print()`)

**What it is:** Running your code and checking output with `print()` statements.

**Example:**
```python
result = add(2, 3)
print(f"Result: {result}")  # You look at output and decide if it's right
```

**When to use:**
- ✅ Quick experiments while learning
- ✅ Exploring how a function behaves
- ✅ Debugging (temporarily adding print statements)

**Pros:** Simple, no setup required
**Cons:** Slow, error-prone, not reusable

---

### Automated Testing (using `assert` and `pytest`)

**What it is:** Writing code that checks if your code works correctly.

**Example:**
```python
def test_add():
    assert add(2, 3) == 5  # pytest checks automatically!
```

**When to use:**
- ✅ Code that will be used repeatedly
- ✅ Projects that will change over time
- ✅ Sharing code with others
- ✅ Professional development

**Pros:** Fast, reliable, reusable
**Cons:** Takes time to write, requires learning pytest

**Key insight:** `print()` is for **you** (while coding). `assert` is for **the computer** (to check automatically).

---

## pytest Basics

### What is pytest?

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

### Writing Your First Test

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

### Understanding `assert`

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

**Important:** Don't add extra `if` checks after `assert` — it's redundant!

---

### Running Tests

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

### Reading Error Messages

When a test fails, pytest shows you exactly what went wrong:

**Error message:**
```
____________________ test_fahrenheit_to_celsius_freezing _____________________

def test_fahrenheit_to_celsius_freezing():
    result = fahrenheit_to_celsius(32)
>   assert result == 0, f"Expected 0, got {result}"
E   AssertionError: Expected 0, got -17.77777777777778
E   assert -17.77777777777778 == 0

test_temperature.py:15: AssertionError
```

**How to read this:**
1. **Test name:** Which test failed
2. **Line with `>`:** The exact line that failed
3. **`E AssertionError`:** What you expected vs. what you got
4. **Bottom line:** File and line number

---

## Testing Best Practices

### Edge Cases

**Edge cases** are unusual inputs that might break your code:

```python
def test_add_zeros():
    """Test adding zeros (edge case)."""
    assert add(0, 0) == 0

def test_add_negative_numbers():
    """Test adding negative numbers."""
    assert add(-2, -3) == -5
```

**Common edge cases:**
- Zero values: `add(0, 0)`
- Negative numbers: `add(-5, -3)`
- Empty strings: `greet("")`
- Empty lists: `sum_list([])`
- Very large numbers: `multiply(1000000, 1000000)`

---

### Functions with Default Parameters

Some functions have optional parameters with default values:

```python
def is_freezing(temp, unit="celsius"):
    if unit == "celsius":
        return temp <= 0
```

**Test both the default AND explicit values:**

```python
def test_is_freezing_default():
    """Test default parameter (celsius)."""
    assert is_freezing(0) == True

def test_is_freezing_celsius():
    """Test explicit celsius parameter."""
    assert is_freezing(0, "celsius") == True
```

**Why test both?** Default parameter might have a bug!

---

### Functions That Raise Errors

Some functions should raise errors for invalid input:

```python
def divide(a, b):
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**Test it:**
```python
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

### Organising Tests

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

**Test file naming:**
- Start with `test_` (e.g., `test_calculator.py`)
- OR end with `_test.py` (e.g., `calculator_test.py`)

---

### The Testing Workflow: Red → Green → Refactor

Professional developers follow a pattern called **"Red-Green-Refactor"**:

1. **🔴 Red:** Write a test that fails (because the code is buggy)
2. **🟢 Green:** Fix the code to make the test pass
3. **🔵 Refactor:** Clean up the code (optional)

**Example:**

**Step 1: Write test (RED - fails):**
```python
def test_fahrenheit_to_celsius_freezing():
    result = fahrenheit_to_celsius(32)
    assert result == 0, f"Expected 0, got {result}"
```

Run it:
```bash
pytest test_temperature.py -v
```

Output:
```
FAILED test_temperature.py::test_fahrenheit_to_celsius_freezing
AssertionError: Expected 0, got -17.77777777777778
```

**Step 2: Fix code (GREEN - passes):**
```python
def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9  # Added parentheses!
```

Run tests again:
```bash
pytest test_temperature.py -v
```

Output:
```
PASSED test_temperature.py::test_fahrenheit_to_celsius_freezing
```

**Step 3: Refactor (optional):**
- Clean up variable names
- Add comments
- Remove duplication

---

## Alternative: unittest Framework

### What is unittest?

**unittest** is Python's built-in testing framework (no installation needed!). It uses a class-based approach.

**pytest style:**
```python
def test_add():
    assert add(2, 3) == 5
```

**unittest style:**
```python
import unittest

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
```

---

### Why Does unittest Require Classes?

**unittest** uses an object-oriented approach because:
1. **Test grouping:** Related tests are grouped in one class
2. **Setup/teardown:** Common setup code runs before each test
3. **Inheritance:** Test classes inherit from `unittest.TestCase`
4. **Test discovery:** unittest finds all `test_*` methods in classes

**Example with setup:**
```python
import unittest

class TestCalculator(unittest.TestCase):
    def setUp(self):
        """Runs before EACH test method."""
        self.calc = Calculator()
    
    def tearDown(self):
        """Runs after EACH test method."""
        pass
    
    def test_add(self):
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)
```

**`setUp` and `tearDown`:**
- `setUp()` — Runs before each test (prepare data, connections, etc.)
- `tearDown()` — Runs after each test (clean up, close files, etc.)

---

### Running unittest Tests

**Method 1: Command line**
```bash
python -m unittest test_calculator.py
```

**Method 2: With `unittest.main()`**
```python
import unittest

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

if __name__ == "__main__":
    unittest.main()
```

**Run it:**
```bash
python test_calculator.py
```

**What `if __name__ == "__main__":` does:**
- Checks if the file is being run directly (not imported)
- If yes, runs `unittest.main()` which discovers and runs all tests
- This pattern allows the file to be both runnable AND importable

**Output:**
```
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
```

---

### unittest Test Methods Reference

| Method | Checks | Example |
|--------|--------|---------|
| `assertEqual(a, b)` | `a == b` | `self.assertEqual(add(2, 3), 5)` |
| `assertNotEqual(a, b)` | `a != b` | `self.assertNotEqual(x, y)` |
| `assertTrue(x)` | `x is True` | `self.assertTrue(is_valid)` |
| `assertFalse(x)` | `x is False` | `self.assertFalse(is_error)` |
| `assertIsNone(x)` | `x is None` | `self.assertIsNone(result)` |
| `assertIsNotNone(x)` | `x is not None` | `self.assertIsNotNone(result)` |
| `assertIn(a, b)` | `a in b` | `self.assertIn(item, list)` |
| `assertNotIn(a, b)` | `a not in b` | `self.assertNotIn(item, list)` |
| `assertRaises(error)` | Exception raised | `with self.assertRaises(ValueError):` |

---

### pytest vs unittest — Comparison

| Feature | pytest | unittest |
|---------|--------|----------|
| **Installation** | `pip install pytest` | Built into Python |
| **Test structure** | Functions | Classes required |
| **Syntax** | `assert x == y` | `self.assertEqual(x, y)` |
| **Setup/teardown** | `@pytest.fixture` | `setUp()` / `tearDown()` |
| **Learning curve** | Gentle | Steeper (OOP required) |
| **Best for** | Modern Python projects | Enterprise, education |

**Industry trend:** Most modern Python projects use **pytest**, but unittest is still widely used in enterprise and education!

---

### Choosing the Right Approach

**For learning Python:**
- Start with `print()` for exploration
- Learn `assert` for simple checks
- Learn `unittest` for structured testing (often required in courses)
- Learn `pytest` for modern Python development

**For school/university:**
- Follow what your instructor teaches
- Often `unittest` is required for assignments
- Understand both frameworks for exams

**For personal projects:**
- Start with `pytest` (simpler, more Pythonic)
- Use `unittest` if you prefer class-based structure

**For work/professional:**
- Follow team conventions
- New projects: usually `pytest`
- Legacy projects: often `unittest`

---

## Practice Exercise

**Scenario:** You've been given a buggy temperature converter module, and your job is to write tests that catch the bugs!

**Your task:**
1. Create a file called `temperature.py` with these buggy functions:
   ```python
   def celsius_to_fahrenheit(celsius):
       return celsius * 9/5 + 32
   
   def fahrenheit_to_celsius(fahrenheit):
       return fahrenheit - 32 * 5/9  # BUG: Missing parentheses!
   
   def is_freezing(temp, unit="celsius"):
       if unit == "celsius":
           return temp <= 0
       elif unit == "fahrenheit":
           return temp <= 30  # BUG: Should be 32!
   ```
2. Create a test file called `test_temperature.py`
3. Write at least 6 tests that cover:
   - Normal conversions (celsius to fahrenheit and vice versa)
   - Edge cases (freezing point, boiling point)
   - The `is_freezing` function with both units
4. Run the tests and watch them fail
5. Look at the error messages to identify the bugs
6. Fix the bugs in `temperature.py`
7. Run the tests again - they should all pass!

**Example test to get you started:**
```python
from temperature import celsius_to_fahrenheit

def test_celsius_to_fahrenheit():
    result = celsius_to_fahrenheit(0)
    assert result == 32, f"Expected 32, got {result}"
```

**Try it yourself first!** Solution below.

---

## Solution

### test_temperature.py

```python
import pytest
from temperature import celsius_to_fahrenheit, fahrenheit_to_celsius, is_freezing


def test_celsius_to_fahrenheit_freezing():
    """Test Celsius to Fahrenheit at freezing point."""
    result = celsius_to_fahrenheit(0)
    assert result == 32


def test_celsius_to_fahrenheit_boiling():
    """Test Celsius to Fahrenheit at boiling point."""
    result = celsius_to_fahrenheit(100)
    assert result == 212


def test_fahrenheit_to_celsius_freezing():
    """Test Fahrenheit to Celsius at freezing point."""
    result = fahrenheit_to_celsius(32)
    assert result == 0


def test_fahrenheit_to_celsius_boiling():
    """Test Fahrenheit to Celsius at boiling point."""
    result = fahrenheit_to_celsius(212)
    assert result == 100


def test_is_freezing_celsius():
    """Test freezing point in Celsius."""
    assert is_freezing(0, "celsius") == True
    assert is_freezing(-10, "celsius") == True
    assert is_freezing(10, "celsius") == False


def test_is_freezing_fahrenheit():
    """Test freezing point in Fahrenheit."""
    assert is_freezing(32, "fahrenheit") == True
    assert is_freezing(20, "fahrenheit") == True
    assert is_freezing(40, "fahrenheit") == False
```

### Fixed temperature.py

```python
def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return celsius * 9/5 + 32


def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9  # FIXED: Added parentheses!


def is_freezing(temp, unit="celsius"):
    """Check if temperature is at or below freezing."""
    if unit == "celsius":
        return temp <= 0
    elif unit == "fahrenheit":
        return temp <= 32  # FIXED: Changed from 30 to 32!
```

**To run the tests:**
```bash
# First run (with bugs) - tests will fail
pytest test_temperature.py -v

# Fix the bugs in temperature.py

# Second run (after fix) - all tests should pass!
pytest test_temperature.py -v
```

---

## Quick Recap

- **Testing** — Running code with known inputs to verify outputs
- **Manual testing** — Using `print()` for exploration
- **Automated testing** — Using `assert` or unittest
- **pytest** — Modern Python testing framework (recommended)
- **unittest** — Built-in Python testing framework (education/enterprise)
- **Test functions** — Start with `test_`
- **`assert`** — Checks if condition is true (pytest)
- **`assertEqual`, `assertTrue`** — unittest assertion methods
- **`if __name__ == "__main__":`** — Pattern to run unittest directly
- **Classes in unittest** — Required for organizing related tests
- **Edge cases** — Test unusual inputs (zeros, negatives, empty values)
- **`pytest.raises()`** — Test that errors are raised
- **Run tests:** `pytest` or `python -m unittest`

---

## What's Next?

Ready for more? Continue to **[Lesson 13: Building Your Own API](13-building-your-own-api.md)**! 🚀

---

**Your turn:** Try the temperature converter exercise! Then experiment with unittest style to see the difference! ✅💛
