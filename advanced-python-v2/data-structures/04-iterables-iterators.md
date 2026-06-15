# Data Structures Lesson 4: Iterables & Iterators 🔄

**← Back to [Lesson 3: Deque](03-deque.md)**

---

## The Question Behind Every For-Loop

You've written `for item in collection:` hundreds of times. It works on lists, strings, dicts, files, queues, stacks, everything.

But HOW? How does `for` know how to get the next item? How does it know when to stop?

The answer: **iterators**.

---

## Iterable vs Iterator — The Crucial Distinction

- An **iterable** is something you CAN loop over (a list, a string, a file)
- An **iterator** is the thing that DOES the looping — it keeps track of where you are

Think of a book:
- The **book** is the iterable — you can read it
- A **bookmark** is the iterator — it remembers which page you're on

You can have multiple bookmarks in the same book. Each one tracks a different position. When you finish the book, the bookmark is done — it can't go further.

---

## What `for` Actually Does

This:

```python
for item in [1, 2, 3]:
    print(item)
```

Is secretly this:

```python
# Python creates an iterator from the iterable
iterator = iter([1, 2, 3])

# Then it calls next() repeatedly
while True:
    try:
        item = next(iterator)
        print(item)
    except StopIteration:
        break  # Iterator is exhausted — stop the loop
```

`iter()` creates the iterator. `next()` advances it. `StopIteration` signals "no more items."

---

## Seeing It In Action

```python
numbers = [1, 2, 3]

# A list is ITERABLE but NOT an iterator
# next(numbers)  # ❌ TypeError — 'list' object is not an iterator

# iter() CREATES an iterator
it = iter(numbers)

print(next(it))  # 1
print(next(it))  # 2
print(next(it))  # 3
# print(next(it))  # ❌ StopIteration — nothing left!

# You can create multiple iterators — each starts fresh
it2 = iter(numbers)
print(next(it2))  # 1 — brand new start!
```

**Key insight:** Iterables are reusable (loop over them many times). Iterators are exhaustible (once consumed, they're done).

---

## Generators: Iterators Made Easy

Writing a full iterator class is tedious. Python has a shortcut: **generators**.

A generator is a function that uses `yield` instead of `return`:

```python
# A regular function — returns once
def get_numbers():
    return [1, 2, 3]  # Creates the whole list at once, returns it

# A generator — yields values one at a time
def count_up_to(limit):
    n = 1
    while n <= limit:
        yield n      # Pauses here, remembers where it was
        n += 1


# Calling a generator creates a generator object (which IS an iterator!)
counter = count_up_to(3)
print(type(counter))  # <class 'generator'>

print(next(counter))  # 1 — runs until first yield
print(next(counter))  # 2 — resumes after yield, runs until next yield
print(next(counter))  # 3
# print(next(counter))  # StopIteration

# For-loops consume generators automatically:
for num in count_up_to(5):
    print(num, end=" ")  # 1 2 3 4 5
```

**`yield` is like `return`, but it PAUSES the function instead of ending it.** When `next()` is called again, it resumes right where it left off.

---

## Why Generators Matter: Memory

```python
# This creates a list of 10 MILLION numbers in memory at once
# big_list = [x for x in range(10_000_000)]  # ~80 MB!

# This creates them one at a time — almost no memory
big_gen = (x for x in range(10_000_000))  # Generator expression

# Process one at a time:
total = sum(big_gen)  # Works, even on 10M items
```

Generator expressions look like list comprehensions but use `()` instead of `[]`:

```python
squares_list = [x**2 for x in range(1000)]   # List — computed now, stored in memory
squares_gen  = (x**2 for x in range(1000))   # Generator — computed on demand
```

---

## A Practical Generator: Reading a Big File

```python
def find_errors(log_file):
    """Read a log file line by line, yielding only error lines."""
    with open(log_file) as f:
        for line in f:
            if "ERROR" in line:
                yield line.strip()


# Even if the file is 10GB, only one line is in memory at a time
for error in find_errors("server.log"):
    print(f"Found error: {error}")
```

---

## Practice: A Fibonacci Generator

**Your task:** Write a generator that produces Fibonacci numbers — forever or up to a limit.

1. `fibonacci()` — yields Fibonacci numbers endlessly: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34...
2. `first_n_fib(n)` — returns the first n Fibonacci numbers using your generator

**Test it:**

```python
for num in first_n_fib(10):
    print(num, end=" ")
# 0 1 1 2 3 5 8 13 21 34
```

Then try: what's the 100th Fibonacci number? You can compute it instantly because you're generating one at a time, not storing them all.

Create `fibonacci.py` and try it!

---

## Solution

```python
def fibonacci():
    """Generate Fibonacci numbers forever."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def first_n_fib(n):
    """Return the first n Fibonacci numbers."""
    result = []
    fib = fibonacci()
    for _ in range(n):
        result.append(next(fib))
    return result


# Test
print("First 10 Fibonacci numbers:")
for num in first_n_fib(10):
    print(num, end=" ")
print()

# The 100th Fibonacci number
fib = fibonacci()
for _ in range(100):
    value = next(fib)
print(f"\n100th Fibonacci: {value}")
# 218922995834555169026 — computed in microseconds, not stored in memory
```

---

## What You Just Learned

- **Iterable** = something you can loop over (has `__iter__`)
- **Iterator** = the thing doing the looping (has `__next__`)
- **`iter()`** creates an iterator, **`next()`** advances it
- **`StopIteration`** signals "done"
- **Generators** = functions with `yield` — easy iterators
- **Generator expressions** = `(x for x in ...)` — lazy, memory-efficient

---

This wraps up the data structures intro. You now have:

- **Stacks** (LIFO) — undo/redo, back button
- **Queues** (FIFO) — print jobs, ticket systems
- **Deques** (both ends) — clipboard history, recent items
- **Iterables & Generators** — how `for` works, lazy evaluation

---

## What's Next?

These are the building blocks. From here, the curriculum continues with decorators, recursion, linked lists, trees, and sorting — but take your time. These four data structure lessons and the OOP lessons are already a solid foundation.

When you're ready: **decorators** — functions that wrap other functions to add behaviour. It's the last "big idea" before we dive into algorithms.

---

**Your turn:** Build the Fibonacci generator! Then write an `even_fibonacci()` generator that only yields even Fibonacci numbers (0, 2, 8, 34...). 🔄💛
