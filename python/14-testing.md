# Python Lesson 14: Testing Your Code ✅

**← Back to [Lesson 13: Working with APIs](13-working-with-apis.md)**

---

## Why Test Your Code?

**Plain English:** Testing means checking that your code does what you expect it to do.

**Real-world analogy:** Imagine building a car:
- **Without testing** = Drive it off the lot and hope it works
- **With testing** = Test brakes, engine, lights before selling

Testing catches bugs before your users do!

---

## Benefits of Testing

- ✅ Catches bugs early
- ✅ Makes refactoring safer
- ✅ Documents how code should work
- ✅ Gives confidence to deploy
- ✅ Saves time debugging later

---

## The `unittest` Module

Python has a built-in testing framework:

```python
import unittest

def add(a, b):
    return a + b

class TestMath(unittest.TestCase):
    def test_add_positive_numbers(self):
        result = add(2, 3)
        self.assertEqual(result, 5)
    
    def test_add_negative_numbers(self):
        result = add(-2, -3)
        self.assertEqual(result, -5)

if __name__ == "__main__":
    unittest.main()
```

**Run tests:**
```bash
python test_file.py
```

---

## Common Assertion Methods

| Method | Checks | Example |
|--------|--------|---------|
| `assertEqual(a, b)` | `a == b` | `self.assertEqual(2+2, 4)` |
| `assertNotEqual(a, b)` | `a != b` | `self.assertNotEqual(2, 3)` |
| `assertTrue(x)` | `bool(x) is True` | `self.assertTrue(5 > 3)` |
| `assertFalse(x)` | `bool(x) is False` | `self.assertFalse(5 > 10)` |
| `assertIsNone(x)` | `x is None` | `self.assertIsNone(result)` |
| `assertIn(a, b)` | `a in b` | `self.assertIn(3, [1, 2, 3])` |
| `assertRaises(Error)` | Exception raised | `self.assertRaises(ValueError, func)` |

---

## Using `pytest` (Recommended!)

`pytest` is simpler and more popular:

**Install:**
```bash
pip install pytest
```

**Create test file:**
```python
# test_calculator.py
def add(a, b):
    return a + b

def test_add_positive_numbers():
    result = add(2, 3)
    assert result == 5

def test_add_negative_numbers():
    result = add(-2, -3)
    assert result == -5

def test_add_mixed_numbers():
    result = add(-2, 3)
    assert result == 1
```

**Run tests:**
```bash
pytest test_calculator.py
```

**Output:**
```
============================= test session starts =============================
collected 3 items

test_calculator.py ...                                                   [100%]

============================== 3 passed in 0.01s ==============================
```

---

## Test Naming Conventions

- Test files: `test_*.py` or `*_test.py`
- Test functions: `test_*`
- Test classes: `Test*`

**Examples:**
```
test_user.py
test_api.py
test_utils.py
```

---

## Running Tests

### Run all tests in directory:
```bash
pytest
```

### Run specific file:
```bash
pytest test_user.py
```

### Run specific test:
```bash
pytest test_user.py::test_create_user
```

### Run with verbose output:
```bash
pytest -v
```

### Run and show coverage:
```bash
pytest --cov=.
```

---

## Testing Different Scenarios

### Test for exceptions:
```python
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
```

### Test with parameters:
```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (5, 5, 10),
    (0, 0, 0),
    (-2, 2, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

---

## Test Fixtures

Fixtures set up test data:

```python
import pytest

@pytest.fixture
def sample_user():
    return {"name": "Alice", "age": 30, "email": "alice@example.com"}

def test_user_name(sample_user):
    assert sample_user["name"] == "Alice"

def test_user_age(sample_user):
    assert sample_user["age"] == 30
```

---

## Mocking External Services

Test without calling real APIs:

```python
import pytest
from unittest.mock import patch
import requests

def get_user_data(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

@patch('requests.get')
def test_get_user_data(mock_get):
    # Mock the response
    mock_get.return_value.json.return_value = {"id": 1, "name": "Alice"}
    
    result = get_user_data(1)
    
    assert result["name"] == "Alice"
    mock_get.assert_called_once_with("https://api.example.com/users/1")
```

---

## Test-Driven Development (TDD)

**Red-Green-Refactor cycle:**

1. **Red** — Write a failing test
2. **Green** — Write code to pass the test
3. **Refactor** — Improve the code (tests ensure it still works)

**Example:**
```python
# Step 1: Write failing test
def test_calculate_discount():
    assert calculate_discount(100, 20) == 80

# Step 2: Make it pass
def calculate_discount(price, discount):
    return price - (price * discount / 100)

# Step 3: Refactor (add validation)
def calculate_discount(price, discount):
    if price < 0 or discount < 0:
        raise ValueError("Values must be positive!")
    return price - (price * discount / 100)
```

---

## Best Practices

### ✅ DO:

```python
# Write independent tests
def test_addition():
    assert add(2, 3) == 5

def test_subtraction():
    assert subtract(5, 3) == 2

# Use descriptive names
def test_user_login_with_valid_credentials():
    ...

# Test one thing per test
def test_empty_cart():
    cart = Cart()
    assert cart.is_empty()

# Test edge cases
def test_add_zero():
    assert add(0, 0) == 0
```

### ❌ DON'T:

```python
# Don't test multiple things
def test_everything():
    assert add(2, 3) == 5
    assert subtract(5, 3) == 2
    assert multiply(2, 3) == 6

# Don't depend on test order
def test_b():
    result = test_a()  # Bad!
    assert result == 5
```

---

## Practice Exercise

### Scenario: You're testing a calculator module!

**Your task:**
1. Create a file called `test_calculator.py`
2. Create functions: `add(a, b)`, `subtract(a, b)`, `multiply(a, b)`
3. Write a test that checks `add(2, 3)` returns `5`
4. Write a test that checks `subtract(5, 2)` returns `3`
5. Write a test that checks `multiply(3, 4)` returns `12`
6. Add a test for edge case: `add(0, 0)` returns `0`
7. Run all tests with `pytest -v`

**Try it yourself first!** Scroll down when ready.

---

## Solutions

### Solution 1: Build a Test Suite for a Calculator

```python
# test_calculator.py

# Functions to test
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

# Test functions
def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(5, 2) == 3

def test_multiply():
    assert multiply(3, 4) == 12

def test_add_zero():
    assert add(0, 0) == 0
```

**Run:**
```bash
pytest test_calculator.py -v
```

**Output:**
```
test_calculator.py::test_add PASSED
test_calculator.py::test_subtract PASSED
test_calculator.py::test_multiply PASSED
test_calculator.py::test_add_zero PASSED
```

---

## Quick Recap

- **Testing** = Verify code works correctly
- **`unittest`** = Built-in testing framework
- **`pytest`** = Simpler, more popular (recommended!)
- **Assertions** = `assertEqual`, `assertTrue`, `assertRaises`
- **Fixtures** = Reusable test data
- **Mocking** = Test without external services
- **TDD** = Write tests first, then code
- **Run tests** = `pytest` or `pytest -v`

---

## What's Next?

Ready for more? Continue to **[Lesson 15: Building Your Own API](15-building-api.md)** — learn to create REST APIs with FastAPI! 🚀

---

