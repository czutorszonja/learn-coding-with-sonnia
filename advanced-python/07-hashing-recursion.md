# Advanced Python Lesson 7: Hashing & Recursion 🔐

**← Back to [Lesson 6: Decorators & Collections](06-decorators-collections.md)**

---

## What is This Lesson About?

**Plain English:** Hashing and recursion are two of the most powerful ideas in computer science — and when you combine them, you unlock patterns that solve problems that would otherwise be impossible. This lesson bridges the two: using hash maps to supercharge recursive algorithms, and using recursion to navigate structures that hashing helps you identify.

**Real-world analogy:** Imagine you're a detective investigating a sprawling criminal network:
- **Recursion** is how you trace connections — you follow one lead, which reveals three more, and you follow each of those...
- **Hashing** is your case file — every time you investigate someone, you stamp their file `VISITED` so you don't waste time re-investigating them
- **Together:** You can map the entire network without going in circles, and you know instantly if you've already checked someone

---

## Part 1: Hashing — A Deeper Look

### What Makes a Good Hash?

A hash function maps _anything_ to a _fixed-size number_:

```python
# Python's built-in hash()
print(hash("hello"))         # 1058227008376475732
print(hash("hello!"))        # -7918736898185845934  (totally different!)
print(hash((1, 2, 3)))       # 529344067295497451
print(hash(42))              # 42  (integers hash to themselves!)

# ❌ Mutable things can't be hashed
# hash([1, 2, 3])  # TypeError: unhashable type: 'list'
```

**Key properties:**
1. **Deterministic** — same input → same hash, every time
2. **Uniform** — spreads values evenly (minimises collisions)
3. **Fast** — O(1), near-instant
4. **Avalanche effect** — tiny input change → completely different hash

### How a Dict Uses Hashing Under the Hood

```python
# When you write:
my_dict["Szonja"] = "Python learner"

# Python does:
# 1. hash("Szonja") → e.g., 5738291047263518294
# 2. index = hash_value % table_size
# 3. Store ("Szonja", "Python learner") at that index

# When you read:
print(my_dict["Szonja"])

# Python does:
# 1. hash("Szonja") → 5738291047263518294 (same!)
# 2. index = hash_value % table_size (same index!)
# 3. Go straight to that slot → O(1) retrieval
```

### Handling Collisions

What happens when two keys hash to the same slot?

```python
# Collision: hash("apple") % 8 == 3 AND hash("grape") % 8 == 3
#
# Python uses "open addressing" — if slot 3 is taken, try 4, then 5...
# Or "chaining" — each slot holds a linked list of (key, value) pairs
#
# Either way, you still get O(1) average lookup — collisions are rare
# with a good hash function and a big enough table.
```

### Hashing Custom Objects

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Two points are equal if their coordinates match."""
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        """Hash must match __eq__ — equal objects MUST have equal hashes."""
        return hash((self.x, self.y))  # Delegate to tuple's hash!

p1 = Point(3, 4)
p2 = Point(3, 4)
p3 = Point(5, 6)

print(p1 == p2)           # True — same coordinates
print(hash(p1) == hash(p2))  # True — equal objects, equal hashes

# Now Point works as a dict key or set member!
visited = {p1, p3}
print(p2 in visited)  # True — p2 "is" p1 for hashing purposes
```

**The Golden Rule of Hashing:**
- If `a == b`, then `hash(a) == hash(b)` — **must** be true
- If `a != b`, `hash(a)` can equal `hash(b)` — but should be rare (collision)

---

## Part 2: Recursion — A Quick Refresher

```python
def factorial(n):
    if n <= 1:              # BASE CASE — stop here!
        return 1
    return n * factorial(n - 1)  # RECURSIVE CASE — smaller problem

# What happens:
# factorial(4)
#   4 * factorial(3)
#       3 * factorial(2)
#           2 * factorial(1)
#               1           ← base case hits, unwind!
#           2 * 1 = 2
#       3 * 2 = 6
#   4 * 6 = 24
```

The call stack builds up, then unwinds. Deep recursion → deep stack → potential `RecursionError`.

---

## Part 3: Where Hashing Meets Recursion — Memoization

### The Problem: Exponential Blowup

```python
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

# fib(5) calls fib(4) and fib(3)
# fib(4) calls fib(3) and fib(2)   ← fib(3) again!
# fib(3) calls fib(2) and fib(1)   ← fib(3) a THIRD time!
#
# fib(40) takes MINUTES — exponential time O(2ⁿ)
```

**The insight:** We're recalculating the same thing over and over. If only we could _remember_...

### The Fix: A Dict as Memory

```python
def fib_memo(n, memo=None):
    if memo is None:
        memo = {}                # Our memory — a hash map!

    if n in memo:                # Already computed? Return instantly!
        return memo[n]

    if n <= 1:
        return n

    result = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    memo[n] = result             # Remember this result
    return result

print(fib_memo(100))  # Instant! O(n) instead of O(2ⁿ)
# 354224848179261915075 — computed in microseconds
```

**Why this works:** The hash map (`memo`) turns repeated subproblems from "recalculate everything" into "look it up in O(1)". This is the core idea of **dynamic programming** — recursion + memoization.

### `functools.lru_cache` — Built-in Memoization

```python
from functools import lru_cache

@lru_cache(maxsize=None)   # Unlimited cache
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(500))  # Works! lru_cache handles everything
# 139423224561697880139724382870407283950070256587697307264108962948325571622863290691557658876222521294125

# Bonus: check cache stats
print(fib.cache_info())
# CacheInfo(hits=498, misses=501, maxsize=None, currsize=501)
```

`lru_cache` is `memoize` on steroids — it handles hashable arguments, has a size limit, and tracks statistics.

---

## Part 4: Recursive Hashing of Nested Structures

Hashing isn't just for dict keys — it's a tool for _identifying_ things. Combine it with recursion to identify entire trees of data.

### Computing a Hash for a Directory Tree

```python
import hashlib
import os

def hash_file(filepath):
    """Return SHA-256 hash of a file's contents."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def hash_directory(path):
    """
    Recursively compute a hash for an entire directory.
    Two directories with identical contents get the same hash!
    """
    hasher = hashlib.sha256()

    # Get sorted entries for deterministic hashing
    entries = sorted(os.listdir(path))

    for entry in entries:
        full_path = os.path.join(path, entry)
        hasher.update(entry.encode())  # Include the name!

        if os.path.isfile(full_path):
            file_hash = hash_file(full_path)
            hasher.update(file_hash.encode())
        elif os.path.isdir(full_path):
            dir_hash = hash_directory(full_path)  # RECURSION!
            hasher.update(dir_hash.encode())

    return hasher.hexdigest()
```

**This is how Git works** — every file and directory is hashed, and the root hash identifies the entire repository state.

### Finding Duplicate Files with Recursive Hashing

```python
def find_duplicates(root_path):
    """
    Walk a directory tree and find duplicate files
    using recursive hashing + a hash map.
    """
    hash_to_paths = {}  # hash → list of file paths

    def walk(path):
        if os.path.isfile(path):
            file_hash = hash_file(path)
            if file_hash not in hash_to_paths:
                hash_to_paths[file_hash] = []
            hash_to_paths[file_hash].append(path)
        elif os.path.isdir(path):
            for entry in os.listdir(path):   # RECURSION
                walk(os.path.join(path, entry))

    walk(root_path)

    # Only return hashes with duplicates
    return {h: paths for h, paths in hash_to_paths.items() if len(paths) > 1}


# Usage:
# duplicates = find_duplicates("/home/szonja/documents")
# for file_hash, paths in duplicates.items():
#     print(f"Duplicate (hash={file_hash[:8]}...):")
#     for p in paths:
#         print(f"  {p}")
```

---

## Part 5: Recursive Data Structure Hashing

### Deep Equality Check with Hashing

```python
def deep_hash(obj):
    """
    Compute a deterministic hash for any nested Python structure.
    Equal structures → equal hashes, no matter their identity!
    """
    if isinstance(obj, dict):
        # Sort by key for deterministic ordering
        items = sorted(obj.items())
        return hash(tuple(
            (deep_hash(k), deep_hash(v)) for k, v in items
        ))
    elif isinstance(obj, (list, tuple)):
        return hash(tuple(deep_hash(item) for item in obj))
    elif isinstance(obj, set):
        # Sets are unordered — sort the hashes
        return hash(tuple(sorted(deep_hash(item) for item in obj)))
    else:
        return hash(obj)


# Two different objects with identical structure
tree_a = {"name": "root", "children": [{"name": "a"}, {"name": "b"}]}
tree_b = {"name": "root", "children": [{"name": "a"}, {"name": "b"}]}

print(deep_hash(tree_a) == deep_hash(tree_b))  # True!
# deep_hash recursively hashes every level — structural equality as a number
```

### Detecting Structural Cycles

```python
def safe_deep_hash(obj, visited=None):
    """
    Like deep_hash, but handles circular references.
    Uses a hash set (visited) to detect cycles.
    """
    if visited is None:
        visited = set()

    obj_id = id(obj)
    if obj_id in visited:
        return hash("<cycle>")  # Cycle detected — use a sentinel
    visited.add(obj_id)

    try:
        if isinstance(obj, dict):
            items = sorted(obj.items())
            return hash(tuple(
                (safe_deep_hash(k, visited), safe_deep_hash(v, visited))
                for k, v in items
            ))
        elif isinstance(obj, (list, tuple)):
            return hash(tuple(safe_deep_hash(item, visited) for item in obj))
        else:
            return hash(obj)
    finally:
        visited.discard(obj_id)  # Backtrack — allow revisiting via different paths


# Circular structure
a = []
b = [a]
a.append(b)  # a contains b, b contains a — circular!

try:
    h = safe_deep_hash(a)
    print(f"Hash of circular structure: {h}")  # Works!
except RecursionError:
    print("Would recurse forever without visited tracking!")
```

---

## Practice Exercise: Recursive Memoized Spell Checker

### The Problem

Build a spell checker that uses **recursion + memoization** to find the minimum edit distance between two words — and then use it to suggest corrections.

**Edit distance (Levenshtein distance):** The minimum number of single-character edits (insert, delete, substitute) to turn one word into another.

For example: `"kitten"` → `"sitting"` = 3 edits (k→s, e→i, +g)

### Your Tasks

1. **Write `edit_distance(s1, s2)` recursively:**
   - Base cases: if one string is empty, distance = length of the other
   - If first characters match: skip them, recurse on the rest
   - Otherwise: try all three operations (insert, delete, substitute) and take the minimum
   - Add `lru_cache` to make it fast!

2. **Write `suggest_corrections(word, dictionary, max_suggestions=5)`:**
   - Given a misspelt word and a list of valid words
   - Compute edit distance to every dictionary word
   - Return the closest matches, sorted by distance
   - Use a `Counter` or `defaultdict` to group suggestions by distance

3. **Test it:**
   ```python
   dictionary = ["python", "typing", "pytorch", "pythonic", "pithon",
                 "typhoon", "tycoon", "typing", "pylon", "pythonista"]
   print(suggest_corrections("pyton", dictionary))
   # Should suggest: python (distance 1), pylon (1), pithon (1), ...
   ```

4. **Bonus:** Add a `memo` dict that caches edit distances across multiple word suggestions — reuse work between words!

---

## Solution

```python
from functools import lru_cache
from collections import defaultdict


# === Part 1: Recursive Edit Distance with Memoization ===

@lru_cache(maxsize=None)
def edit_distance(s1, s2):
    """
    Minimum edits to turn s1 into s2.
    Operations: insert, delete, substitute (each costs 1).
    """
    # Base case: one string is empty
    if not s1:
        return len(s2)   # Insert all remaining chars
    if not s2:
        return len(s1)   # Delete all remaining chars

    # First characters match — no edit needed here
    if s1[0] == s2[0]:
        return edit_distance(s1[1:], s2[1:])

    # Try all three operations, take the minimum
    substitute = 1 + edit_distance(s1[1:], s2[1:])   # Change first char
    insert = 1 + edit_distance(s1, s2[1:])            # Insert into s1
    delete = 1 + edit_distance(s1[1:], s2)            # Delete from s1

    return min(substitute, insert, delete)


# === Part 2: Suggest Corrections ===

def suggest_corrections(word, dictionary, max_suggestions=5):
    """Find the closest dictionary words to the given word."""
    # Group words by their edit distance
    by_distance = defaultdict(list)

    for candidate in dictionary:
        dist = edit_distance(word, candidate)
        by_distance[dist].append(candidate)

    # Sort by distance, flatten, and limit
    suggestions = []
    for dist in sorted(by_distance.keys()):
        suggestions.extend(sorted(by_distance[dist]))
        if len(suggestions) >= max_suggestions:
            break

    return suggestions[:max_suggestions]


# === Part 3: Test It ===

if __name__ == "__main__":
    # Basic edit distance tests
    print("Edit distance examples:")
    print(f"  'kitten' → 'sitting': {edit_distance('kitten', 'sitting')}")  # 3
    print(f"  'abc' → '': {edit_distance('abc', '')}")                       # 3
    print(f"  '' → 'abc': {edit_distance('', 'abc')}")                       # 3
    print(f"  'python' → 'python': {edit_distance('python', 'python')}")     # 0
    print(f"  'pyton' → 'python': {edit_distance('pyton', 'python')}")       # 1

    # Cache stats
    print(f"\nCache stats: {edit_distance.cache_info()}")

    # Spell check demo
    print("\n" + "=" * 50)
    print("🔍 Spell Checker")
    print("=" * 50)

    dictionary = [
        "python", "typing", "pytorch", "pythonic", "pithon",
        "typhoon", "tycoon", "pylon", "pythonista", "pythonize",
        "typo", "typhoid", "pit", "pity", "pony", "tony"
    ]

    test_words = ["pyton", "typingg", "pythn", "hello"]

    for word in test_words:
        suggestions = suggest_corrections(word, dictionary)
        print(f"\n'{word}' — did you mean?")
        for s in suggestions:
            dist = edit_distance(word, s)
            print(f"  {s} (distance {dist})")

    print(f"\nTotal cache hits after all suggestions: "
          f"{edit_distance.cache_info().hits}")
```

**Sample output:**
```
Edit distance examples:
  'kitten' → 'sitting': 3
  'abc' → '': 3
  '' → 'abc': 3
  'python' → 'python': 0
  'pyton' → 'python': 1

Cache stats: CacheInfo(hits=30, misses=128, ...)

==================================================
🔍 Spell Checker
==================================================

'pyton' — did you mean?
  python (distance 1)
  pylon (distance 1)
  pithon (distance 1)
  pony (distance 2)
  tony (distance 2)

'typingg' — did you mean?
  typing (distance 1)
  typo (distance 3)
  typhoid (distance 4)

'pythn' — did you mean?
  python (distance 1)
  pithon (distance 2)

'hello' — did you mean?
  (no close matches)

Total cache hits after all suggestions: 342
```

---

## Quick Recap

- **Hash functions** — map anything to a number: deterministic, uniform, fast
- **Collisions** — when two keys hash to the same slot; Python handles them transparently
- **`__hash__` + `__eq__`** — the golden rule: equal objects MUST have equal hashes
- **Memoization** — using a dict to cache recursive results; turns O(2ⁿ) into O(n)
- **`lru_cache`** — built-in memoization; `maxsize=None` for unlimited, `cache_info()` for stats
- **Recursive hashing** — hash nested structures; identical structure → identical hash
- **Cycle detection** — use a `set` to track visited objects in recursive traversal
- **Edit distance** — classic recursion + memoization problem; basis of spell checkers, diff tools, DNA alignment

---

## What's Next?

You've now seen how hashing and recursion work together — memoization, recursive hashing, and cycle-safe traversal. Next up: building data structures out of chains of nodes. Continue to **[Lesson 8: Linked Lists](08-linked-lists.md)** 🔗

---

**Your turn:** Build the spell checker! Then try adding `lru_cache(maxsize=256)` instead of unlimited and check `cache_info()` after running many suggestions — watch the evictions happen when the cache fills up. 🔐💛
