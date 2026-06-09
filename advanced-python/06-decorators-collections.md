# Advanced Python Lesson 6: Decorators & Collections 🎀

**← Back to [Lesson 5: Iterables & Iterators](05-iterables-iterators.md)**

---

## What Are Decorators?

**Plain English:** A decorator is a function that takes another function, wraps it in extra behaviour, and returns the wrapped version — without modifying the original function's code. You apply it with `@`.

**Real-world analogy:** Gift wrapping:
- The **gift** inside is the original function — it still does its job
- The **wrapping paper** is the decorator — it adds something extra (logging, timing, access control)
- The **box** you hand over is the wrapped function — same gift, better presentation
- You can wrap a gift in multiple layers — tissue, paper, ribbon — each adding something

---

## The `@` Syntax — Just Sugar

These two are **exactly the same**:

```python
# Without @ syntax
def greet():
    print("Hello!")
greet = log_call(greet)

# With @ syntax — cleaner!
@log_call
def greet():
    print("Hello!")
```

---

## Writing Your First Decorator

```python
def announce(func):
    """Prints 'Calling...' before and 'Done!' after any function."""
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}...")
        result = func(*args, **kwargs)
        print("Done!")
        return result
    return wrapper

@announce
def calculate_total(items):
    return sum(items)

calculate_total([1, 2, 3])
# Calling calculate_total...
# Done!
# 6
```

**What's happening:**
1. `announce` receives `calculate_total` as an argument
2. It defines `wrapper` — a new function that calls the original
3. It returns `wrapper`, and `calculate_total` is **replaced** by `wrapper`
4. Every call to `calculate_total` now goes through `wrapper` first

---

## `*args, **kwargs` — The Secret Sauce

Without them, your decorator would only work on functions with a specific signature:

```python
# ❌ Only works on functions with no arguments
def bad_decorator(func):
    def wrapper():          # Can't pass arguments through!
        print("Before")
        result = func()     # Can't receive arguments!
        print("After")
        return result
    return wrapper

# ✅ Works on ANY function
def good_decorator(func):
    def wrapper(*args, **kwargs):   # Collects everything
        print("Before")
        result = func(*args, **kwargs)  # Passes everything through
        print("After")
        return result
    return wrapper
```

---

## `functools.wraps` — Preserving Identity

Without `@wraps`, the decorated function loses its name and docstring:

```python
from functools import wraps

def without_wraps(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def with_wraps(func):
    @wraps(func)             # ← This preserves the original's metadata
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@without_wraps
def say_hi():
    """A friendly greeting."""
    pass

print(say_hi.__name__)  # 'wrapper'  — lost!
print(say_hi.__doc__)   # None       — gone!

@with_wraps
def say_hello():
    """A friendly greeting."""
    pass

print(say_hello.__name__)  # 'say_hello'  — preserved!
print(say_hello.__doc__)   # 'A friendly greeting.'  — intact!
```

**Rule of thumb:** Always use `@wraps` in your decorators!

---

## Practical Decorator Patterns

### 1. Timing Decorator

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_calculation(n):
    total = 0
    for i in range(n):
        total += i ** 2
    return total
```

### 2. Retry Decorator

```python
def retry(max_attempts=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise  # All attempts failed — give up
                    print(f"Attempt {attempt} failed, retrying...")
            return None
        return wrapper
    return decorator

@retry(max_attempts=3)
def fetch_data(url):
    # Imagine this might fail sometimes...
    pass
```

### 3. Cache / Memoize Decorator

```python
def memoize(func):
    """Remember results — if you've seen these arguments before, skip the work."""
    cache = {}

    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper

@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))  # Instant — would take years without memoization!
```

---

## Decorators with Arguments

When your decorator _itself_ needs parameters, you add another layer:

```python
def repeat(times):
    """Run a function multiple times."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def cheer(name):
    print(f"Go {name}!")

cheer("Szonja")
# Go Szonja!
# Go Szonja!
# Go Szonja!
```

**Three layers:** `repeat(times)` → `decorator(func)` → `wrapper(*args, **kwargs)`

---

## Built-in Decorators You Already Know

| Decorator | What it does |
|-----------|-------------|
| `@staticmethod` | Method that doesn't need `self` — just a namespaced function |
| `@classmethod` | Method that receives the _class_ (`cls`) as first argument |
| `@property` | Turn a method into an attribute — getter without `()` |
| `@<name>.setter` | Setter for a `@property` |
| `@functools.lru_cache` | Built-in memoization — way more powerful than our simple one! |

---

## Part 2: The `collections` Module

Python's `collections` module gives you specialised container types beyond plain lists and dicts.

---

### `namedtuple` — Lightweight Classes with Less Boilerplate

```python
from collections import namedtuple

# No class definition needed — just name the fields!
Book = namedtuple('Book', ['title', 'author', 'year', 'rating'])

lotr = Book('The Lord of the Rings', 'J.R.R. Tolkien', 1954, 5.0)

# Access by name (like an object) or by index (like a tuple)
print(lotr.title)    # The Lord of the Rings
print(lotr[1])       # J.R.R. Tolkien
print(lotr.rating)   # 5.0

# Immutable — you can't accidentally change it
# lotr.rating = 4.5  # ❌ AttributeError!

# Built-in pretty printing
print(lotr)
# Book(title='The Lord of the Rings', author='J.R.R. Tolkien', year=1954, rating=5.0)
```

**When to use:** Data records that shouldn't change — coordinates, database rows, API responses.

---

### `defaultdict` — No More KeyError

```python
from collections import defaultdict

# The old way — always checking
word_counts = {}
for word in "the quick brown fox jumps over the lazy dog".split():
    if word not in word_counts:
        word_counts[word] = 0
    word_counts[word] += 1

# defaultdict — it auto-creates missing keys!
word_counts = defaultdict(int)     # Missing keys default to 0
for word in "the quick brown fox jumps over the lazy dog".split():
    word_counts[word] += 1         # No check needed!

print(dict(word_counts))
# {'the': 2, 'quick': 1, 'brown': 1, ...}

# Other useful defaults:
by_category = defaultdict(list)    # Missing → empty list
user_scores = defaultdict(lambda: 0)  # Missing → 0 with a lambda
nested = defaultdict(dict)         # Missing → empty dict (nested dicts!)
```

---

### `Counter` — Count Anything, Instantly

```python
from collections import Counter

# Count anything iterable
words = "the quick brown fox the lazy dog the fox".split()
counts = Counter(words)
print(counts)
# Counter({'the': 3, 'fox': 2, 'quick': 1, 'brown': 1, 'lazy': 1, 'dog': 1})

# Most common items
print(counts.most_common(2))  # [('the', 3), ('fox', 2)]

# Count individual characters
letter_counts = Counter("mississippi")
print(letter_counts)
# Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})

# Math with Counters!
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(c1 + c2)   # Counter({'a': 4, 'b': 3})
print(c1 - c2)   # Counter({'a': 2})  — b removed (would be negative)
print(c1 & c2)   # Counter({'a': 1, 'b': 1})  — intersection (min)
print(c1 | c2)   # Counter({'a': 3, 'b': 2})  — union (max)
```

---

### `OrderedDict` — A Dict That Remembers Insertion Order

Since Python 3.7, regular dicts remember order too. But `OrderedDict` has extra tricks:

```python
from collections import OrderedDict

od = OrderedDict()
od['z'] = 'last alphabetically'
od['a'] = 'first alphabetically'
od['m'] = 'middle'

# move_to_end — great for LRU caches!
od.move_to_end('a')   # Move to end (least recently used)
print(list(od.keys()))  # ['z', 'm', 'a']

od.move_to_end('z', last=False)  # Move to front (most recently used)
print(list(od.keys()))  # ['z', 'm', 'a']
```

---

### `ChainMap` — Search Through Multiple Dicts

```python
from collections import ChainMap

# Imagine: config with layers of precedence
defaults = {'theme': 'light', 'font_size': 12, 'debug': False}
user_settings = {'theme': 'dark', 'font_size': 14}
session_overrides = {'debug': True}

config = ChainMap(session_overrides, user_settings, defaults)

print(config['theme'])      # 'dark'  — from user_settings (first match wins)
print(config['font_size'])  # 14      — from user_settings
print(config['debug'])      # True    — from session_overrides

# Modify the first mapping only
config['theme'] = 'ocean'
print(session_overrides)  # {'debug': True, 'theme': 'ocean'}
# defaults and user_settings unchanged!
```

---

## Practice Exercise: Logging API with Decorators

### The Problem

Build an `@api_log` decorator and use `collections` to analyse API call patterns.

You're building a simple API handler. Each function represents an API endpoint. You need to:

1. Write an `@api_log` decorator that:
   - Prints `"API CALL: {function_name} with args={args}"` before the call
   - Prints `"API CALL: {function_name} returned {result}"` after the call
   - Times how long the call took and prints the duration
   - Uses `@wraps` to preserve function metadata

2. Write a `@count_calls` class-based decorator that:
   - Tracks how many times each decorated function is called
   - Stores the counts in a `Counter`
   - Has a `report()` class method that prints statistics

3. Build these endpoints and analyse them:
   - `get_user(user_id)` → returns `{"id": user_id, "name": "Test User"}`
   - `create_post(title, content)` → returns `{"id": 42, "title": title}`
   - `search_posts(query)` → returns `[]`

4. Call the endpoints multiple times with different arguments, then print a summary report using `Counter` and `defaultdict` to show:
   - Total calls per endpoint
   - Most common arguments per endpoint
   - Average response time per endpoint

---

## Solution

```python
import time
from functools import wraps
from collections import Counter, defaultdict


# === Part 1: @api_log decorator ===

def api_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        print(f"API CALL: {func_name} with args={args}")

        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start

        print(f"API CALL: {func_name} returned {result}")
        print(f"API CALL: {func_name} took {elapsed:.4f}s")
        return result
    return wrapper


# === Part 2: @count_calls class-based decorator ===

class count_calls:
    """Tracks call statistics across all decorated functions."""
    counters = Counter()      # call counts per function
    timings = defaultdict(list)  # response times per function
    args_seen = defaultdict(Counter)  # most common args per function

    def __init__(self, func):
        self.func = func
        wraps(func)(self)     # Preserve metadata

    def __call__(self, *args, **kwargs):
        name = self.func.__name__
        self.counters[name] += 1
        self.args_seen[name][args] += 1

        start = time.time()
        result = self.func(*args, **kwargs)
        elapsed = time.time() - start

        self.timings[name].append(elapsed)
        return result

    @classmethod
    def report(cls):
        print("\n📊 API CALL REPORT")
        print("=" * 50)

        for func_name, count in cls.counters.most_common():
            avg_time = sum(cls.timings[func_name]) / len(cls.timings[func_name])
            print(f"\n{func_name}:")
            print(f"  Total calls: {count}")
            print(f"  Avg response time: {avg_time:.4f}s")

            top_args = cls.args_seen[func_name].most_common(3)
            if top_args:
                print(f"  Most common arguments:")
                for args, n in top_args:
                    print(f"    {args} — {n}×")


# === Part 3: The API endpoints ===

@api_log
@count_calls
def get_user(user_id):
    """Fetch a user by ID."""
    time.sleep(0.01 * user_id)  # Simulate varying load
    return {"id": user_id, "name": "Szonja"}


@api_log
@count_calls
def create_post(title, content):
    """Create a new post."""
    time.sleep(0.02)
    return {"id": 42, "title": title, "content": content}


@api_log
@count_calls
def search_posts(query):
    """Search for posts."""
    time.sleep(0.015)
    return []


# === Part 4: Run it and analyse ===

if __name__ == "__main__":
    # Simulate API traffic
    get_user(1)
    get_user(1)      # Same call twice
    get_user(2)
    get_user(1)      # Three times with user_id=1!

    create_post("Hello", "First post!")
    create_post("Hello", "First post!")  # Duplicate post
    create_post("Python Tips", "Use decorators!")

    search_posts("decorators")
    search_posts("python")
    search_posts("python")  # Same search twice

    # Print the summary
    count_calls.report()
```

**Sample output:**
```
API CALL: get_user with args=(1,)
API CALL: get_user returned {'id': 1, 'name': 'Szonja'}
API CALL: get_user took 0.0102s
...

📊 API CALL REPORT
==================================================

get_user:
  Total calls: 4
  Avg response time: 0.0153s
  Most common arguments:
    (1,) — 3×
    (2,) — 1×

create_post:
  Total calls: 3
  Avg response time: 0.0201s
  Most common arguments:
    ('Hello', 'First post!') — 2×
    ('Python Tips', 'Use decorators!') — 1×

search_posts:
  Total calls: 3
  Avg response time: 0.0150s
  Most common arguments:
    ('python',) — 2×
    ('decorators',) — 1×
```

---

## Quick Recap

- **Decorator** — a function that wraps another function to add behaviour
- **`@decorator`** — syntactic sugar for `func = decorator(func)`
- **`*args, **kwargs`** — makes your decorator work on any function
- **`@wraps`** — always use it! Preserves name, docstring, and metadata
- **Three-layer decorators** — when you need arguments: `@decorator(arg)`
- **`namedtuple`** — lightweight, immutable data records
- **`defaultdict`** — no more KeyError; auto-creates missing values
- **`Counter`** — count anything, get `most_common()`, do counter math
- **`OrderedDict`** — dict with `move_to_end()` for LRU caches
- **`ChainMap`** — search multiple dicts as one; modify only the first

---

## What's Next?

You've added two of Python's most elegant tools to your toolkit — decorators for wrapping behaviour, and collections for specialised containers. Now let's bridge two concepts you've seen separately: hashing and recursion. Continue to **[Lesson 7: Hashing & Recursion](07-hashing-recursion.md)** 🔐

---

**Your turn:** Build the logging API! Then try adding a `@rate_limit(max_per_second=2)` decorator that prevents a function from being called more than `max_per_second` times per second (hint: use `time.time()` and a `defaultdict(list)` to track timestamps). 🎀💛
