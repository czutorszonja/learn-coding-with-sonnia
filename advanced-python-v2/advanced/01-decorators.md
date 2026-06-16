# Advanced: Decorators 🎀

**← Back to [Bridge Lesson 3: Property Basics](../bridge/03-property-basics.md)**

---

## The Problem: "I Wish I Could Just Add This to Every Function"

Imagine you're building an app and you want to log every time a function is called:

```python
def add(a, b):
    print(f"Called: add({a}, {b})")
    return a + b

def multiply(a, b):
    print(f"Called: multiply({a}, {b})")
    return a * b
```

This works, but there's a problem:
- You're **mixing logging code with business logic** — the function does TWO things now
- If you have 50 functions, you're copy-pasting the same `print` line everywhere
- If you want to change the log format later, you have to edit every single function

What if you could write the logging logic once and just... stick it onto any function? Like a stamp?

That's exactly what decorators are.

---

## The Idea: Wrapping a Function

A decorator is a **function that takes another function and extends it**. It's like putting a gift box around your function — the gift is still there, but now it has wrapping paper with extras.

```python
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Returned: {result}")
        return result
    return wrapper


# Now apply it:
def add(a, b):
    return a + b

# Wrap it:
add = logger(add)

print(add(3, 4))
# Calling: add
# Returned: 7
# 7
```

`logger` is a decorator. It creates a new function (`wrapper`) that adds behaviour before and after the original function, then returns that wrapper.

The key insight: **`add = logger(add)` replaces your function with a wrapped version.** The original logic is preserved, but now it comes with extras.

---

## The `@` Syntax — Sugar

Python has a shorthand for `add = logger(add)`:

```python
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@logger
def add(a, b):
    return a + b

@logger
def greet(name):
    return f"Hello, {name}!"
```

The `@logger` above the function definition is exactly equivalent to `add = logger(add)`. It runs at definition time — when Python reads that line, it decorates the function immediately.

---

## Reading Decorators From Inside Out

The syntax can feel backwards at first. When you see:

```python
@logger
def add(a, b):
    return a + b
```

Read it as: **"`add` passes through `logger`"** or **"`logger` wraps `add`"**.

The `@` line lives ABOVE the function, but it's saying "after creating this function, run it through the decorator." It helps to remember that `@logger` is just fancy syntax for `add = logger(add)`.

---

## Real-World Example: Timing

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_sum(n):
    total = 0
    for i in range(n):
        total += i
    return total

print(slow_sum(10_000_000))
# slow_sum took 0.2842s
# 49999995000000
```

Now you can time ANY function by adding one line above it. No copy-paste, no mixed logic.

---

## Decorators With Arguments

What if you want to customise your decorator? Say, a delay that's configurable:

```python
import time

def delay(seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"Waiting {seconds}s...")
            time.sleep(seconds)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@delay(2)
def greet(name):
    return f"Hello, {name}!"

print(greet("Szonja"))
# Waiting 2s...
# Hello, Szonja!
```

This is a **decorator factory** — `delay(2)` returns the actual decorator. The `@` applies whatever `delay(2)` returns.

Trace it:

```
@delay(2)
→ delay(2) returns `decorator`
→ @decorator wraps `greet`
→ `greet` is now the `wrapper` with `seconds=2`
```

---

## Common Decorators You've Already Used

Python has several built-in decorators:

- **`@property`** — you already met this in Bridge 3. It makes a method look like a plain attribute.
- **`@staticmethod`** — a method that doesn't need `self` (belongs to the class, not the instance)
- **`@classmethod`** — a method that gets the class instead of the instance

```python
class Pizza:
    def __init__(self, toppings):
        self.toppings = toppings

    @staticmethod
    def calculate_calories(radius):
        """Doesn't need self — it's just a utility for the class."""
        return 40 * 3.14 * radius ** 2

    @classmethod
    def margherita(cls):
        """Creates a default Pizza without the caller needing to know the constructor."""
        return cls(["mozzarella", "tomato", "basil"])

pizza = Pizza.margherita()
print(pizza.toppings)  # ['mozzarella', 'tomato', 'basil']
```

But the most common one by far is `@property`.

---

## A Tiny Implementation Detail: `functools.wraps`

There's one small problem with decorators as written above:

```python
@logger
def add(a, b):
    return a + b

print(add.__name__)  # 'wrapper' — not 'add'!
```

The `wrapper` function has replaced the original, so Python thinks the function is now called "wrapper". This can break tools that read function names.

The fix is a one-liner:

```python
import functools

def logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@logger
def add(a, b):
    return a + b

print(add.__name__)  # 'add' ✅
```

`functools.wraps` copies the name, docstring, and other metadata from the original function to the wrapper. It's a decorator for your decorator. Use it as a habit.

---

## Practice: An `@on_message` Decorator

**Your task:** You're building a simple bot framework. Create a `Bot` class that:

1. Has a dictionary to store command handlers
2. Has a method `on_message(command)` that returns a decorator
3. The decorator registers the handler function under that command

**Example usage:**

```python
bot = Bot()

@bot.on_message("hello")
def handle_hello(name):
    return f"Hey there, {name}! 👋"

@bot.on_message("goodbye")
def handle_goodbye(name):
    return f"See you, {name}! 💛"

# Simulate messages:
print(bot.process("hello", "Szonja"))
print(bot.process("goodbye", "Szonja"))
print(bot.process("unknown", "Szonja"))
```

**Expected output:**
```
Hey there, Szonja! 👋
See you, Szonja! 💛
I don't understand "unknown"
```

The `Bot.on_message("hello")` decorator should register `handle_hello` under the key `"hello"`. When `process("hello", "Szonja")` is called, it looks up the handler and calls it with `"Szonja"`.

Save this as `bot.py` and try it! The solution is below.

---

## Solution

```python
import functools

class Bot:
    def __init__(self):
        self.handlers = {}

    def on_message(self, command):
        """Decorator factory — registers a function for a command."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            self.handlers[command] = func
            return wrapper
        return decorator

    def process(self, command, *args, **kwargs):
        if command in self.handlers:
            return self.handlers[command](*args, **kwargs)
        return f'I don\'t understand "{command}"'


bot = Bot()

@bot.on_message("hello")
def handle_hello(name):
    return f"Hey there, {name}! 👋"

@bot.on_message("goodbye")
def handle_goodbye(name):
    return f"See you, {name}! 💛"

print(bot.process("hello", "Szonja"))
print(bot.process("goodbye", "Szonja"))
print(bot.process("unknown", "Szonja"))
```

Notice: the `wrapper` isn't strictly necessary here (the decorator could just register `func` directly), but keeping the pattern consistent makes it easier when you later add logging, timing, or other wrapper behaviour.

---

## What You Just Learned

- **A decorator** = a function that wraps another function to extend it
- **`@decorator`** is sugar for `func = decorator(func)`
- **Decorator factories** = functions that accept arguments and return a decorator
- **`@functools.wraps`** preserves the original function's metadata
- Decorators keep your code **DRY** — one wrapping, many applications

---

## What's Next?

Decorators are one of those ideas that seem abstract until you use them a couple of times, then suddenly they're everywhere. They're the last "big language feature" before we shift into algorithmic thinking.

Next up: **[Recursion](../algorithms/01-recursion.md)** — functions that call themselves 🔄

---

**Trust yourself on this one.** If the `@` syntax feels weird at first, it's because it IS weird — it's the only place in Python where something below a line affects something above it. You'll get used to it. 💛
