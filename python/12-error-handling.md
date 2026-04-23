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

## Practice Exercises

### Exercise 1: Safe Division

**Scenario:** You're building a calculator that handles errors gracefully!

**Your task:**
1. Create a function called `safe_divide` that takes two parameters: `a` and `b`
2. Try to divide `a` by `b`
3. Handle `ZeroDivisionError` by returning `None`
4. Handle `TypeError` by returning `None`
5. If successful, return the result

**Try it yourself first!** Scroll down when ready.

---

### Exercise 2: Read File Safely

**Scenario:** You need to read a file that might not exist!

**Your task:**
1. Create a function called `read_file_safely` that takes a `filename` parameter
2. Try to open and read the file
3. Handle `FileNotFoundError` by returning "File not found!"
4. Handle any other errors by returning "An error occurred!"
5. If successful, return the file content

**Try it yourself first!** Scroll down when ready.

---

### Exercise 3: Validate User Input

**Scenario:** You're asking for user input and need to handle invalid entries!

**Your task:**
1. Ask the user to enter their age
2. Try to convert it to an integer
3. Handle `ValueError` by printing "Please enter a valid number!"
4. Check if age is between 0 and 150
5. If not, raise a `ValueError` with message "Invalid age!"
6. If valid, print "Age accepted!"

**Try it yourself first!** Scroll down when ready.

---

### Exercise 4: Debug the Code

**Scenario:** Here's broken code. Find and fix the bugs!

```python
def calculate_discount(price, discount_percent):
    discount = price * discount_percent / 100
    final_price = price - discount
    return final_price

# Test cases
print(calculate_discount(100, 20))  # Should be 80
print(calculate_discount(50, 10))   # Should be 45
print(calculate_discount(100, 150))  # Should handle negative price
```

**Your task:**
1. Identify what's wrong
2. Add error handling or validation
3. Test with the provided cases

**Try it yourself first!** Scroll down when ready.

---

## Solutions

### Solution 1: Safe Division

```python
def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return None
    except TypeError:
        return None

# Test
print(safe_divide(10, 2))    # Output: 5.0
print(safe_divide(10, 0))    # Output: None
print(safe_divide("10", 2))  # Output: None
```

---

### Solution 2: Read File Safely

```python
def read_file_safely(filename):
    try:
        with open(filename, "r") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "File not found!"
    except Exception:
        return "An error occurred!"

# Test
print(read_file_safely("existing.txt"))  # Output: file content
print(read_file_safely("missing.txt"))   # Output: File not found!
```

---

### Solution 3: Validate User Input

```python
def validate_age():
    try:
        age = int(input("Enter your age: "))
        if age < 0 or age > 150:
            raise ValueError("Invalid age!")
        print("Age accepted!")
    except ValueError as e:
        if str(e) == "Invalid age!":
            print(e)
        else:
            print("Please enter a valid number!")

# Run
validate_age()
```

**Output:**
```
Enter your age: -5
Invalid age!
```

---

### Solution 4: Debug the Code

```python
def calculate_discount(price, discount_percent):
    # Validate inputs
    if price < 0:
        raise ValueError("Price cannot be negative!")
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100!")
    
    discount = price * discount_percent / 100
    final_price = price - discount
    return final_price

# Test cases
print(calculate_discount(100, 20))  # Output: 80.0
print(calculate_discount(50, 10))   # Output: 45.0
print(calculate_discount(100, 150))  # Raises ValueError
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

**Your turn:** Try the exercises above! Error handling is crucial for robust applications. Ask if you get stuck! 💛🌞
