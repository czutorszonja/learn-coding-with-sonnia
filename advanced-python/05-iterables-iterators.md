# Advanced Python Lesson 5: Iterables & Iterators 🔄

**← Back to [Lesson 4: Deque](04-deque.md)**

---

## What Are Iterables and Iterators?

**Plain English:** An _iterable_ is anything you can loop over. An _iterator_ is the thing that actually does the looping — it keeps track of where you are and gives you the next item each time you ask.

**Real-world analogy:** A book:
- The **book** (iterable) — you can read it from start to finish
- A **bookmark** (iterator) — it remembers where you are, and each time you come back, you read the next page
- You can have **multiple bookmarks** in the same book — each at a different position
- When you finish the book, the bookmark can't go any further

---

## The Iterator Protocol

Two magic methods make iteration work:

```python
class Something:
    def __iter__(self):
        """Return an iterator object. Called once at the start of a for-loop."""
        return self._iterator

    def __next__(self):
        """Return the next item. Raises StopIteration when done."""
        if no_more_items:
            raise StopIteration
        return next_item
```

**The `for` loop is just syntactic sugar:**

```python
# This:
for item in my_list:
    print(item)

# Is equivalent to:
iterator = iter(my_list)       # Calls __iter__()
while True:
    try:
        item = next(iterator)  # Calls __next__()
        print(item)
    except StopIteration:
        break
```

---

## Iterable vs Iterator — The Crucial Distinction

```python
# A LIST is ITERABLE but NOT an iterator
my_list = [1, 2, 3]
# next(my_list)  # ❌ TypeError: 'list' object is not an iterator

# iter() CREATES an iterator FROM an iterable
iterator = iter(my_list)
print(next(iterator))  # 1
print(next(iterator))  # 2
print(next(iterator))  # 3
# print(next(iterator))  # ❌ StopIteration

# You can create MULTIPLE iterators from the same iterable
iterator2 = iter(my_list)
print(next(iterator2))  # 1 — fresh start!
```

**Key insight:** Iterables are _reusable_ (you can loop over them many times). Iterators are _exhaustible_ (once consumed, they're done).

---

## Building a Custom Iterator

```python
class Countdown:
    """An iterator that counts down from n to 1."""

    def __init__(self, start):
        self._current = start

    def __iter__(self):
        """Iterators return themselves — they ARE their own iterator."""
        return self

    def __next__(self):
        if self._current <= 0:
            raise StopIteration
        value = self._current
        self._current -= 1
        return value


# Using it with a for loop
for num in Countdown(5):
    print(num, end=" ")  # 5 4 3 2 1

# Using next() manually
cd = Countdown(3)
print(next(cd))  # 3
print(next(cd))  # 2
print(next(cd))  # 1
# print(next(cd))  # StopIteration
```

---

## Separating Iterable from Iterator (Better Design)

```python
class CountdownIterable:
    """An iterable that creates fresh Countdown iterators."""

    def __init__(self, start):
        self.start = start

    def __iter__(self):
        """Returns a NEW iterator each time — reusable!"""
        return CountdownIterator(self.start)


class CountdownIterator:
    """The actual iterator that tracks position."""

    def __init__(self, start):
        self._current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self._current <= 0:
            raise StopIteration
        value = self._current
        self._current -= 1
        return value


# Now we can loop multiple times!
cd = CountdownIterable(3)
print(list(cd))  # [3, 2, 1]
print(list(cd))  # [3, 2, 1] — reusable!
```

---

## Building a Range-Like Iterable

```python
class MyRange:
    """A simple reimplementation of range() — lazy and memory-efficient."""

    def __init__(self, start, stop=None, step=1):
        if stop is None:
            self.start = 0
            self.stop = start
        else:
            self.start = start
            self.stop = stop
        self.step = step

    def __iter__(self):
        return MyRangeIterator(self.start, self.stop, self.step)

    def __contains__(self, value):
        """Support 'in' operator — O(1)!"""
        if self.step > 0:
            return self.start <= value < self.stop and (value - self.start) % self.step == 0
        else:
            return self.stop < value <= self.start and (value - self.start) % self.step == 0

    def __len__(self):
        """Calculate length without generating all values."""
        if self.step > 0 and self.start >= self.stop:
            return 0
        if self.step < 0 and self.start <= self.stop:
            return 0
        return max(0, (self.stop - self.start + self.step - (1 if self.step > 0 else -1)) // self.step)

    def __getitem__(self, index):
        """Support indexing — r[5] works!"""
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError("MyRange index out of range")
        return self.start + index * self.step


class MyRangeIterator:
    def __init__(self, start, stop, step):
        self._current = start
        self._stop = stop
        self._step = step

    def __iter__(self):
        return self

    def __next__(self):
        if (self._step > 0 and self._current >= self._stop) or \
           (self._step < 0 and self._current <= self._stop):
            raise StopIteration
        value = self._current
        self._current += self._step
        return value


# Test it
r = MyRange(5)
print(list(r))       # [0, 1, 2, 3, 4]
print(list(r))       # [0, 1, 2, 3, 4] — reusable!

r2 = MyRange(2, 10, 2)
print(list(r2))      # [2, 4, 6, 8]
print(6 in r2)       # True
print(5 in r2)       # False
print(len(r2))       # 4
print(r2[2])         # 6 — indexing works!
```

---

## Generators — Iterators Made Easy

Writing `__iter__` and `__next__` by hand is tedious. **Generators** do it for you:

```python
def countdown_gen(start):
    """A generator function — uses 'yield' instead of 'return'."""
    while start > 0:
        yield start
        start -= 1


# Calling a generator function creates a generator object (an iterator!)
cd = countdown_gen(5)
print(type(cd))      # <class 'generator'>
print(next(cd))      # 5
print(next(cd))      # 4
print(list(cd))      # [3, 2, 1] — consumes the rest

# Generators are exhaustible
print(list(cd))      # [] — already consumed!
```

**`yield` is the magic word.** It:
1. Returns a value (like `return`)
2. Pauses the function (unlike `return` — state is preserved!)
3. Resumes from the same spot when `next()` is called again

---

## Generator Expressions

```python
# List comprehension — creates the whole list in memory
squares_list = [x**2 for x in range(1000000)]  # Memory: ~8MB

# Generator expression — lazy, creates values on demand
squares_gen = (x**2 for x in range(1000000))   # Memory: negligible

# Use generator expressions with any()/all()/sum()/min()/max()
print(sum(squares_gen))  # Processes one at a time, never stores all
```

---

## Real-World Generator Patterns

### 1. Infinite Sequences

```python
def fibonacci():
    """Generate Fibonacci numbers forever."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


fib = fibonacci()
for _ in range(10):
    print(next(fib), end=" ")  # 0 1 1 2 3 5 8 13 21 34
```

### 2. Reading Large Files Lazily

```python
def read_lines_lazy(filename):
    """Yield lines one at a time — never loads the whole file."""
    with open(filename) as f:
        for line in f:  # File objects are already iterators!
            yield line.strip()


# Process a 10GB file without loading it all
for line in read_lines_lazy("huge_file.txt"):
    if "ERROR" in line:
        print(line)
```

### 3. Pipeline of Generators

```python
def integers():
    """All natural numbers."""
    n = 1
    while True:
        yield n
        n += 1


def even_numbers(numbers):
    """Filter: only even numbers."""
    for n in numbers:
        if n % 2 == 0:
            yield n


def take(n, iterable):
    """Take the first n items from an iterable."""
    for i, item in enumerate(iterable):
        if i >= n:
            break
        yield item


# Compose them!
first_5_even = list(take(5, even_numbers(integers())))
print(first_5_even)  # [2, 4, 6, 8, 10]

# Memory-efficient pipeline — only one number exists at a time!
```

### 4. `yield from` — Delegating to Sub-Generators

```python
def flatten(nested_list):
    """Flatten a nested list using yield from."""
    for item in nested_list:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)  # Delegate to recursive call
        else:
            yield item


nested = [1, [2, 3], [4, [5, 6]], 7]
print(list(flatten(nested)))  # [1, 2, 3, 4, 5, 6, 7]
```

---

## The `itertools` Module — Your Iterator Toolbox

```python
import itertools

# ── Infinite iterators ──────────────
itertools.count(10, 2)     # 10, 12, 14, 16, ... (forever)
itertools.cycle('ABC')     # A, B, C, A, B, C, ... (forever)
itertools.repeat('Hi', 3)  # Hi, Hi, Hi

# ── Combining iterators ─────────────
itertools.chain('ABC', 'DEF')           # A, B, C, D, E, F
itertools.zip_longest('AB', '123', fillvalue='-')  # (A,1), (B,2), (-,3)

# ── Filtering ────────────────────────
itertools.takewhile(lambda x: x < 5, [1, 3, 5, 2, 4])   # 1, 3
itertools.dropwhile(lambda x: x < 5, [1, 3, 5, 2, 4])   # 5, 2, 4
itertools.filterfalse(lambda x: x % 2, range(10))        # 0, 2, 4, 6, 8

# ── Combinatorics ────────────────────
itertools.product('AB', '12')           # (A,1), (A,2), (B,1), (B,2)
itertools.permutations('ABC', 2)        # (A,B), (A,C), (B,A), (B,C), (C,A), (C,B)
itertools.combinations('ABC', 2)        # (A,B), (A,C), (B,C)

# ── Grouping ─────────────────────────
data = [('A', 1), ('A', 2), ('B', 3), ('B', 4)]
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"{key}: {list(group)}")
# A: [('A', 1), ('A', 2)]
# B: [('B', 3), ('B', 4)]

# ── Accumulation ─────────────────────
list(itertools.accumulate([1, 2, 3, 4]))  # [1, 3, 6, 10] (running sum)
```

---

## Python's Built-in Iteration Helpers

```python
# enumerate — index + value
for i, name in enumerate(['Alice', 'Bob', 'Charlie'], start=1):
    print(f"{i}. {name}")
# 1. Alice  2. Bob  3. Charlie

# zip — pair up iterables
names = ['Alice', 'Bob', 'Charlie']
scores = [85, 92, 78]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# reversed — reverse any sequence
for char in reversed("hello"):
    print(char)  # o, l, l, e, h

# sorted — returns a new sorted list (works on any iterable)
for num in sorted([3, 1, 4, 1, 5, 9]):
    print(num)  # 1, 1, 3, 4, 5, 9

# map — apply a function to every item
squared = map(lambda x: x**2, [1, 2, 3, 4])
print(list(squared))  # [1, 4, 9, 16]

# filter — keep items that match a condition
evens = filter(lambda x: x % 2 == 0, range(10))
print(list(evens))  # [0, 2, 4, 6, 8]
```

---

## Practice Exercise

**Scenario:** You're building a data processing pipeline that reads GitHub-like event data, filters, transforms, and aggregates it — all lazily, without loading everything into memory.

**Your task:**

1. Create `event_pipeline.py`

2. Build a pipeline of generators/iterators:

   ```python
   # Step 1: Event source (generator — simulates an API)
   def generate_events():
       """Yield events one at a time."""
       events = [
           {"type": "push", "user": "alice", "repo": "myproject", "files": 3},
           {"type": "issue", "user": "bob", "repo": "myproject", "title": "Bug report"},
           {"type": "push", "user": "alice", "repo": "other", "files": 7},
           {"type": "pr", "user": "charlie", "repo": "myproject", "files": 2},
           {"type": "push", "user": "bob", "repo": "other", "files": 1},
           {"type": "issue", "user": "alice", "repo": "other", "title": "Feature req"},
           {"type": "push", "user": "charlie", "repo": "myproject", "files": 5},
           {"type": "push", "user": "alice", "repo": "myproject", "files": 4},
       ]
       for event in events:
           yield event
   ```

3. Build these pipeline stages (each a generator!):
   - `filter_by_type(events, event_type)` — keep only events of a given type
   - `filter_by_user(events, user)` — keep only events by a given user
   - `count_files_changed(events)` — yield `(user, files)` tuples for push events
   - `aggregate_by_user(events)` — group and sum — yield `(user, total_files)` pairs

4. Write a `Pipeline` class that chains stages together:
   ```python
   pipeline = Pipeline(generate_events())
   pipeline.filter_by_type("push")
   pipeline.filter_by_user("alice")
   # Or: pipeline.filter_by_type("push").filter_by_user("alice")
   ```

5. Make the pipeline **lazy** — nothing runs until you iterate. Support `list()`, `sum()`, `next()`, and `for` loops.

6. Bonus: Add a `take(n)` stage that limits output to n items, and a `collect()` method that materialises the result.

**Try it yourself first!** Solution below.

---

## Solution

```python
from collections import defaultdict


def generate_events():
    """Simulate a stream of GitHub-like events."""
    events = [
        {"type": "push", "user": "alice", "repo": "myproject", "files": 3},
        {"type": "issue", "user": "bob", "repo": "myproject", "title": "Bug report"},
        {"type": "push", "user": "alice", "repo": "other", "files": 7},
        {"type": "pr", "user": "charlie", "repo": "myproject", "files": 2},
        {"type": "push", "user": "bob", "repo": "other", "files": 1},
        {"type": "issue", "user": "alice", "repo": "other", "title": "Feature req"},
        {"type": "push", "user": "charlie", "repo": "myproject", "files": 5},
        {"type": "push", "user": "alice", "repo": "myproject", "files": 4},
    ]
    yield from events


# ── Standalone pipeline stages (generators) ───────────────────

def filter_by_type(events, event_type):
    """Yield only events of a specific type."""
    for event in events:
        if event.get("type") == event_type:
            yield event


def filter_by_user(events, user):
    """Yield only events by a specific user."""
    for event in events:
        if event.get("user") == user:
            yield event


def count_files_changed(events):
    """Yield (user, files) tuples for push events."""
    for event in events:
        yield (event["user"], event.get("files", 0))


def aggregate_by_user(events):
    """Sum file changes by user. Yields (user, total_files) pairs."""
    totals = defaultdict(int)
    for user, files in events:
        totals[user] += files
    yield from sorted(totals.items(), key=lambda x: x[1], reverse=True)


def take(n, iterable):
    """Limit output to the first n items."""
    for i, item in enumerate(iterable):
        if i >= n:
            break
        yield item


# ── Pipeline class (chainable, lazy) ──────────────────────────

class Pipeline:
    """Lazy data processing pipeline — chainable stages."""

    def __init__(self, source):
        self._stages = []
        self._source = source

    def filter_by_type(self, event_type):
        """Add a filter-by-type stage."""
        self._stages.append(lambda events: filter_by_type(events, event_type))
        return self  # Chainable!

    def filter_by_user(self, user):
        """Add a filter-by-user stage."""
        self._stages.append(lambda events: filter_by_user(events, user))
        return self

    def count_files(self):
        """Add a file-counting stage."""
        self._stages.append(count_files_changed)
        return self

    def aggregate_by_user(self):
        """Add an aggregation stage."""
        self._stages.append(aggregate_by_user)
        return self

    def limit(self, n):
        """Add a take(n) stage."""
        self._stages.append(lambda events: take(n, events))
        return self

    def __iter__(self):
        """Execute the pipeline lazily."""
        stream = self._source
        for stage in self._stages:
            stream = stage(stream)
        yield from stream

    def collect(self):
        """Materialise the pipeline into a list."""
        return list(self)

    def first(self):
        """Get the first result (or None)."""
        for item in self:
            return item
        return None


# ── Test ───────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== All push events ===")
    pipeline = Pipeline(generate_events())
    pipeline.filter_by_type("push")
    for event in pipeline:
        print(f"  {event['user']} pushed {event['files']} files to {event['repo']}")

    print("\n=== Alice's push events ===")
    pipeline = Pipeline(generate_events())
    pipeline.filter_by_type("push").filter_by_user("alice")
    for event in pipeline:
        print(f"  {event['user']} → {event['repo']}: {event['files']} files")

    print("\n=== Total files pushed per user ===")
    pipeline = Pipeline(generate_events())
    pipeline.filter_by_type("push").count_files().aggregate_by_user()
    for user, total in pipeline:
        print(f"  {user}: {total} files")

    print("\n=== Top 2 pushers ===")
    pipeline = Pipeline(generate_events())
    pipeline.filter_by_type("push").count_files().aggregate_by_user().limit(2)
    print(f"  {pipeline.collect()}")

    print("\n=== First push event ===")
    pipeline = Pipeline(generate_events())
    pipeline.filter_by_type("push")
    first = pipeline.first()
    print(f"  {first}")
```

---

## Quick Recap

- **Iterable** — anything you can `for`-loop over; has `__iter__()`; reusable
- **Iterator** — the thing doing the looping; has `__next__()`; exhaustible
- **`iter()`** creates an iterator; **`next()`** advances it
- **Generator** — function with `yield`; automatically creates an iterator
- **Generator expression** — `(x for x in ...)` — lazy, memory-efficient
- **`yield from`** — delegate to a sub-generator
- **`itertools`** — count, cycle, chain, product, combinations, groupby, etc.
- **Lazy pipelines** — compose generators; nothing runs until you iterate

---

## What's Next?

You've now covered OOP, stacks, queues, deques, and iterables — the foundations of Python data structures. When you're ready, continue to **[Lesson 6: Decorators & Collections](06-decorators-collections.md)**. 🎀

---

**Your turn:** Build the event pipeline! Then add a `map()` stage that transforms events (e.g., extract just the `repo` field) using a lambda, and a `unique()` stage that deduplicates using a set. 🔄💛
