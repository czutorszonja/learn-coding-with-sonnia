# Python Lesson 10: Error Handling — Dealing with Mistakes 🛡️

**← Back to [Lesson 9: File Handling](09-files-explained.md)**

---

## What is Error Handling?

**Plain English:** Error handling means preparing your code for when things go wrong, so it doesn't crash.

**Real-world analogy:** Imagine you're cooking:
- You plan for mistakes: "If I burn the toast, I'll make more"
- You don't just give up and starve!
- You have a backup plan

Error handling is your code's backup plan!

---

## Why Handle Errors?

**Without error handling:**
```python
# Program crashes!
number = int(input("Enter a number: "))
# User types "hello" instead of a number
# CRASH! ValueError: invalid literal for int()
```

**With error handling:**
```python
# Program continues!
try:
    number = int(input("Enter a number: "))
    print(f"You entered: {number}")
except ValueError:
    print("That's not a valid number!")
# Program continues running!
```

---

## The `try` and `except` Blocks

**Basic structure:**
```python
try:
    # Code that might cause an error
    risky_code()
except:
    # Code to run if there's an error
    print("Something went wrong!")
```

**How it works:**
1. Python tries to run the code in `try` block
2. If no error: runs the `try` block and skips `except`
3. If error occurs: stops `try` block and runs `except` block

---

## Catching Specific Errors

**Better practice:** Catch the specific error type:

```python
try:
    number = int(input("Enter a number: "))
    result = 10 / number
    print(f"Result: {result}")
except ValueError:
    print("That's not a valid number!")
except ZeroDivisionError:
    print("You can't divide by zero!")
```

**Common error types:**
- `ValueError` — Wrong type (e.g., `int("hello")`)
- `ZeroDivisionError` — Dividing by zero
- `FileNotFoundError` — File doesn't exist
- `IndexError` — List index out of range
- `KeyError` — Dictionary key doesn't exist

---

## The `else` Block

Run code only if NO error occurred:

```python
try:
    number = int(input("Enter a number: "))
    result = 10 / number
except ValueError:
    print("That's not a valid number!")
except ZeroDivisionError:
    print("You can't divide by zero!")
else:
    print(f"Result: {result}")
    print("Calculation successful!")
```

**When to use:** When you want to run code only if the `try` block succeeds.

---

## The `finally` Block

Code that **always** runs, whether there's an error or not:

```python
try:
    file = open("data.txt", "r")
    content = file.read()
    print(content)
except FileNotFoundError:
    print("File not found!")
finally:
    file.close()
    print("File closed.")
```

**When to use:** For cleanup code (closing files, closing connections, etc.).

**Note:** When using `with` statement, you don't need `finally` for closing files!

---

## Raising Exceptions

You can **create** errors on purpose:

```python
def withdraw_money(balance, amount):
    if amount > balance:
        raise ValueError("Not enough money!")
    return balance - amount

# Test it
try:
    new_balance = withdraw_money(100, 150)
except ValueError as e:
    print(f"Error: {e}")
```

**Output:**
```
Error: Not enough money!
```

**When to use:** When your function detects invalid input or impossible conditions.

---

## Practice Exercise

**Scenario:** You're building a calculator that needs to handle user mistakes gracefully!

**Your task:**
1. Create a function called `safe_divide` that takes two parameters: `a` and `b`
2. The function should try to divide `a` by `b` and return the result
3. Handle `ZeroDivisionError` by returning `None` and printing an error message
4. Handle `TypeError` (if user passes non-numbers) by returning `None` and printing an error message
5. Test it with different inputs (including edge cases)

**Try it yourself first!** Solution below.

---

## Solution

```python
def safe_divide(a, b):
    """Divide a by b with error handling."""
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
        return None
    except TypeError:
        print("Error: Both arguments must be numbers!")
        return None

# Test the function
print("Test 1: Normal division")
print(f"10 / 2 = {safe_divide(10, 2)}")

print("\nTest 2: Division by zero")
print(f"10 / 0 = {safe_divide(10, 0)}")

print("\nTest 3: String instead of number")
print(f"10 / 'hello' = {safe_divide(10, 'hello')}")
```

**Output:**
```
Test 1: Normal division
10 / 2 = 5.0

Test 2: Division by zero
Error: Cannot divide by zero!
10 / 0 = None

Test 3: String instead of number
Error: Both arguments must be numbers!
10 / 'hello' = None
```

---

## Quick Recap

- **`try`** — Code that might cause an error
- **`except`** — Code to run if there's an error
- **`else`** — Code to run if NO error (optional)
- **`finally`** — Code that always runs (optional)
- **Catch specific errors** — Don't use bare `except`
- **`raise`** — Create your own errors
- **Error handling makes your code robust!**

---

## What's Next?

Ready for more? Continue to **[Lesson 11: Working with APIs](11-working-with-apis.md)**! 🚀

---

**Your turn:** Try the calculator exercise! Add more error checks or create your own functions with error handling! 🛡️💛
