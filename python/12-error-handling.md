# Python Lesson 12: Error Handling and Debugging 🐛

**← Back to [Lesson 11: File Handling](11-file-handling.md)**

---

## What are Errors?

**Plain English:** Errors (also called exceptions) are problems that occur when your code runs.

**Real-world analogy:** Imagine you're following a recipe:
- **Syntax error** = Recipe has a typo, you can't even start cooking
- **Runtime error** = You run out of an ingredient while cooking
- **Logic error** = You followed the recipe but the dish tastes wrong

---

## Types of Errors

### 1. Syntax Errors

The code won't even run!

```python
# Missing colon
if True
    print("Hello")  # SyntaxError: invalid syntax

# Missing parenthesis
print("Hello"  # SyntaxError: unexpected EOF
```

**Fix:** Read the error message — it tells you exactly where the problem is!

---

### 2. Runtime Errors (Exceptions)

Code starts running but crashes:

```python
# Division by zero
result = 10 / 0  # ZeroDivisionError

# Accessing non-existent key
person = {"name": "Alice"}
print(person["age"])  # KeyError: 'age'

# Accessing non-existent list item
numbers = [1, 2, 3]
print(numbers[10])  # IndexError: list index out of range

# Converting invalid string to int
age = int("hello")  # ValueError: invalid literal
```

---

### 3. Logic Errors

Code runs but gives wrong results:

```python
# Calculating average (WRONG)
numbers = [10, 20, 30]
average = sum(numbers) / 2  # Should be / 3!
print(average)  # Output: 30.0 (wrong!)
```

**Fix:** Test your code with known inputs and check outputs!

---

## Handling Errors with `try/except`

### Basic try/except

```python
try:
    number = int(input("Enter a number: "))
    result = 10 / number
    print(f"Result: {result}")
except ZeroDivisionError:
    print("You can't divide by zero!")
except ValueError:
    print("Please enter a valid number!")
```

**Output:**
```
Enter a number: 0
You can't divide by zero!
```

---

### Multiple except blocks

```python
try:
    with open("data.txt", "r") as file:
        content = file.read()
        number = int(content)
        result = 10 / number
except FileNotFoundError:
    print("File not found!")
except ValueError:
    print("File doesn't contain a valid number!")
except ZeroDivisionError:
    print("Can't divide by zero!")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

---

### Using `else` and `finally`

```python
try:
    number = int(input("Enter a number: "))
    result = 10 / number
except ZeroDivisionError:
    print("Can't divide by zero!")
except ValueError:
    print("Invalid number!")
else:
    # Runs ONLY if no error occurred
    print(f"Result: {result}")
finally:
    # ALWAYS runs (even if error occurred)
    print("Thank you for using the calculator!")
```

**Output (success):**
```
Enter a number: 2
Result: 5.0
Thank you for using the calculator!
```

**Output (error):**
```
Enter a number: 0
Can't divide by zero!
Thank you for using the calculator!
```

---

## Raising Your Own Errors

Use `raise` to create custom errors:

```python
def withdraw_money(balance, amount):
    if amount > balance:
        raise ValueError("Insufficient funds!")
    if amount < 0:
        raise ValueError("Can't withdraw negative amount!")
    return balance - amount

# Usage
try:
    new_balance = withdraw_money(100, 150)
except ValueError as e:
    print(f"Error: {e}")
```

**Output:**
```
Error: Insufficient funds!
```

---

## Debugging Techniques

### 1. Print Statements

```python
def calculate_average(numbers):
    print(f"DEBUG: Input = {numbers}")
    total = sum(numbers)
    print(f"DEBUG: Total = {total}")
    count = len(numbers)
    print(f"DEBUG: Count = {count}")
    average = total / count
    print(f"DEBUG: Average = {average}")
    return average

calculate_average([10, 20, 30])
```

**Output:**
```
DEBUG: Input = [10, 20, 30]
DEBUG: Total = 60
DEBUG: Count = 3
DEBUG: Average = 20.0
```

---

### 2. Using `assert` for Testing

```python
def add(a, b):
    return a + b

# Test the function
assert add(2, 3) == 5, "2 + 3 should equal 5"
assert add(0, 0) == 0, "0 + 0 should equal 0"
assert add(-1, 1) == 0, "-1 + 1 should equal 0"
print("All tests passed!")
```

---

### 3. Using Python Debugger (`pdb`)

```python
import pdb

def calculate_total(prices):
    total = 0
    for price in prices:
        pdb.set_trace()  # Pause execution here
        total += price
    return total

calculate_total([10, 20, 30])
```

**Common pdb commands:**
- `n` (next) — Execute next line
- `c` (continue) — Continue until next breakpoint
- `l` (list) — Show current code
- `p variable` — Print variable value
- `q` (quit) — Exit debugger

---

## Common Error Types

| Error | When it occurs | Example |
|-------|---------------|---------|
| `SyntaxError` | Invalid Python syntax | `if True print("hi")` |
| `NameError` | Variable doesn't exist | `print(x)` when x not defined |
| `TypeError` | Wrong data type | `"5" + 3` |
| `ValueError` | Right type, wrong value | `int("hello")` |
| `IndexError` | List index out of range | `[1,2,3][10]` |
| `KeyError` | Dictionary key doesn't exist | `{"a": 1}["b"]` |
| `FileNotFoundError` | File doesn't exist | `open("missing.txt")` |
| `ZeroDivisionError` | Dividing by zero | `10 / 0` |
| `AttributeError` | Object doesn't have that attribute | `"hello".uppercase()` |

---

## Best Practices

### ✅ DO:

```python
# Be specific with exceptions
try:
    result = 10 / int(input("Enter number: "))
except ValueError:
    print("Please enter a valid number!")
except ZeroDivisionError:
    print("Can't divide by zero!")

# Log errors
import logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

try:
    risky_operation()
except Exception as e:
    logging.error(f"Error occurred: {e}")

# Clean up resources
with open("file.txt", "r") as f:
    content = f.read()
# File automatically closed
```

### ❌ DON'T:

```python
# Don't catch all exceptions vaguely
try:
    do_something()
except:  # Too broad!
    pass  # Silently ignores error

# Don't use exceptions for normal flow
if key in dictionary:
    value = dictionary[key]
else:
    value = None
# NOT: try: value = dictionary[key] except KeyError: value = None
```

---

## Practice Exercise

### Scenario: You're building a calculator that handles errors!

**Your task:**
1. Ask the user to enter two numbers (use `input()`)
2. Convert both inputs to integers
3. Handle `ValueError` if the input is not a valid number
4. Try to divide the first number by the second
5. Handle `ZeroDivisionError` if the second number is zero
6. Use an `else` block to print the result if successful
7. Use a `finally` block to print "Calculation complete!"

**Try it yourself first!** Scroll down when ready.

---

## Solutions

### Solution 1: Build a Robust Calculator

```python
try:
    # Get user input
    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))
    
    # Try to divide
    result = num1 / num2
    
except ValueError:
    print("Please enter valid numbers!")
except ZeroDivisionError:
    print("Can't divide by zero!")
else:
    print(f"Result: {result}")
finally:
    print("Calculation complete!")
```

**Output:**
```
Enter first number: 10
Enter second number: 0
Can't divide by zero!
Calculation complete!
```

---

## Quick Recap

- **Syntax errors** — Code won't run (fix the syntax!)
- **Runtime errors** — Code crashes (use try/except!)
- **Logic errors** — Wrong results (debug with print statements!)
- **`try/except`** — Handle errors gracefully
- **`else`** — Runs if no error occurred
- **`finally`** — Always runs (cleanup code)
- **`raise`** — Create custom errors
- **`assert`** — Test your code
- **`pdb`** — Python debugger for stepping through code

---

## What's Next?

Ready for more? Continue to **[Lesson 13: Working with APIs](13-working-with-apis.md)** — learn to fetch data from the web! 🌐

---

