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

**Without testing (manual):**
```python
# You manually test every time
result = add(2, 3)
print(result)  # Is 5 correct? Did I type it right?

# Change something? Test everything again manually!
```

**With testing (automated):**
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
# Manual testing with print()
result = add(2, 3)
print(f"Result: {result}")  # You look at output and decide if it's right

result = add(0, 0)
print(f"Result: {result}")  # You check each one manually
```

**When to use:**
- ✅ Quick experiments while learning
- ✅ Exploring how a function behaves
- ✅ One-off checks during development
- ✅ Debugging (temporarily adding print statements)

**Pros:**
- Simple and intuitive
- No setup required
- Good for exploration

**Cons:**
- You must read output and decide if it's correct
- Slow for many tests
- Easy to miss errors
- Tests aren't saved for later
- Must re-run manually after changes

---

### Automated Testing (using `assert` and `pytest`)

**What it is:** Writing code that checks if your code works correctly.

**Example:**
```python
# Automated testing with assert
def test_add():
    assert add(2, 3) == 5  # pytest checks automatically!
    assert add(0, 0) == 0
    assert add(-1, 1) == 0
```

**When to use:**
- ✅ Code that will be used repeatedly
- ✅ Projects that will change over time
- ✅ Sharing code with others
- ✅ Catching regressions (bugs that come back)
- ✅ Professional development

**Pros:**
- Tests run automatically
- Clear pass/fail results
- Tests are saved and reusable
- Fast — run hundreds of tests in seconds
- Catches bugs you might miss

**Cons:**
- Takes time to write tests
- Requires learning pytest
- Overkill for tiny scripts

---

### Comparison Table

| Aspect | Manual (`print()`) | Automated (`assert`) |
|--------|-------------------|---------------------|
| **Speed** | Slow (check each output) | Fast (all at once) |
| **Accuracy** | You might miss errors | Computer never misses |
| **Reusability** | Run manually each time | Run anytime with `pytest` |
| **Best for** | Learning, debugging | Production code |
| **Setup** | None | Install pytest |

---

### The Professional Workflow

**During development:**
1. Start with `print()` to explore and understand
2. Once you understand, write `assert` tests
3. Use `pytest` to run all tests

**Example:**
```python
# Step 1: Explore with print()
result = celsius_to_fahrenheit(0)
print(f"0°C = {result}°F")  # You see: 0°C = 32.0°F

# Step 2: Write automated test
def test_celsius_to_fahrenheit():
    assert celsius_to_fahrenheit(0) == 32

# Step 3: Run with pytest
# bash: pytest test_temp.py -v
# PASSED ✅
```

**Key insight:** `print()` is for **you** (while coding). `assert` is for **the computer** (to check automatically).

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

**Important:** Don't add extra `if` checks after `assert` — it's redundant!

```python
# WRONG - redundant code
assert result == 32
if result != 32:
    raise AssertionError  # This never runs!

# RIGHT - just use assert
assert result == 32
```

The `assert` statement ALREADY raises an error if the condition is false. No need for extra code!

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

**Output (all tests pass):**
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

## Reading Error Messages

When a test fails, pytest shows you exactly what went wrong:

**Example buggy code:**
```python
# temperature.py
def celsius_to_fahrenheit(celsius):
    return celsius * 9/5 + 32  # Correct!

def fahrenheit_to_celsius(fahrenheit):
    return fahrenheit - 32 * 5/9  # BUG: Missing parentheses!
```

**Test:**
```python
# test_temperature.py
def test_fahrenheit_to_celsius_freezing():
    result = fahrenheit_to_celsius(32)
    assert result == 0, f"Expected 0, got {result}"
```

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
1. **Test name:** `test_fahrenheit_to_celsius_freezing` — which test failed
2. **Line with `>`:** Shows the exact line that failed
3. **`E AssertionError`:** Shows what you expected vs. what you got
4. **Bottom line:** Shows the file and line number

**What the error tells you:**
- Expected: `0`
- Got: `-17.77777777777778`
- The formula is wrong! (Missing parentheses around `fahrenheit - 32`)

**Fix:**
```python
def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9  # FIXED: Added parentheses!
```

**Re-run tests:**
```bash
pytest test_temperature.py -v
```

**Now it passes!** ✅

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

## Testing Functions with Default Parameters

Some functions have optional parameters with default values:

```python
# temperature.py
def is_freezing(temp, unit="celsius"):
    if unit == "celsius":
        return temp <= 0
    elif unit == "fahrenheit":
        return temp <= 32
```

**Test both the default AND explicit values:**

```python
# test_temperature.py
def test_is_freezing_default():
    """Test default parameter (celsius)."""
    assert is_freezing(0) == True  # Uses default unit="celsius"
    assert is_freezing(-10) == True
    assert is_freezing(10) == False

def test_is_freezing_celsius():
    """Test explicit celsius parameter."""
    assert is_freezing(0, "celsius") == True
    assert is_freezing(-10, "celsius") == True

def test_is_freezing_fahrenheit():
    """Test fahrenheit parameter."""
    assert is_freezing(32, "fahrenheit") == True
    assert is_freezing(20, "fahrenheit") == True
    assert is_freezing(40, "fahrenheit") == False
```

**Why test both?**
- Default parameter might have a bug
- Explicit parameter might have a bug
- Test both to be thorough!

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

**Test it with pytest:**
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

**Test it with unittest:**
```python
# test_calculator.py
import unittest

class TestCalculator(unittest.TestCase):
    def test_divide_by_zero(self):
        """Test that dividing by zero raises an error."""
        with self.assertRaises(ValueError):
            divide(10, 0)
```

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

**Test file naming:**
- Start with `test_` (e.g., `test_calculator.py`)
- OR end with `_test.py` (e.g., `calculator_test.py`)

**Inside test files:**
- Group related tests in classes (unittest)
- OR use separate functions (pytest)
- Use descriptive names: `test_add_positive_numbers` not `test1`

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

## The Testing Workflow: Red → Green → Refactor

Professional developers follow a pattern called **"Red-Green-Refactor"**:

1. **🔴 Red:** Write a test that fails (because the code is buggy)
2. **🟢 Green:** Fix the code to make the test pass
3. **🔵 Refactor:** Clean up the code (optional)

**Example:**

**Step 1: Write test (RED - fails):**
```python
# test_temperature.py
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
# temperature.py - FIXED
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

## Other Testing Frameworks

### `unittest` — Python's Built-in Testing Framework

Python comes with a built-in testing framework called `unittest`. It's part of the standard library (no installation needed!) and uses a class-based approach.

**pytest style (what we taught):**
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
        print("Setting up test")
    
    def tearDown(self):
        """Runs after EACH test method."""
        print("Cleaning up test")
    
    def test_add(self):
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)
    
    def test_subtract(self):
        result = self.calc.subtract(5, 2)
        self.assertEqual(result, 3)
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

### Complete unittest Example

**temperature.py:**
```python
def celsius_to_fahrenheit(celsius):
    return celsius * 9/5 + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

def is_freezing(temp, unit="celsius"):
    if unit == "celsius":
        return temp <= 0
    elif unit == "fahrenheit":
        return temp <= 32
```

**test_temperature.py (unittest version):**
```python
import unittest
from temperature import celsius_to_fahrenheit, fahrenheit_to_celsius, is_freezing


class TestTemperatureConversions(unittest.TestCase):
    """Test temperature conversion functions."""
    
    def test_celsius_to_fahrenheit_freezing(self):
        """Test Celsius to Fahrenheit at freezing point."""
        result = celsius_to_fahrenheit(0)
        self.assertEqual(result, 32)
    
    def test_celsius_to_fahrenheit_boiling(self):
        """Test Celsius to Fahrenheit at boiling point."""
        result = celsius_to_fahrenheit(100)
        self.assertEqual(result, 212)
    
    def test_fahrenheit_to_celsius_freezing(self):
        """Test Fahrenheit to Celsius at freezing point."""
        result = fahrenheit_to_celsius(32)
        self.assertEqual(result, 0)
    
    def test_fahrenheit_to_celsius_boiling(self):
        """Test Fahrenheit to Celsius at boiling point."""
        result = fahrenheit_to_celsius(212)
        self.assertEqual(result, 100)


class TestIsFreezing(unittest.TestCase):
    """Test is_freezing function."""
    
    def test_is_freezing_celsius(self):
        """Test freezing point in Celsius."""
        self.assertTrue(is_freezing(0, "celsius"))
        self.assertTrue(is_freezing(-10, "celsius"))
        self.assertFalse(is_freezing(10, "celsius"))
    
    def test_is_freezing_fahrenheit(self):
        """Test freezing point in Fahrenheit."""
        self.assertTrue(is_freezing(32, "fahrenheit"))
        self.assertTrue(is_freezing(20, "fahrenheit"))
        self.assertFalse(is_freezing(40, "fahrenheit"))


if __name__ == "__main__":
    unittest.main()
```

**Run it:**
```bash
# Method 1: python -m unittest
python -m unittest test_temperature.py -v

# Method 2: Run file directly
python test_temperature.py -v
```

**Output:**
```
test_celsius_to_fahrenheit_boiling (__main__.TestTemperatureConversions) ... ok
test_celsius_to_fahrenheit_freezing (__main__.TestTemperatureConversions) ... ok
test_fahrenheit_to_celsius_boiling (__main__.TestTemperatureConversions) ... ok
test_fahrenheit_to_celsius_freezing (__main__.TestTemperatureConversions) ... ok
test_is_freezing_celsius (__main__.TestIsFreezing) ... ok
test_is_freezing_fahrenheit (__main__.TestIsFreezing) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.002s

OK
```

---

### unittest Test Methods Reference

| Method | Checks | Example |
|--------|--------|--------|
| `assertEqual(a, b)` | `a == b` | `self.assertEqual(add(2, 3), 5)` |
| `assertNotEqual(a, b)` | `a != b` | `self.assertNotEqual(x, y)` |
| `assertTrue(x)` | `x is True` | `self.assertTrue(is_valid)` |
| `assertFalse(x)` | `x is False` | `self.assertFalse(is_error)` |
| `assertIsNone(x)` | `x is None` | `self.assertIsNone(result)` |
| `assertIsNotNone(x)` | `x is not None` | `self.assertIsNotNotNone(result)` |
| `assertIn(a, b)` | `a in b` | `self.assertIn(item, list)` |
| `assertNotIn(a, b)` | `a not in b` | `self.assertNotIn(item, list)` |
| `assertIsInstance(a, b)` | `isinstance(a, b)` | `self.assertIsInstance(obj, str)` |
| `assertRaises(error)` | Exception raised | `with self.assertRaises(ValueError):` |

---

### pytest vs unittest — Assertion Comparison

| What to Test | pytest Style | unittest Style |
|--------------|--------------|----------------|
| Equality | `assert a == b` | `self.assertEqual(a, b)` |
| Inequality | `assert a != b` | `self.assertNotEqual(a, b)` |
| True | `assert x` | `self.assertTrue(x)` |
| False | `assert not x` | `self.assertFalse(x)` |
| None | `assert x is None` | `self.assertIsNone(x)` |
| In list | `assert item in list` | `self.assertIn(item, list)` |
| Exception | `with pytest.raises(Error):` | `with self.assertRaises(Error):` |
| Type check | `assert isinstance(obj, type)` | `self.assertIsInstance(obj, type)` |

**Running tests:**
```bash
# pytest
pytest test_file.py -v

# unittest
python -m unittest test_file.py -v
```

---

### pytest vs unittest — Detailed Comparison

**Use pytest when:**
- ✅ Starting a new project (modern choice)
- ✅ You want simpler, cleaner syntax
- ✅ You want better error messages
- ✅ You're writing Python 3 code
- ✅ Most open-source Python projects
- ✅ You want fixtures for setup/teardown
- ✅ You want plugins and extensions

**Use unittest when:**
- ✅ Working on legacy code (older projects)
- ✅ Your team already uses unittest
- ✅ You need built-in (no external dependencies)
- ✅ Enterprise environments with strict policies
- ✅ You want Java-style test structure (JUnit)
- ✅ Academic/educational settings (often taught in schools)
- ✅ You want unittest's built-in test discovery

**Industry trend:** Most modern Python projects use **pytest**, but unittest is still widely used in enterprise!

---

### Feature Comparison Table

| Feature | pytest | unittest |
|---------|--------|----------|
| **Installation** | `pip install pytest` | Built into Python |
| **Test structure** | Functions | Classes required |
| **Syntax** | `assert x == y` | `self.assertEqual(x, y)` |
| **Setup/teardown** | `@pytest.fixture` | `setUp()` / `tearDown()` methods |
| **Test discovery** | Automatic | Automatic |
| **Plugins** | Extensive plugin ecosystem | Limited |
| **Error messages** | Very clear, detailed | Good, but verbose |
| **Learning curve** | Gentle | Steeper (OOP required) |
| **Community** | Large, active | Mature, stable |
| **Best for** | Modern Python projects | Enterprise, legacy, education |

---

### Code Comparison: Same Tests in Both Frameworks

**pytest version:**
```python
# test_calculator_pytest.py
import pytest
from calculator import Calculator

@pytest.fixture
def calc():
    """Create a Calculator instance for tests."""
    return Calculator()

def test_add(calc):
    result = calc.add(2, 3)
    assert result == 5

def test_subtract(calc):
    result = calc.subtract(5, 2)
    assert result == 3

def test_multiply(calc):
    result = calc.multiply(4, 3)
    assert result == 12

def test_divide(calc):
    result = calc.divide(10, 2)
    assert result == 5

def test_divide_by_zero(calc):
    with pytest.raises(ValueError):
        calc.divide(10, 0)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

**unittest version:**
```python
# test_calculator_unittest.py
import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        """Create a Calculator instance before each test."""
        self.calc = Calculator()
    
    def test_add(self):
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)
    
    def test_subtract(self):
        result = self.calc.subtract(5, 2)
        self.assertEqual(result, 3)
    
    def test_multiply(self):
        result = self.calc.multiply(4, 3)
        self.assertEqual(result, 12)
    
    def test_divide(self):
        result = self.calc.divide(10, 2)
        self.assertEqual(result, 5)
    
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

if __name__ == "__main__":
    unittest.main()
```

**Run pytest version:**
```bash
pytest test_calculator_pytest.py -v
```

**Run unittest version:**
```bash
python -m unittest test_calculator_unittest.py -v
```

**Both produce similar output:**
```
test_add ... ok
test_divide ... ok
test_divide_by_zero ... ok
test_multiply ... ok
test_subtract ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.003s

OK
```

---

### Choosing the Right Testing Approach

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

**For open source:**
- Check what the project uses
- Most modern projects: `pytest`
- Older projects: `unittest`

---

### Other Testing Tools

**`doctest`** — Test examples in docstrings:
```python
def add(a, b):
    """Add two numbers.
    
    >>> add(2, 3)
    5
    >>> add(0, 0)
    0
    """
    return a + b

# Run with: python -m doctest calculator.py
```

**`coverage.py`** — Measure test coverage:
```bash
pip install coverage
coverage run -m pytest
coverage report  # Shows which lines are tested
```

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

### `unittest` — Python's Built-in Testing Framework

Python comes with a built-in testing framework called `unittest`. It's part of the standard library (no installation needed!) and uses a class-based approach.

**pytest style (what we taught):**
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
        print("Setting up test")
    
    def tearDown(self):
        """Runs after EACH test method."""
        print("Cleaning up test")
    
    def test_add(self):
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)
    
    def test_subtract(self):
        result = self.calc.subtract(5, 2)
        self.assertEqual(result, 3)
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

### Complete unittest Example

**temperature.py:**
```python
def celsius_to_fahrenheit(celsius):
    return celsius * 9/5 + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

def is_freezing(temp, unit="celsius"):
    if unit == "celsius":
        return temp <= 0
    elif unit == "fahrenheit":
        return temp <= 32
```

**test_temperature.py (unittest version):**
```python
import unittest
from temperature import celsius_to_fahrenheit, fahrenheit_to_celsius, is_freezing


class TestTemperatureConversions(unittest.TestCase):
    """Test temperature conversion functions."""
    
    def test_celsius_to_fahrenheit_freezing(self):
        """Test Celsius to Fahrenheit at freezing point."""
        result = celsius_to_fahrenheit(0)
        self.assertEqual(result, 32)
    
    def test_celsius_to_fahrenheit_boiling(self):
        """Test Celsius to Fahrenheit at boiling point."""
        result = celsius_to_fahrenheit(100)
        self.assertEqual(result, 212)
    
    def test_fahrenheit_to_celsius_freezing(self):
        """Test Fahrenheit to Celsius at freezing point."""
        result = fahrenheit_to_celsius(32)
        self.assertEqual(result, 0)
    
    def test_fahrenheit_to_celsius_boiling(self):
        """Test Fahrenheit to Celsius at boiling point."""
        result = fahrenheit_to_celsius(212)
        self.assertEqual(result, 100)


class TestIsFreezing(unittest.TestCase):
    """Test is_freezing function."""
    
    def test_is_freezing_celsius(self):
        """Test freezing point in Celsius."""
        self.assertTrue(is_freezing(0, "celsius"))
        self.assertTrue(is_freezing(-10, "celsius"))
        self.assertFalse(is_freezing(10, "celsius"))
    
    def test_is_freezing_fahrenheit(self):
        """Test freezing point in Fahrenheit."""
        self.assertTrue(is_freezing(32, "fahrenheit"))
        self.assertTrue(is_freezing(20, "fahrenheit"))
        self.assertFalse(is_freezing(40, "fahrenheit"))


if __name__ == "__main__":
    unittest.main()
```

**Run it:**
```bash
# Method 1: python -m unittest
python -m unittest test_temperature.py -v

# Method 2: Run file directly
python test_temperature.py -v
```

**Output:**
```
test_celsius_to_fahrenheit_boiling (__main__.TestTemperatureConversions) ... ok
test_celsius_to_fahrenheit_freezing (__main__.TestTemperatureConversions) ... ok
test_fahrenheit_to_celsius_boiling (__main__.TestTemperatureConversions) ... ok
test_fahrenheit_to_celsius_freezing (__main__.TestTemperatureConversions) ... ok
test_is_freezing_celsius (__main__.TestIsFreezing) ... ok
test_is_freezing_fahrenheit (__main__.TestIsFreezing) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.002s

OK
```

---

### unittest Test Methods Reference

| Method | Checks | Example |
|--------|--------|--------|
| `assertEqual(a, b)` | `a == b` | `self.assertEqual(add(2, 3), 5)` |
| `assertNotEqual(a, b)` | `a != b` | `self.assertNotEqual(x, y)` |
| `assertTrue(x)` | `x is True` | `self.assertTrue(is_valid)` |
| `assertFalse(x)` | `x is False` | `self.assertFalse(is_error)` |
| `assertIsNone(x)` | `x is None` | `self.assertIsNone(result)` |
| `assertIsNotNone(x)` | `x is not None` | `self.assertIsNotNotNone(result)` |
| `assertIn(a, b)` | `a in b` | `self.assertIn(item, list)` |
| `assertNotIn(a, b)` | `a not in b` | `self.assertNotIn(item, list)` |
| `assertIsInstance(a, b)` | `isinstance(a, b)` | `self.assertIsInstance(obj, str)` |
| `assertRaises(error)` | Exception raised | `with self.assertRaises(ValueError):` |

---

### pytest vs unittest — Assertion Comparison

| What to Test | pytest Style | unittest Style |
|--------------|--------------|----------------|
| Equality | `assert a == b` | `self.assertEqual(a, b)` |
| Inequality | `assert a != b` | `self.assertNotEqual(a, b)` |
| True | `assert x` | `self.assertTrue(x)` |
| False | `assert not x` | `self.assertFalse(x)` |
| None | `assert x is None` | `self.assertIsNone(x)` |
| In list | `assert item in list` | `self.assertIn(item, list)` |
| Exception | `with pytest.raises(Error):` | `with self.assertRaises(Error):` |
| Type check | `assert isinstance(obj, type)` | `self.assertIsInstance(obj, type)` |

**Running tests:**
```bash
# pytest
pytest test_file.py -v

# unittest
python -m unittest test_file.py -v
```

---

### pytest vs unittest — Detailed Comparison

**Use pytest when:**
- ✅ Starting a new project (modern choice)
- ✅ You want simpler, cleaner syntax
- ✅ You want better error messages
- ✅ You're writing Python 3 code
- ✅ Most open-source Python projects
- ✅ You want fixtures for setup/teardown
- ✅ You want plugins and extensions

**Use unittest when:**
- ✅ Working on legacy code (older projects)
- ✅ Your team already uses unittest
- ✅ You need built-in (no external dependencies)
- ✅ Enterprise environments with strict policies
- ✅ You need Java-style test structure (JUnit)
- ✅ Academic/educational settings (often taught in schools)
- ✅ You want unittest's built-in test discovery

**Industry trend:** Most modern Python projects use **pytest**, but unittest is still widely used in enterprise!

---

### Feature Comparison Table

| Feature | pytest | unittest |
|---------|--------|----------|
| **Installation** | `pip install pytest` | Built into Python |
| **Test structure** | Functions | Classes required |
| **Syntax** | `assert x == y` | `self.assertEqual(x, y)` |
| **Setup/teardown** | `@pytest.fixture` | `setUp()` / `tearDown()` methods |
| **Test discovery** | Automatic | Automatic |
| **Plugins** | Extensive plugin ecosystem | Limited |
| **Error messages** | Very clear, detailed | Good, but verbose |
| **Learning curve** | Gentle | Steeper (OOP required) |
| **Community** | Large, active | Mature, stable |
| **Best for** | Modern Python projects | Enterprise, legacy, education |

---

### Code Comparison: Same Tests in Both Frameworks

**pytest version:**
```python
# test_calculator.py
import pytest

def test_add():
    assert add(2, 3) == 5

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)

@pytest.fixture
def calc():
    """Setup: create calculator before test."""
    return Calculator()

def test_calculator_add(calc):
    result = calc.add(2, 3)
    assert result == 5
```

**unittest version:**
```python
# test_calculator.py
import unittest

class TestCalculator(unittest.TestCase):
    def setUp(self):
        """Setup: create calculator before each test."""
        self.calc = Calculator()
    
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
    
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(10, 0)
    
    def test_calculator_add(self):
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)

if __name__ == "__main__":
    unittest.main()
```

**Key differences:**
1. pytest uses functions, unittest uses classes
2. pytest uses `assert`, unittest uses `self.assertEqual()`
3. pytest uses `@pytest.fixture`, unittest uses `setUp()`
4. unittest requires `if __name__ == "__main__":` to run directly

---

### Choosing the Right Testing Approach

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

**For open source:**
- Check what the project uses
- Most modern projects: `pytest`
- Older projects: `unittest`

---

### Complete Example: Both Frameworks Side by Side

**Code to test:**
```python
# calculator.py
class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
```

**pytest version:**
```python
# test_calculator_pytest.py
import pytest
from calculator import Calculator

@pytest.fixture
def calc():
    """Create a Calculator instance for tests."""
    return Calculator()

def test_add(calc):
    result = calc.add(2, 3)
    assert result == 5

def test_subtract(calc):
    result = calc.subtract(5, 2)
    assert result == 3

def test_multiply(calc):
    result = calc.multiply(4, 3)
    assert result == 12

def test_divide(calc):
    result = calc.divide(10, 2)
    assert result == 5

def test_divide_by_zero(calc):
    with pytest.raises(ValueError):
        calc.divide(10, 0)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

**unittest version:**
```python
# test_calculator_unittest.py
import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        """Create a Calculator instance before each test."""
        self.calc = Calculator()
    
    def test_add(self):
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)
    
    def test_subtract(self):
        result = self.calc.subtract(5, 2)
        self.assertEqual(result, 3)
    
    def test_multiply(self):
        result = self.calc.multiply(4, 3)
        self.assertEqual(result, 12)
    
    def test_divide(self):
        result = self.calc.divide(10, 2)
        self.assertEqual(result, 5)
    
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

if __name__ == "__main__":
    unittest.main()
```

**Run pytest version:**
```bash
pytest test_calculator_pytest.py -v
```

**Run unittest version:**
```bash
python -m unittest test_calculator_unittest.py -v
```

**Both produce similar output:**
```
test_add ... ok
test_divide ... ok
test_divide_by_zero ... ok
test_multiply ... ok
test_subtract ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.003s

OK
```

---

### Other Testing Tools

**`doctest`** — Test examples in docstrings:
```python
def add(a, b):
    """Add two numbers.
    
    >>> add(2, 3)
    5
    >>> add(0, 0)
    0
    """
    return a + b

# Run with: python -m doctest calculator.py
```

**`coverage.py`** — Measure test coverage:
```bash
pip install coverage
coverage run -m pytest
coverage report  # Shows which lines are tested
```

---

## Quick Recap

- **Testing** — Running code with known inputs to verify outputs
- **Manual testing** — Using `print()` for exploration
- **Automated testing** — Using `assert` or `unittest`
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

---

## Common Testing Mistakes

### Mistake 1: Redundant Assertions

**WRONG:**
```python
def test_something():
    result = add(2, 3)
    assert result == 5
    if result != 5:  # This never runs!
        raise AssertionError
```

**RIGHT:**
```python
def test_something():
    result = add(2, 3)
    assert result == 5  # assert already raises error if false!
```

---

### Mistake 2: Testing Multiple Things in One Test

**WRONG:**
```python
def test_add_and_multiply():
    assert add(2, 3) == 5
    assert multiply(2, 3) == 6  # What if this fails?
    assert subtract(5, 2) == 3
```

**RIGHT:**
```python
def test_add():
    assert add(2, 3) == 5

def test_multiply():
    assert multiply(2, 3) == 6

def test_subtract():
    assert subtract(5, 2) == 3
```

**Why?** If one test fails, you know exactly which function is broken!

---

### Mistake 3: Not Testing Edge Cases

**WRONG:**
```python
def test_divide():
    assert divide(10, 2) == 5  # Only tests normal case
```

**RIGHT:**
```python
def test_divide_normal():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)  # Edge case!
```

---

### Mistake 4: Ignoring Test Names

**WRONG:**
```python
def test1():
    ...
def test2():
    ...
```

**RIGHT:**
```python
def test_add_positive_numbers():
    ...
def test_add_negative_numbers():
    ...
```

**Why?** When a test fails, the name tells you what broke!

---

### Mistake 5: Not Importing the Module

**ERROR:** `ModuleNotFoundError: No module named 'temperature'`

**FIX:** Make sure both files are in the same folder:
```
my_project/
├── temperature.py
└── test_temperature.py
```

And import correctly:
```python
from temperature import celsius_to_fahrenheit
```

---

### Mistake 6: pytest Not Found

**ERROR:** `command not found: pytest`

**FIX 1:** Install pytest:
```bash
pip install pytest
```

**FIX 2:** Run through Python module:
```bash
python -m pytest test_file.py -v
```

**FIX 3:** Check you're in the right environment:
```bash
which python
python -m pip freeze | grep pytest
```
