# Python Lesson 18: Debugging Techniques 🐛

**← Back to [Lesson 17: Virtual Environments and Packages](17-virtual-environments.md)**

---

## What is Debugging?

**Plain English:** Debugging is finding and fixing bugs (errors) in your code.

**Real-world analogy:** Imagine you're a detective:
- **The crime** = Your code isn't working
- **The clues** = Error messages, wrong outputs
- **The investigation** = Debugging techniques
- **The solution** = Fixing the bug

---

## The Debugging Spectrum

Think of debugging techniques like tools in a toolbox — you don't use a sledgehammer for a screw:

```
Simple ←───────────────────────────────────→ Complex
  │                                           │
print()  →  logging  →  assert  →  pdb  →  IDE Debugger
```

---

## 1. Print Statements

**What it is:** Adding `print()` calls to show variable values at specific points.

**When to use it:**
- Quick checks during development
- Simple scripts where you just need to see a value
- When you can't install extra tools
- When code runs once and finishes

**Example:**
```python
def calculate_total(prices):
    print(f"DEBUG: Input = {prices}")  # See what we got
    total = sum(prices)
    print(f"DEBUG: Total = {total}")    # See the result
    return total

calculate_total([10, 20, 30])
```

**Output:**
```
DEBUG: Input = [10, 20, 30]
DEBUG: Total = 60
```

**Limitations:**
- Clutters your code (must remove later)
- Can't pause execution
- Hard to use in production (spammy logs)
- Time-consuming if you need to check many variables

**Why choose it:** Fast, no setup, works everywhere.

---

## 2. Logging Module

**What it is:** Python's built-in logging system — like `print()` but professional.

**When to use it:**
- Production code (can be turned off without removing code)
- Long-running applications (servers, bots)
- When you need timestamps, severity levels
- Tracking events over time

**Example:**
```python
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def process_order(order_id, amount):
    logging.debug(f"Processing order {order_id}")
    if amount <= 0:
        logging.error(f"Invalid amount: {amount}")
        return False
    logging.info(f"Order {order_id} completed")
    return True
```

**Output:**
```
DEBUG: Processing order 123
INFO: Order 123 completed
```

**Log Levels (from lowest to highest):**
- `DEBUG` — Detailed info for debugging
- `INFO` — Confirmation things work
- `WARNING` — Something unexpected
- `ERROR` — Serious problem
- `CRITICAL` — Severe error

**Limitations:**
- More setup than `print()`
- Still doesn't pause execution
- Can be verbose if overused

**Why choose it:** Production-safe, configurable, can be enabled/disabled without code changes.

---

## 3. Assertions

**What it is:** Checking that conditions are true — code stops if they're not.

**When to use it:**
- Validating assumptions (e.g., "this should never be negative")
- Testing invariants (things that should always be true)
- Catching bugs early in development
- **Not** for user input validation!

**Example:**
```python
def set_temperature(temp):
    assert temp >= -273.15, "Temperature below absolute zero!"
    assert temp <= 1000, "Temperature too high!"
    print(f"Temperature set to {temp}°C")

set_temperature(25)    # Works
set_temperature(-300)  # AssertionError!
```

**Limitations:**
- Can be disabled with `python -O` (optimization mode)
- Stops execution immediately (no graceful handling)
- Not for runtime errors (use exceptions instead)

**Why choose it:** Catches programmer errors early, self-documenting.

---

## 4. Python Debugger (pdb)

**What it is:** Interactive debugger that pauses execution and lets you inspect variables.

**When to use it:**
- Complex bugs where you need to step through code
- When you need to see the call stack
- Exploring unfamiliar code
- When `print()` isn't enough

**Starting the debugger:**

**Method 1: Add breakpoint in code**
```python
import pdb

def calculate_average(numbers):
    pdb.set_trace()  # Pause here
    total = sum(numbers)
    count = len(numbers)
    return total / count

calculate_average([10, 20, 30])
```

**Method 2: Run script with pdb**
```bash
python -m pdb script.py
```

**Method 3: Breakpoint by line number**
```bash
python -m pdb -c "break 5" script.py
```

**Common pdb commands:**

| Command | Description |
|---------|-------------|
| `n` (next) | Execute next line |
| `s` (step) | Step into a function |
| `c` (continue) | Continue until next breakpoint |
| `p variable` | Print a variable's value |
| `l` (list) | Show current code |
| `q` (quit) | Exit debugger |
| `h` (help) | Show help |

**Example session:**
```bash
$ python -m pdb script.py
> /path/script.py(1)<module>()
-> import pdb

(Pdb) n
> /path/script.py(2)<module>()
-> def calculate_average(numbers):

(Pdb) c
```

**Limitations:**
- Slows down execution
- Requires interaction (can't use in production)
- Can be confusing for beginners
- Code runs differently than normal

**Why choose it:** Full control, can explore any variable, step through logic.

---

## 5. IDE Debugger

**What it is:** Visual debugger with breakpoints, variable panels, and step controls.

**When to use it:**
- Complex applications with multiple files
- When you want a visual interface
- Team collaboration (easier to show others)
- Daily development work

### Setting Up Breakpoints:

**In any IDE:**
1. Click to the left of a line number to add a breakpoint (red dot)
2. Run the code in debug mode
3. Execution pauses at the breakpoint
4. Inspect variables in the debug panel
5. Use controls: Continue, Step Over, Step Into, Step Out

**Common IDEs:**
- VSCode — Free, highly customisable
- PyCharm — Built specifically for Python
- Sublime Text — Lightweight with plugins

**Limitations:**
- Requires IDE setup
- Can be overwhelming for simple scripts
- Project-specific configuration

**Why choose it:** Visual, interactive, best for complex debugging.

---

## Decision Tree: Which to Use?

```
Need to debug?
    │
    ├─→ Quick value check? → print()
    │
    ├─→ Production code? → logging
    │
    ├─→ Validate assumption? → assert
    │
    ├─→ Complex logic bug? → pdb or IDE debugger
    │
    └─→ Multi-file application? → IDE debugger
```

---

## Common Debugging Scenarios

### Scenario 1: "Why is this value wrong?"
**Use:** `print()` or IDE breakpoint
```python
# Quick check
print(f"Expected: {expected}, Got: {actual}")

# Or IDE: Set breakpoint, inspect variables visually
```

### Scenario 2: "Code crashes somewhere"
**Use:** IDE debugger with breakpoints
- Set breakpoint at start
- Step through until crash
- Inspect variables at each step

### Scenario 3: "Bug only happens sometimes"
**Use:** `logging`
- Log events leading up to the bug
- Review logs to find pattern

### Scenario 4: "Function returns unexpected result"
**Use:** `assert` for validation
```python
def divide(a, b):
    assert b != 0, "Can't divide by zero!"
    return a / b
```

### Scenario 5: "I don't understand this code"
**Use:** IDE debugger or `pdb`
- Step through line by line
- Watch how variables change

---

## Pro Tips

1. **Start simple:** Try `print()` first, escalate if needed
2. **Don't over-debug:** Sometimes reading the error message carefully is enough
3. **Use meaningful messages:** `print("HERE")` is useless; `print(f"User ID: {user_id}")` is helpful
4. **Remove debug code:** `print()` statements should be temporary
5. **Learn keyboard shortcuts:** Saves tons of time in IDE debugger

---

## Practice Exercise

**Scenario:** You've inherited a buggy calculator function from a coworker!

**Your task:**
1. Create a file called `debug_practice.py`
2. Copy the buggy function below into it
3. Use `print()` statements to find where the bug is
4. Once found, fix the bug
5. Test with the provided test cases

**Buggy code:**
```python
def calculate_statistics(numbers):
    """Calculate sum, average, and max of a list."""
    total = sum(numbers)
    average = total / len(numbers)
    maximum = max(numbers)
    
    return {
        "sum": total,
        "average": average,
        "max": maximum
    }

# Test cases
result = calculate_statistics([10, 20, 30])
print(f"Result: {result}")
```

**Test cases to try:**
1. `[10, 20, 30]` — Expected: sum=60, average=20, max=30
2. `[5, 5, 5, 5]` — Expected: sum=20, average=5, max=5
3. `[100]` — Expected: sum=100, average=100, max=100

**Debugging steps:**
1. Add `print()` statements to show intermediate values
2. Run the code and compare output to expected
3. Identify which calculation is wrong
4. Fix the bug
5. Remove debug prints when done

**Try it yourself first!** Scroll down when ready.

---

## Solutions

```python
def calculate_statistics(numbers):
    """Calculate sum, average, and max of a list."""
    # Debug prints (remove when done!)
    print(f"Input: {numbers}")
    print(f"Sum: {sum(numbers)}")
    print(f"Length: {len(numbers)}")
    
    total = sum(numbers)
    average = total / len(numbers)
    maximum = max(numbers)
    
    print(f"Average: {average}")
    print(f"Max: {maximum}")
    
    return {
        "sum": total,
        "average": average,
        "max": maximum
    }

# Test cases
result = calculate_statistics([10, 20, 30])
print(f"Result: {result}")
```

**Expected output:**
```
Input: [10, 20, 30]
Sum: 60
Length: 3
Average: 20.0
Max: 30
Result: {'sum': 60, 'average': 20.0, 'max': 30}
```

**Note:** This code actually works correctly! The exercise is to practice adding debug prints to verify the logic.

---

## Quick Recap

- **`print()`** — Quick, simple, temporary
- **`logging`** — Production-safe, configurable
- **`assert`** — Validate assumptions, catch errors early
- **`pdb`** — Interactive debugging, step through code
- **IDE debugger** — Visual, best for complex projects
- **Breakpoints** — Manual (add `pdb.set_trace()` or click in IDE)
- **Decision tree** — Start simple, escalate as needed

---

## What's Next?

Ready for more? Continue to **[Lesson 19: Working with Databases](19-working-with-databases.md)** — learn to use SQLite and SQLAlchemy! 🗄️
