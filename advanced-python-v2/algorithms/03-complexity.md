# Algorithms: Time & Space Complexity ⏱️

**← Back to [Hashing](../data-structures/08-hashing.md)**

---

## The Question Nobody Asks Until They Have To

Your code works. That's great. But then you feed it more data, and suddenly it's... crawling.

```python
# This works fine with 10 students
students = ["Szonja", "Arthur", "Cece", ...]
for s1 in students:
    for s2 in students:
        print(f"{s1} knows {s2}")

# With 10 students → 100 prints. Fine.
# With 1000 students → 1,000,000 prints. Ouch.
# With 10,000 students → 100,000,000 prints. 🔥
```

The difference between 100 operations and 100 million operations isn't "a bit slower." It's the difference between instant and unusable.

That's why we talk about **complexity**: a language for predicting how code behaves as data grows.

---

## The Idea: Counting Steps, Not Seconds

We don't measure complexity in seconds because that depends on your computer. Instead, we count **how many steps** an algorithm takes **relative to the input size**.

We use a notation called **Big O**: it describes the worst-case scenario as the input gets really big.

Think of it like this:
- **How does this function behave when I give it 10 items? 100? 10,000?**
- Big O answers: "it grows like this..."

---

## The Main Characters

### O(1) — Constant Time

The algorithm takes the same number of steps regardless of input size.

```python
def get_first(items):
    return items[0]  # One step. Always.
```

- 10 items → 1 step
- 1,000,000 items → 1 step
- **Examples:** dictionary lookup, array index, hash table get

### O(n) — Linear Time

The algorithm's steps grow in direct proportion to the input.

```python
def find_max(items):
    max_val = items[0]
    for item in items:     # One loop over everything
        if item > max_val:
            max_val = item
    return max_val
```

- 10 items → ~10 steps
- 1,000 items → ~1,000 steps
- **Examples:** looping through a list, linear search, counting items

### O(n²) — Quadratic Time

Nested loops. For each item, loop over everything again.

```python
def has_duplicates(items):
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                return True
    return False
```

- 10 items → ~100 steps
- 1,000 items → ~1,000,000 steps
- **Examples:** bubble sort, nested loops, comparing every pair

### O(log n) — Logarithmic Time

The algorithm cuts the problem in half each time. This is deceptively fast.

```python
# Binary search on a SORTED list
def binary_search(items, target):
    low, high = 0, len(items) - 1
    while low <= high:
        mid = (low + high) // 2
        if items[mid] == target:
            return mid
        elif items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

- 10 items → ~4 steps
- 1,000 items → ~10 steps
- 1,000,000 items → ~20 steps
- **Examples:** binary search, balanced BST lookup, merge sort

### O(n log n) — Linearithmic Time

The sweet spot for sorting. Most efficient general-purpose sorting algorithms live here.

```python
# Merge sort (from the sorting lesson)
# Each item gets processed log(n) times
```

- 10 items → ~33 steps
- 1,000 items → ~10,000 steps
- 1,000,000 items → ~20,000,000 steps
- **Examples:** merge sort, Timsort (Python's built-in sort), many divide-and-conquer algorithms

---

## Visual Comparison

Here's approximately how many steps each complexity takes:

| Input size | O(1) | O(log n) | O(n) | O(n log n) | O(n²) |
|-----------|------|----------|------|-----------|-------|
| 10 | 1 | 4 | 10 | 33 | 100 |
| 100 | 1 | 7 | 100 | 664 | 10,000 |
| 1,000 | 1 | 10 | 1,000 | 9,966 | 1,000,000 |
| 10,000 | 1 | 14 | 10,000 | 132,877 | 100,000,000 |
| 1,000,000 | 1 | 20 | 1,000,000 | 19,931,569 | ✉️🕯️ |

O(n²) at a million items is roughly a trillion operations. At 1 billion operations per second, that's 1,000 seconds — about 17 minutes. For a single operation.

Meanwhile O(log n) finishes in... 20 steps.

---

## How to Read Big O

You might see things like **O(2n)** or **O(n + 100)**. In Big O notation, we drop constants:

- O(2n) → O(n)
- O(n + 1000) → O(n)
- O(n² + n) → O(n²) (for large n, the n² term dominates)

Why? Because Big O describes **growth rate**, not exact counts. When n is 1,000,000, the difference between 2,000,000 and 1,000,000 operations is irrelevant compared to the difference between 1,000,000 and 1,000,000,000,000.

**If you see multiple terms, keep only the one that grows fastest.**

---

## Space Complexity

Time isn't the only resource. **Memory** matters too.

**O(1) space** — uses a fixed amount of extra memory:

```python
def find_max(items):
    max_val = items[0]     # One extra variable — always 1
    for item in items:
        if item > max_val:
            max_val = item
    return max_val
```

**O(n) space** — memory scales with input size:

```python
def get_evens(items):
    evens = []             # Could grow as large as items
    for item in items:
        if item % 2 == 0:
            evens.append(item)
    return evens
```

If items has 1,000,000 elements and they're all even, `evens` also has 1,000,000 elements. That's O(n) space.

**O(n²) space** — memory grows with the square of input:

```python
def make_grid(rows, cols):
    grid = []
    for r in range(rows):
        grid.append([0] * cols)  # rows × cols in memory
    return grid
```

A 10,000 × 10,000 grid is 100 million cells. That's ~800 MB for integers. Your laptop will not enjoy this.

---

## The Tradeoff Mindset

Here's the thing: **you almost always trade time for space, or space for time.**

- **Hash tables** use more memory (space) but give instant lookups (time)
- **Bubble sort** uses almost no extra memory (space) but is painfully slow (time)
- **Merge sort** uses O(n) extra memory (space) but is fast O(n log n) (time)

Real engineering is deciding which tradeoff is right for your situation.

> "Can I afford more memory to make this faster?"
> "Can I afford slower execution to keep memory low?"

---

## Practice: Identify the Complexity

**Your task:** For each function below, figure out its **time complexity** and **space complexity**. Write them in a comment.

```python
# Function A
def sum_list(items):
    total = 0
    for item in items:
        total += item
    return total

# Function B
def print_pairs(items):
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            print(items[i], items[j])

# Function C
def contains_duplicate(items):
    seen = set()
    for item in items:
        if item in seen:
            return True
        seen.add(item)
    return False

# Function D
def reverse_in_place(items):
    left, right = 0, len(items) - 1
    while left < right:
        items[left], items[right] = items[right], items[left]
        left += 1
        right -= 1
    return items

# Function E
def print_all_subsets(items):
    n = len(items)
    for i in range(1 << n):  # 2^n iterations
        subset = []
        for j in range(n):
            if i & (1 << j):
                subset.append(items[j])
        print(subset)
```

Answer what each one is, then check below!

---

## Solutions

### Function A — `sum_list`
```
Time:  O(n)    — loops through each item once
Space: O(1)    — only one extra variable (`total`)
```

### Function B — `print_pairs`
```
Time:  O(n²)   — nested loops, roughly n(n-1)/2 pairs
Space: O(1)    — no additional storage that grows
```

### Function C — `contains_duplicate`
```
Time:  O(n)    — one loop, and set membership is O(1) average
Space: O(n)    — the set could hold all n items
```

This is the classic **space-time tradeoff**: you use O(n) extra memory to avoid O(n²) nested loops.

### Function D — `reverse_in_place`
```
Time:  O(n)    — loops through half the items
Space: O(1)    — just a couple of index variables
```

### Function E — `print_all_subsets`
```
Time:  O(n · 2ⁿ)  — 2ⁿ subsets, each taking O(n) to build
Space: O(n)       — the subset list grows to at most n items
```

O(2ⁿ) is **exponential time**. For n=20, that's about a million subsets. For n=30, it's a billion. For n=40... don't. This is the complexity territory of password cracking and the Travelling Salesman problem.

---

## Quick Cheat Sheet

| Notation | Name | Example |
|----------|------|---------|
| O(1) | Constant | Array index, hash lookup |
| O(log n) | Logarithmic | Binary search, BST search |
| O(n) | Linear | Single loop, linear search |
| O(n log n) | Linearithmic | Merge sort, Timsort |
| O(n²) | Quadratic | Nested loops, bubble sort |
| O(2ⁿ) | Exponential | Subset generation, recursive Fibonacci without memoization |
| O(n!) | Factorial | All permutations — don't go here |

**Rule of thumb for everyday coding:**
- One loop over the data → O(n)
- Nested loops over the same data → O(n²)
- Divide in half each time → O(log n)
- A loop around a divide step → O(n log n)

---

## What You Just Learned

- **Big O** describes how an algorithm scales, not how fast it runs
- **Time complexity** = how many steps as input grows
- **Space complexity** = how much extra memory as input grows
- **Drop constants** — O(2n) = O(n)
- **Tradeoffs** — faster time often costs more space, and vice versa
- O(n²) and beyond become **unusable** at scale

---

## Why This Matters For You

Every lesson you've done is now tagged with its complexity in your head:

| Data Structure | Get | Insert | Delete | Search |
|---------------|-----|--------|--------|--------|
| List (unsorted) | O(1) | O(n) | O(n) | O(n) |
| Stack/Queue | O(n) | O(1) | O(1) | O(n) |
| BST (balanced) | O(log n) | O(log n) | O(log n) | O(log n) |
| Hash Table | O(1) | O(1) | O(1) | O(1)* |

*Average case. Worst-case can be O(n) with bad hashing or collisions.

Now when someone says "dictionary lookups are fast" you know exactly how fast — and why. 💛

---

**You don't need to memorise these.** You need to develop the instinct: "am I writing a loop inside a loop? That's going to hurt at scale." The instinct comes from practice, not flashcards.
