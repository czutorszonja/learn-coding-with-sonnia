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

**Scenario:** You're building a user registration system that validates age input!

**Your task:**
1. Create a function called `get_user_age` that asks for age input and returns it as an integer
2. Handle `ValueError` if the user types non-numbers (print error and return None)
3. Handle the case if age is negative (raise a `ValueError` with a message)
4. Handle the case if age is over 150 (raise a `ValueError` with a message)
5. Create another function called `register_user` that takes name and age as parameters
6. This function should check if age is valid (use try/except) and print a welcome message
7. Test with different inputs: valid age, text, negative number, very large number

**Example output:**
```
Enter your age: hello
Error: Age must be a number!
Enter your age: -5
Error: Age cannot be negative!
Enter your age: 25
Welcome, Arthur! You are 25 years old.
```

**Try it yourself first!** Solution below.

---

## Solution

```python
def get_user_age():
    """Get age from user with error handling."""
    try:
        age_input = input("Enter your age: ")
        age = int(age_input)
        
        if age < 0:
            raise ValueError("Age cannot be negative!")
        if age > 150:
            raise ValueError("Age cannot be over 150!")
        
        return age
    except ValueError as e:
        print(f"Error: {e}")
        return None

def register_user(name, age):
    """Register a user with validation."""
    if age is None:
        print("Registration failed: Invalid age")
        return
    
    print(f"Welcome, {name}! You are {age} years old.")
    print("Registration successful!")

# Test the functions
print("=== User Registration ===")
name = input("Enter your name: ")
age = get_user_age()
register_user(name, age)
```

**Example runs:**
```
=== User Registration ===
Enter your name: Arthur
Enter your age: hello
Error: Age must be a number!
Registration failed: Invalid age
```

```
=== User Registration ===
Enter your name: Szonja
Enter your age: 25
Welcome, Szonja! You are 25 years old.
Registration successful!
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

**Your turn:** Try the registration exercise! Add more validations like checking if name is empty! 🛡️💛
