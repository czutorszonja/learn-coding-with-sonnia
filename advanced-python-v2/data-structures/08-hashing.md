# Data Structures Lesson 8: Hashing — Instant Lookups ✨

**← Back to [Lesson 7: Trees](07-trees.md)**

---

## The Problem: "Where Did I Put That?"

You know how finding something in a sorted list is fast if you binary search? But what if you don't want to sort at all? What if you want **instant access** by any key?

```python
phonebook = {
    "Szonja": "0744...",
    "Arthur": "0759...",
    "Sonnia": "sonnia@sonnia.ai",
}
print(phonebook["Szonja"])  # Instant — even with 10,000 entries
```

How does Python find `"Szonja"` instantly without scanning every entry? It's not searching, it's not binary comparing — it's **hashing**. Python computes a number from the key and jumps directly to that memory location.

---

## The Idea: A Magic Index

Imagine you have a filing cabinet with 26 drawers, labelled A to Z. You file "Szonja" — you put it in drawer S. Later, someone asks for Szonja — you go straight to drawer S.

You didn't scan every letter. You **computed the drawer from the name**. That's hashing.

A **hash function** takes any piece of data and returns a fixed-size number (called a **hash**):

```
"Szonja"    → hash function → 872364
"Arthur"    → hash function → 129873
"Sonnia"    → hash function → 987412
```

Python then uses that number to decide where in memory to store the value. When you look it up, Python re-computes the hash and goes directly to that spot.

---

## The Two Guarantees

1. **Deterministic** — the same input ALWAYS produces the same hash
2. **Fast** — computing a hash takes almost no time

If either of these were false, dictionaries wouldn't work. The first hash of `"Szonja"` maps to bucket 7, and every subsequent lookup for `"Szonja"` goes to the same bucket.

---

## Python's `hash()` Function

```python
print(hash("Szonja"))   # Some number (changes between Python runs)
print(hash("Arthur"))   # Different number
print(hash("Szonja"))   # Same as first call ✅
print(hash(42))         # Works with integers too
print(hash(3.14))       # Even floats
```

Not everything is hashable:

```python
# hash([1, 2, 3])  # TypeError: unhashable type: 'list'
```

Lists are **mutable** — their contents can change, so their hash would change too. If a list's hash changed while it was being used as a dictionary key, the dictionary would break. Python prevents this: only immutable types (strings, numbers, tuples) can be hashed.

---

## Collisions: When Two Keys Share a Bucket

What happens if `"Szonja"` and `"Strawberry"` both hash to the same bucket? That's a **collision**.

Python handles this with **chaining**: each bucket holds a list of (key, value) pairs. When you look up a key, Python checks all entries in the bucket.

```
Bucket 7: [("Szonja", "0744..."), ("Strawberry", "red")]
            ↑ Look up "Szonja" → scan these two → found!
```

With a good hash function, collisions are rare, and each bucket has at most 1-2 entries. Even with collisions, lookups are still essentially O(1) — you're just checking 1 or 2 items instead of 1.

If a bucket gets too full, Python **resizes** the table (doubles the size and rehashes everything). This is why dictionaries can grow without slowing down.

---

## Building Your Own Hash Table

Let's build one to see how it works from scratch:

```python
class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def _hash(self, key):
        """Simple hash function — sum of character codes."""
        return sum(ord(c) for c in str(key)) % self.size

    def set(self, key, value):
        index = self._hash(key)
        bucket = self.buckets[index]
        # Check if key already exists — update it
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        # New key — append to bucket
        bucket.append((key, value))

    def get(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(key)

    def __str__(self):
        parts = []
        for i, bucket in enumerate(self.buckets):
            if bucket:
                parts.append(f"  [{i}]: {bucket}")
        return "HashTable:\n" + "\n".join(parts)
```

```python
phonebook = HashTable()
phonebook.set("Szonja", "0744...")
phonebook.set("Arthur", "0759...")
phonebook.set("Sonnia", "sonnia@sonnia.ai")

print(phonebook.get("Szonja"))      # 0744...
print(phonebook.get("Sonnia"))      # sonnia@sonnia.ai
# print(phonebook.get("Nobody"))    # KeyError

print(phonebook)
```

Output:
```
0744...
sonnia@sonnia.ai
HashTable:
  [0]: [('Sonnia', 'sonnia@sonnia.ai')]
  [3]: [('Arthur', '0759...')]
  [7]: [('Szonja', '0744...')]
```

These are all in different buckets. If they collided, they'd share a bucket as a list of tuples.

---

## Real Hash Functions Are Better

My `_hash` function is basic — it sums character codes. That causes problems:

```python
print(hash("abc"))  # 97 + 98 + 99 = 294
print(hash("cba"))  # 99 + 98 + 97 = 294 — SAME!
```

Anagrams collide! Python's actual hash function is much more sophisticated, mixing up bits to spread things evenly. Real hash functions use **bit shifting and prime numbers** to avoid patterns. For our purposes, the simple version teaches the concept — just don't use it in production.

---

## Practice: Build a Frequency Counter

**Your task:** Write a function `char_frequency(text)` that returns a hash table (your `HashTable` class) mapping each character to how many times it appears in the text.

```python
def char_frequency(text):
    # Your code here — iterate over characters,
    # get the current count, increment it, set it back
    pass


result = char_frequency("hello world")
print(result.get("h"))  # 1
print(result.get("l"))  # 3
print(result.get("z"))  # Should raise KeyError
```

Create `frequency.py` and try it!

---

## Solution

```python
class HashTable:
    def __init__(self, size=26):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def _hash(self, key):
        return sum(ord(c) for c in str(key)) % self.size

    def set(self, key, value):
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(key)


def char_frequency(text):
    freq = HashTable(size=36)  # 26 letters + 10 digits + symbols
    for char in text:
        try:
            current = freq.get(char)
            freq.set(char, current + 1)
        except KeyError:
            freq.set(char, 1)
    return freq


result = char_frequency("hello world")
print(f"h: {result.get('h')}")  # 1
print(f"l: {result.get('l')}")  # 3
print(f"o: {result.get('o')}")  # 2
print(f" : {result.get(' ')}")  # 1
# print(result.get('z'))  # KeyError
```

Bonus: Python's built-in `collections.Counter` does this exact thing, and it's built on a dictionary (which is built on hashing):

```python
from collections import Counter
freq = Counter("hello world")
print(freq)
# Counter({'l': 3, 'o': 2, 'h': 1, 'e': 1, ' ': 1, 'w': 1, 'r': 1, 'd': 1})
```

---

## Hashing in the Real World

Hashing goes way beyond dictionaries:

- **Password storage** — passwords are hashed (never stored in plaintext). When you log in, your input is hashed and compared to the stored hash.
- **Git** — every commit has a SHA-1 hash that uniquely identifies its contents and history
- **Caching** — hash URLs to quickly check if a page is cached
- **Data integrity** — file checksums verify that downloads weren't corrupted

---

## Data Structures — You Built All Of These

| Data Structure | Strength |
|---|---|
| **Stack** | LIFO — undo, back button |
| **Queue** | FIFO — print jobs, ticketing |
| **Deque** | Both ends — clipboard, recent items |
| **Iterables / Generators** | How `for` works, lazy evaluation |
| **Linked List** | Fast insert/delete in middle |
| **Tree** | Hierarchical data |
| **Hash Table** | Instant lookups |

You've gone from "what's a class?" to "what's a hash table?" — that's a massive journey, and you've built something real at every step.

---

**Each of these topics could fill a semester. You're learning them in afternoons. That's not just okay — that's how learning should feel when it fits right.** 💛

---

**Next: [Lesson 9: Heaps & Priority Queues](09-heaps.md) →**
