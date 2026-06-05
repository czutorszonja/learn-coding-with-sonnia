# Advanced Python Lesson 11: Hash Maps Deep Dive 🔑

**← Back to [Lesson 10: Heaps & Priority Queues](10-heaps-priority-queues.md)**

---

## What is a Hash Map?

**Plain English:** A hash map (Python's `dict`) lets you store and retrieve values by a _key_ in O(1) time — near-instant, no matter how many items you have. Under the hood, it uses a _hash function_ to turn your key into an array index.

**Real-world analogy:** A library with a brilliant cataloguing system:
- Every book has a unique call number (computed from its title)
- The call number tells you _exactly_ which shelf and position the book is on
- You don't need to search every shelf — you go straight to it
- Sometimes two books get the same call number (collision!) — the librarian has a system for that

---

## How Hashing Works

```python
# Your key goes in...
key = "Szonja"

# Python hashes it to a number...
hash_value = hash(key)  # e.g., 5738291047263518294

# That number maps to an array index...
index = hash_value % array_size

# The value is stored at that index!
```

**The magic:** Same key → same hash → same index → instant retrieval!

---

## Hash Function Requirements

A good hash function must be:

1. **Deterministic** — same input always produces the same hash
2. **Uniform** — spreads values evenly across the array
3. **Fast** — computing the hash must be cheap
4. **Avalanche effect** — small input change → completely different hash

```python
# Python's hash is fast and well-distributed
print(hash("hello"))        # 1058227008376475732
print(hash("hello!"))       # -7918736898185845934 (totally different!)
print(hash(42))             # 42 (integers hash to themselves)
print(hash((1, 2, 3)))      # 529344067295497451
# print(hash([1, 2, 3]))    # ❌ TypeError! Lists are unhashable (mutable)
```

---

## Collisions — When Two Keys Map to the Same Index

It happens. Here's how we handle it:

### 1. Separate Chaining (Linked Lists)

```
Array: [0]  →  None
       [1]  →  ("apple", "red")  →  ("cherry", "red")  →  None
       [2]  →  ("banana", "yellow")  →  None
       [3]  →  None
```

Each array slot holds a linked list of (key, value) pairs. If two keys collide, they share the slot in a chain.

### 2. Open Addressing (Linear Probing)

```
Array: [0]  ("banana", "yellow")
       [1]  ("apple", "red")
       [2]  ("cherry", "red")   ← wanted slot 1 but it was taken, so used next open
       [3]  None
```

If a slot is taken, look at the next one, then the next, until you find an empty spot.

**Python uses open addressing** with a clever variant called "pseudo-random probing" — it's fast and cache-friendly.

---

## Building a Hash Map from Scratch

```python
class SimpleHashMap:
    """A simplified hash map using separate chaining."""

    def __init__(self, initial_size=8):
        self.size = initial_size
        self.buckets = [[] for _ in range(self.size)]  # Array of lists
        self._count = 0

    def _hash(self, key):
        """Map a key to a bucket index."""
        return hash(key) % self.size

    def put(self, key, value):
        """Insert or update a key-value pair."""
        index = self._hash(key)
        bucket = self.buckets[index]

        # Check if key already exists in this bucket
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Update
                return

        # New key — append to bucket
        bucket.append((key, value))
        self._count += 1

        # Resize if getting too full (load factor > 0.75)
        if self._count / self.size > 0.75:
            self._resize(self.size * 2)

    def get(self, key, default=None):
        """Retrieve a value by key."""
        index = self._hash(key)
        bucket = self.buckets[index]

        for k, v in bucket:
            if k == key:
                return v
        return default

    def remove(self, key):
        """Remove a key-value pair."""
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._count -= 1
                return True
        return False

    def _resize(self, new_size):
        """Grow the array and rehash everything."""
        old_buckets = self.buckets
        self.size = new_size
        self.buckets = [[] for _ in range(new_size)]
        self._count = 0

        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)

    def __contains__(self, key):
        return self.get(key) is not None

    def __getitem__(self, key):
        result = self.get(key)
        if result is None:
            raise KeyError(key)
        return result

    def __setitem__(self, key, value):
        self.put(key, value)

    def __len__(self):
        return self._count

    def keys(self):
        """Return all keys."""
        result = []
        for bucket in self.buckets:
            for key, _ in bucket:
                result.append(key)
        return result

    def __repr__(self):
        items = [f"{k!r}: {v!r}" for k, v in self.items()]
        return "{" + ", ".join(items) + "}"

    def items(self):
        """Return all (key, value) pairs."""
        result = []
        for bucket in self.buckets:
            for pair in bucket:
                result.append(pair)
        return result
```

---

## Why Some Types Are Hashable and Others Aren't

```python
# ✅ Hashable (immutable)
hash("hello")       # str
hash(42)            # int
hash(3.14)          # float
hash((1, 2))        # tuple (of hashable items)
hash(frozenset({1}))# frozenset

# ❌ Not hashable (mutable)
# hash([1, 2, 3])   # list — can change!
# hash({1, 2})      # set — can change!
# hash({"a": 1})    # dict — can change!
```

**Why?** If a key's hash changes after insertion, you can never find it again! Mutable objects can change → their hash would change → lost data.

---

## Python Dict Internals (CPython 3.6+)

Python's dict is remarkably efficient:

1. **Compact** — keys and values stored in separate dense arrays
2. **Insertion-ordered** — since Python 3.7, dicts remember insertion order (officially guaranteed)
3. **Memory-efficient** — uses an _indices_ array to map hashes to entries
4. **Optimised for small dicts** — special case for ≤ 8 items

```python
# Dicts preserve insertion order!
d = {}
d["first"] = 1
d["second"] = 2
d["third"] = 3
print(list(d.keys()))  # ['first', 'second', 'third']
```

---

## `defaultdict` and `Counter` — Dict Superpowers

```python
from collections import defaultdict, Counter

# defaultdict — automatic default values
word_counts = defaultdict(int)  # Default 0 for missing keys
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
for word in words:
    word_counts[word] += 1      # No "if word not in dict" needed!
print(dict(word_counts))        # {'apple': 3, 'banana': 2, 'cherry': 1}

# Group items with defaultdict(list)
groups = defaultdict(list)
pairs = [("fruit", "apple"), ("fruit", "banana"), ("veg", "carrot")]
for category, item in pairs:
    groups[category].append(item)
print(dict(groups))  # {'fruit': ['apple', 'banana'], 'veg': ['carrot']}

# Counter — count hashable items directly
counter = Counter(["a", "b", "a", "c", "b", "a"])
print(counter)               # Counter({'a': 3, 'b': 2, 'c': 1})
print(counter.most_common(2))# [('a', 3), ('b', 2)]

# Counter operations
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(c1 + c2)   # Counter({'a': 4, 'b': 3}) — add counts
print(c1 - c2)   # Counter({'a': 2})           — subtract counts
print(c1 & c2)   # Counter({'a': 1, 'b': 1})   — intersection (min)
print(c1 | c2)   # Counter({'a': 3, 'b': 2})   — union (max)
```

---

## Time Complexity Comparison

| Operation | List | Sorted List | BST (balanced) | Hash Map |
|-----------|------|-------------|----------------|----------|
| Search | O(n) | O(log n) | O(log n) | O(1) avg |
| Insert | O(n)* | O(n) | O(log n) | O(1) avg |
| Delete | O(n) | O(n) | O(log n) | O(1) avg |
| Sorted order | — | O(1) | O(n) | ❌ |

\* O(1) amortised at the end, O(n) in the middle

**Takeaway:** Hash maps are the speed king for lookups — but you give up ordering.

---

## Practice Exercise

**Scenario:** You're building a URL shortener (like bit.ly). Short codes map to long URLs, and you need instant lookups.

**Your task:**

1. Create `url_shortener.py` with a `URLShortener` class that:
   - `shorten(long_url)` — generates a short code (6 random characters), stores the mapping, returns the short URL like `https://short.ly/abc123`
   - `expand(short_code)` — returns the original long URL or None
   - `get_clicks(short_code)` — returns how many times the short URL was accessed (expand counts as a click!)
   - `get_all_urls()` — returns a dict of `{short_code: {"url": long_url, "clicks": count}}`

2. Use a hash map (dict) as your backing store — O(1) lookups!

3. Bonus features:
   - If the same long URL is shortened twice, return the _existing_ short code (don't create duplicates)
   - Make `generate_code()` a separate method that creates random 6-char codes using letters and digits
   - Handle collisions: if a generated code already exists, generate a new one

4. Write a `generate_code` function:
   ```python
   import random
   import string

   def generate_code(length=6):
       chars = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
       return ''.join(random.choices(chars, k=length))
   ```

5. Test your shortener:
   ```python
   shortener = URLShortener()
   code1 = shortener.shorten("https://www.example.com/very/long/url")
   code2 = shortener.shorten("https://www.example.com/another/long/url")
   code3 = shortener.shorten("https://www.example.com/very/long/url")  # Duplicate!

   print(code1)  # "abc123"
   print(code3)  # "abc123" (same as code1 — duplicate detected!)

   print(shortener.expand("abc123"))  # Original URL
   print(shortener.expand("abc123"))  # Original URL (2 clicks now!)
   print(shortener.get_clicks("abc123"))  # 2

   print(shortener.get_all_urls())
   ```

**Try it yourself first!** Solution below.

---

## Solution

```python
import random
import string


def generate_code(length=6):
    """Generate a random alphanumeric code."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


class URLShortener:
    """A URL shortener backed by hash maps for O(1) lookups."""

    def __init__(self):
        self._code_to_url = {}   # short_code → long_url
        self._url_to_code = {}   # long_url → short_code (reverse lookup)
        self._clicks = {}        # short_code → click count

    def shorten(self, long_url):
        """Shorten a URL. Returns existing code if already shortened."""
        # Check if URL was already shortened
        if long_url in self._url_to_code:
            existing_code = self._url_to_code[long_url]
            return existing_code

        # Generate a unique code
        code = generate_code()
        while code in self._code_to_url:
            code = generate_code()  # Collision — try again

        # Store mappings
        self._code_to_url[code] = long_url
        self._url_to_code[long_url] = code
        self._clicks[code] = 0

        return code

    def expand(self, short_code):
        """Expand a short code to the original URL. Counts as a click."""
        long_url = self._code_to_url.get(short_code)
        if long_url:
            self._clicks[short_code] += 1
        return long_url

    def get_clicks(self, short_code):
        """Return the click count for a short code."""
        return self._clicks.get(short_code, 0)

    def get_all_urls(self):
        """Return all shortened URLs with click counts."""
        return {
            code: {
                "url": self._code_to_url[code],
                "clicks": self._clicks[code]
            }
            for code in self._code_to_url
        }


# --- Test ---
if __name__ == "__main__":
    shortener = URLShortener()

    code1 = shortener.shorten("https://www.example.com/very/long/url")
    code2 = shortener.shorten("https://www.example.com/another/long/url")
    code3 = shortener.shorten("https://www.example.com/very/long/url")

    print(f"Code 1: {code1}")
    print(f"Code 2: {code2}")
    print(f"Code 3: {code3} (should match Code 1)")

    # Expand — counts clicks
    print(f"\nExpand '{code1}': {shortener.expand(code1)}")
    print(f"Expand '{code1}' again: {shortener.expand(code1)}")

    print(f"\nClicks for '{code1}': {shortener.get_clicks(code1)}")
    print(f"Clicks for '{code2}': {shortener.get_clicks(code2)}")

    print(f"\nAll URLs:")
    for code, info in shortener.get_all_urls().items():
        print(f"  {code}: {info['url']} ({info['clicks']} clicks)")
```

---

## Quick Recap

- **Hash map** — key → hash → array index → O(1) lookup
- **Hash function** must be deterministic, uniform, fast
- **Collision resolution** — chaining (linked lists) or open addressing (probing)
- **Python dicts** use open addressing, are insertion-ordered (3.7+), and highly optimised
- **Hashable types** are immutable (str, int, tuple); mutable types (list, set, dict) are not
- **`defaultdict`** and **`Counter`** are dict superpowers
- **Short URL** pattern — two dicts for bidirectional O(1) lookup

---

## What's Next?

You can find things instantly with hash maps. Now let's learn how to _organise_ them efficiently. Continue to **[Lesson 12: Sorting Algorithms](12-sorting-algorithms.md)** 📊

---

**Your turn:** Build the URL shortener! Then try adding `get_top_urls(n)` that returns the n most-clicked URLs using `Counter.most_common()`. 🔑💛
