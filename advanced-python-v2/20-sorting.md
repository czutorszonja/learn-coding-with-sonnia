# Lesson 20: Sorting 📊

**← Back to [Lesson 14: Trees](14-trees.md)**

---

## The Problem: A Messy Bookshelf

Imagine a bookshelf with 100 books, all out of order. You want them alphabetised. What do you do?

Most people would scan the shelf, pull out a book, find where it goes, shift things around. It works, but it takes a while.

How would you describe the process to a computer? That's what sorting algorithms are — precise recipes for putting things in order.

---

## Why Sorting Matters

Sorted data unlocks efficiency:
- **Searching** — finding something in a sorted list is O(log n) with binary search. In an unsorted list? O(n) — check every item.
- **Duplicates** — in a sorted list, duplicates are right next to each other. Instant detection.
- **Ranking** — "top 10" = first 10 items. Trivial when sorted.

That's why sorting is one of the most studied problems in computer science.

---

## Bubble Sort: The Simplest (But Slowest)

Bubble sort is what happens when you teach sorting to someone who's never thought about it:

> Compare adjacent items. If they're in the wrong order, swap them. Keep doing this until no swaps are needed.

```python
def bubble_sort(items):
    n = len(items)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
                swapped = True
        if not swapped:
            break  # Already sorted — early exit!
    return items
```

```python
print(bubble_sort([5, 3, 8, 1, 2]))
# [1, 2, 3, 5, 8]
```

**How it works:** Each pass "bubbles" the largest remaining element to the end. After the first pass, the largest number is at the end. After the second pass, the second-largest is second from the end. And so on.

```
Pass 1: [3, 5, 1, 2, 8]  — 8 bubbled to the end
Pass 2: [3, 1, 2, 5, 8]  — 5 locked in
Pass 3: [1, 2, 3, 5, 8]  — 3 locked in, and sorted! Early exit.
```

**Time:** O(n²) — for n items, roughly n × n / 2 comparisons. A list of 100 items takes ~5,000 comparisons. A list of 10,000 takes ~50 million.

**Space:** O(1) — sorts in place, doesn't use extra memory.

Bubble sort is mainly used as a teaching tool. In real code, you'd almost never use it.

---

## Merge Sort: Divide and Conquer

Merge sort uses recursion. The idea:

> 1. Split the list in half
> 2. Recursively sort each half
> 3. Merge the two sorted halves together

```
[5, 3, 8, 1, 2, 7, 4, 6]
         ↓ split
[5, 3, 8, 1]    [2, 7, 4, 6]
    ↓ split          ↓ split
[5, 3] [8, 1]   [2, 7] [4, 6]
  ↓       ↓        ↓       ↓
[3, 5] [1, 8]   [2, 7] [4, 6]
    ↓ merge         ↓ merge
[1, 3, 5, 8]    [2, 4, 6, 7]
         ↓ merge
[1, 2, 3, 4, 5, 6, 7, 8]
```

The "merge" step is where the magic happens. When you have two sorted piles, merging them is easy — just keep picking the smallest front element from either pile.

```python
def merge_sort(items):
    if len(items) <= 1:
        return items  # Base case: already sorted

    # Divide
    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])

    # Conquer: merge the two sorted halves
    return merge(left, right)


def merge(left, right):
    """Merge two sorted lists into one sorted list."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # One list is exhausted — append whatever remains
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

```python
print(merge_sort([5, 3, 8, 1, 2, 7, 4, 6]))
# [1, 2, 3, 4, 5, 6, 7, 8]
```

**Time:** O(n log n) — always. Even if the list is already sorted. With merge sort, every item is processed about log₂(n) times.

**Space:** O(n) — merge sort creates new lists during merging. It's not in-place like bubble sort.

---

## Bubble Sort vs Merge Sort: The Gap

```python
import time, random

def time_sort(sort_func, items):
    copy = items[:]
    start = time.time()
    sort_func(copy)
    return time.time() - start

n = 2000
data = [random.randint(0, 10000) for _ in range(n)]

bubble_time = time_sort(bubble_sort, data)
merge_time = time_sort(merge_sort, data)

print(f"n = {n}")
print(f"Bubble sort:  {bubble_time:.3f}s")
print(f"Merge sort:   {merge_time:.3f}s")
print(f"Merge is {bubble_time / merge_time:.1f}x faster")
```

On my machine with n=2000:
```
Bubble sort:  0.148s
Merge sort:   0.003s
Merge is 49.3x faster
```

At n=20,000, bubble sort takes ~15 seconds while merge sort takes ~0.03s. That's a 500x difference. At n=200,000, bubble sort becomes unusable.

This is why the choice of algorithm matters more than the choice of programming language.

---

## Python's Built-In Sort

Let's be honest: in real code, you use Python's `sorted()` or `.sort()`:

```python
items = [5, 3, 8, 1, 2]
items.sort()  # In-place
print(items)  # [1, 2, 3, 5, 8]

# Or create a new sorted list without modifying the original:
items = [5, 3, 8, 1, 2]
sorted_items = sorted(items)
print(sorted_items)  # [1, 2, 3, 5, 8]
print(items)         # [5, 3, 8, 1, 2]
```

Python uses **Timsort** — a hybrid of merge sort and insertion sort, adapted to real-world data that often has partially ordered runs. It's O(n log n) worst-case, O(n) best-case (if data is already sorted).

So why learn bubble sort and merge sort? Because:

1. **Understanding** — knowing how sorting works helps you recognise when a problem needs sorting
2. **Interviews** — people ask about these (annoying but true)
3. **Foundation** — the patterns (divide-and-conquer, swapping, merging) show up everywhere

---

## Practice: Sort by Custom Key

**Your task:** Write a function `sort_by_key(items, key_func)` that sorts a list using merge sort, but uses a custom key function instead of direct value comparison.

```python
def sort_by_key(items, key_func):
    # Your merge sort variant here
    pass


# Test: sort strings by their length
words = ["banana", "cat", "elephant", "dog", "apple"]
sorted_words = sort_by_key(words, len)
print(sorted_words)
# ['cat', 'dog', 'apple', 'banana', 'elephant']

# Test: sort tuples by their second element
points = [(1, 5), (3, 2), (2, 4), (5, 1)]
sorted_points = sort_by_key(points, lambda p: p[1])
print(sorted_points)
# [(5, 1), (3, 2), (2, 4), (1, 5)]
```

Hint: instead of comparing `left[i] <= right[j]`, compare `key_func(left[i]) <= key_func(right[j])`.

Save as `custom_sort.py` and try it!

---

## Solution

```python
def merge(left, right, key_func):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key_func(left[i]) <= key_func(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def sort_by_key(items, key_func):
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left = sort_by_key(items[:mid], key_func)
    right = sort_by_key(items[mid:], key_func)
    return merge(left, right, key_func)


# Tests
words = ["banana", "cat", "elephant", "dog", "apple"]
sorted_words = sort_by_key(words, len)
print(sorted_words)
# ['cat', 'dog', 'apple', 'banana', 'elephant']

points = [(1, 5), (3, 2), (2, 4), (5, 1)]
sorted_points = sort_by_key(points, lambda p: p[1])
print(sorted_points)
# [(5, 1), (3, 2), (2, 4), (1, 5)]
```

Now your sort can handle anything — strings, objects, custom structs — as long as you provide a key function. This is exactly how Python's `sorted(list, key=...)` works under the hood.

---

## What You Just Learned

- **Bubble sort** = simple, O(n²), mostly useless in practice
- **Merge sort** = divide-and-conquer, O(n log n), reliable and fast
- **The gap matters** — a bad algorithm can be 500× slower than a good one
- **Python's `sorted()`** uses Timsort — just use it in real code
- **Sorting by custom keys** = we can sort anything

---

## What's Next?

Sorting organises data. But how do you find data FAST without sorting? That's where **hashing** comes in.

Next up: **[Lesson 15: Hashing](15-hashing.md)** — instant lookups ✨

---

**You don't need to memorise sorting algorithms.** You need to understand why some are slow and some are fast. The rest is just labels. 💛
