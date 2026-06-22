# Data Structures Lesson 10: Hash Map Superpowers — defaultdict & Counter 🦸

**← Back to [Lesson 9: Heaps](09-heaps.md)**

---

## The Problem: Dicts That Fight Back

You know dicts. They're fast. But they have a rough edge:

```python
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]

# Count occurrences...
counts = {}
for word in words:
    if word not in counts:      # 😩 Check every time
        counts[word] = 0
    counts[word] += 1           # Now we can safely increment

print(counts)  # {'apple': 3, 'banana': 2, 'cherry': 1}
```

That `if word not in counts` check is tedious and error-prone. If you forget it — `KeyError`.

Or grouping items:

```python
pairs = [("fruit", "apple"), ("fruit", "banana"), ("veg", "carrot")]

groups = {}
for category, item in pairs:
    if category not in groups:  # 😩 Again
        groups[category] = []
    groups[category].append(item)
```

Every. Single. Time. The same pattern: check if the key exists, create a default, then use it. Surely there's a better way?

---

## The Idea: Dicts That Auto-Create Missing Values

`defaultdict` is a dict that **automatically creates a default value** when you access a key that doesn't exist. No more `if key not in dict` guards.

`Counter` is a specialised dict purpose-built for counting things — it's `defaultdict(int)` but with extra superpowers like `most_common()`.

Both live in `collections`:

```python
from collections import defaultdict, Counter
```

---

## Step by Step

### Part 1: defaultdict — Never Check for Missing Keys

When you create a `defaultdict`, you tell it **what to use as the default**:

```python
from collections import defaultdict

# defaultdict(int) — missing keys default to 0
counts = defaultdict(int)

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
for word in words:
    counts[word] += 1   # No check! Auto-creates 0 for new keys

print(dict(counts))  # {'apple': 3, 'banana': 2, 'cherry': 1}
```

The magic: `defaultdict(int)` means "if a key is missing, call `int()` — which returns `0` — and use that."

```python
# defaultdict(list) — missing keys default to []
groups = defaultdict(list)

pairs = [("fruit", "apple"), ("fruit", "banana"), ("veg", "carrot")]
for category, item in pairs:
    groups[category].append(item)   # No check! Auto-creates [] for new categories

print(dict(groups))  # {'fruit': ['apple', 'banana'], 'veg': ['carrot']}
```

Any callable works:

```python
from collections import defaultdict

d = defaultdict(lambda: "not found")   # Custom default
print(d["nope"])  # "not found"

scores = defaultdict(float)             # Default 0.0
scores["Alice"] += 9.5
print(scores["Alice"])  # 9.5
print(scores["Bob"])    # 0.0 — auto-created!
```

| Factory | Default value | Use case |
|---------|--------------|----------|
| `int` | `0` | Counting, summing |
| `list` | `[]` | Grouping items |
| `set` | `set()` | Collecting unique values |
| `str` | `""` | Building strings |
| `float` | `0.0` | Numeric scores |
| `dict` | `{}` | Nested dicts |

### Part 2: Counter — Counting on Easy Mode

`Counter` is what you get when `defaultdict(int)` meets a statistics tool:

```python
from collections import Counter

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
c = Counter(words)
print(c)  # Counter({'apple': 3, 'banana': 2, 'cherry': 1})
```

That's it. One line. No loop needed.

**most_common(n)** — the headliner feature:

```python
print(c.most_common(2))  # [('apple', 3), ('banana', 2)]
print(c.most_common(1))  # [('apple', 3)]
```

**Counting from scratch:**

```python
c = Counter()
c["view"] += 1
c["view"] += 1
c["click"] += 1
print(c)              # Counter({'view': 2, 'click': 1})
print(c["share"])     # 0 — missing keys return 0, NOT a KeyError!
```

Unlike a regular dict, `Counter["missing"]` returns `0` instead of raising `KeyError`.

**Counter math** — you can add, subtract, intersect, and union counters:

```python
monday = Counter(apples=3, bananas=1)
tuesday = Counter(apples=1, bananas=2)

print(monday + tuesday)   # Counter({'apples': 4, 'bananas': 3})
print(monday - tuesday)   # Counter({'apples': 2})  — bananas goes to 0, removed
print(monday & tuesday)   # Counter({'apples': 1, 'bananas': 1})  — min of each
print(monday | tuesday)   # Counter({'apples': 3, 'bananas': 2})  — max of each
```

### Part 3: defaultdict vs dict.get() — When to Use Which

```python
# dict.get() — good for ONE default access
d = {"a": 1, "b": 2}
print(d.get("c", 0))  # 0 — provides default for this call only

# defaultdict — good for MANY default accesses (loops)
dd = defaultdict(int)
dd["a"] += 1  # Works without setup
dd["b"] += 1  # Works without setup
```

**Rule of thumb:** If you're doing one lookup → `dict.get()`. If you're building something in a loop → `defaultdict`.

### Part 4: A Real Pattern — Nested defaultdict

Grouping by two categories:

```python
from collections import defaultdict

# Sales: (region, product) → quantity
sales = [
    ("EU", "laptop", 5),
    ("EU", "phone", 3),
    ("US", "laptop", 2),
    ("EU", "laptop", 1),
    ("US", "phone", 4),
]

# defaultdict of defaultdict of int — auto-creates the whole nesting!
by_region = defaultdict(lambda: defaultdict(int))

for region, product, qty in sales:
    by_region[region][product] += qty

# by_region["EU"]["laptop"] → 6 — no setup at any level!
print(dict(by_region))
# {'EU': {'laptop': 6, 'phone': 3}, 'US': {'laptop': 2, 'phone': 4}}
```

The `lambda: defaultdict(int)` means: "if a region key is missing, create a new `defaultdict(int)` for it." Each level auto-creates the next.

---

## Practice

You've got a log file where each line is someone visiting a page. Build an **analytics tool** that answers questions about the data.

```python
visits = [
    "home", "about", "home", "products",
    "home", "about", "contact", "products",
    "home", "home", "about", "products",
]
```

1. Use `Counter` to count visits per page in one line
2. Print the **3 most-visited pages** with `most_common()`
3. Use `defaultdict(set)` to build a `page -> {visitor}` mapping from this data:

```python
page_visits = [
    ("home", "Alice"),
    ("about", "Bob"),
    ("home", "Charlie"),
    ("home", "Alice"),          # Alice visits home again — should only count once!
    ("products", "Bob"),
    ("about", "Alice"),
]
```

The result should show unique visitors per page — Alice visiting home twice counts as one.

```python
# Your code here:


# Expected output:
# Page counts: {'home': 5, 'about': 3, 'products': 3, 'contact': 1}
# Top 3: [('home', 5), ('about', 3), ('products', 3)]
# Unique visitors: {'home': {'Alice', 'Charlie'}, 'about': {'Bob', 'Alice'}, 'products': {'Bob'}}
```

---

## Solution

<details>
<summary>Click to reveal</summary>

```python
from collections import defaultdict, Counter

# --- Part 1: Count visits ---
visits = [
    "home", "about", "home", "products",
    "home", "about", "contact", "products",
    "home", "home", "about", "products",
]

page_counts = Counter(visits)
print(f"Page counts: {dict(page_counts)}")
print(f"Top 3: {page_counts.most_common(3)}")

# --- Part 2: Unique visitors per page ---
page_visits = [
    ("home", "Alice"),
    ("about", "Bob"),
    ("home", "Charlie"),
    ("home", "Alice"),          # Duplicate — set handles this!
    ("products", "Bob"),
    ("about", "Alice"),
]

unique_visitors = defaultdict(set)   # set auto-deduplicates
for page, visitor in page_visits:
    unique_visitors[page].add(visitor)

print(f"Unique visitors: {dict(unique_visitors)}")
```

`defaultdict(set)` is the key insight — `set` auto-deduplicates, so Alice visiting home twice only counts once.

</details>

---

## Recap

- **`defaultdict`** — dict that auto-creates missing keys. No more `if key not in dict`.
- **`defaultdict(int)`** → counting. **`defaultdict(list)`** → grouping. **`defaultdict(set)`** → deduplicating.
- **`Counter`** — `defaultdict(int)` with superpowers: `most_common()`, counter math (+, -, &, |)
- **`Counter["missing"]` returns `0`** — never a `KeyError`
- **`dict.get()`** for one-offs, **`defaultdict`** for loops
- **Nested defaultdict** with `lambda` — auto-creates multiple levels

---


