# Lesson 10b: Binary Search 🔍

**Companion to [Lesson 10: Sorting](10-sorting.md)** — do that one first.

---

## The Problem: Finding a Needle in a Haystack

You just sorted a bookshelf with 1,000 books. Now someone asks: "where's *Dune*?"

You could start at the beginning and check each book one by one:

```
The Alchemist... no.
Animal Farm... no.
Beloved... no.
...
```

That's 500 checks on average. In a library with a million books, that's half a million checks. There's a better way.

---

## Linear Search: The Obvious (Bad) Way

```python
def linear_search(items, target):
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1  # not found
```

This is O(n) — every extra book adds one more check. It works. It's simple. It's also slow.

The problem? **Linear search ignores the fact that your data is sorted.** It's like looking for "Dune" in an alphabetised shelf by starting at A and checking every single book. You'd never do that in real life — you'd open the shelf roughly in the middle.

---

## Binary Search: Cut the Problem in Half

Here's what you actually do at a bookshelf:

1. Open to the middle
2. Is "Dune" before or after where you are?
3. Throw away the half that can't possibly contain it
4. Repeat with the remaining half

That's binary search. Each step eliminates **half** the remaining books.

```python
def binary_search(items, target):
    left, right = 0, len(items) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if items[mid] == target:
            return mid          # found it!
        elif items[mid] < target:
            left = mid + 1      # target is to the right
        else:
            right = mid - 1     # target is to the left
    
    return -1  # not found


# Try it
books = ["Alchemist", "Animal Farm", "Beloved", "Dune", "Frankenstein", 
         "Gatsby", "Hamlet", "Invisible Man", "Jane Eyre", "Kafka on the Shore"]

print(binary_search(books, "Dune"))   # 3
print(binary_search(books, "Moby Dick"))  # -1 (not in the list)
```

Walk through finding "Dune" in those 10 books:

| Step | left | right | mid | items[mid] | Action |
|------|------|-------|-----|------------|--------|
| 1 | 0 | 9 | 4 | "Frankenstein" | Dune < Frankenstein → go left |
| 2 | 0 | 3 | 1 | "Animal Farm" | Dune > Animal Farm → go right |
| 3 | 2 | 3 | 2 | "Beloved" | Dune > Beloved → go right |
| 4 | 3 | 3 | 3 | "Dune" | Found! 🎉 |

4 steps to find it. Linear search would've taken 4 steps too — but with 1,000 books, binary search takes ~10 steps while linear takes ~500.

---

## The Maths: Why It's O(log n)

Every step cuts the search space in half:

```
1,000 → 500 → 250 → 125 → 63 → 32 → 16 → 8 → 4 → 2 → 1
```

That's 10 steps for 1,000 items. For 1,000,000 items? About 20 steps.

The pattern: **steps needed = log₂(n)**. This is what O(log n) means.

```python
import math

for size in [10, 100, 1000, 10000, 100000, 1000000]:
    steps = math.ceil(math.log2(size))
    print(f"{size:>10,} items → at most {steps} steps")
```

```
        10 items → at most 4 steps
       100 items → at most 7 steps
     1,000 items → at most 10 steps
    10,000 items → at most 14 steps
   100,000 items → at most 17 steps
 1,000,000 items → at most 20 steps
```

Look at that curve — doubling the data only adds ONE more step.

---

## The Tricky Parts (Where People Get It Wrong)

### 1. The `while left <= right` condition

Why `<=` and not `<`? Because when `left == right`, there's still one element to check. If you use `<`, you'll skip the last element.

```python
# ❌ Wrong — misses the last element when it's the target
while left < right:
    ...

# ✅ Right
while left <= right:
    ...
```

### 2. Integer overflow (not a problem in Python, but...)

In languages like Java or C++, `(left + right)` can overflow for huge arrays. The safe version:

```python
mid = left + (right - left) // 2
```

In Python, integers are arbitrary precision, so `(left + right) // 2` is fine. But it's good to know the pattern.

### 3. Sorted data only!

Binary search **requires sorted data**. If the list isn't sorted, you'll get garbage:

```python
unsorted = [5, 1, 9, 3, 7]
print(binary_search(unsorted, 3))  # might return -1 or wrong index
```

This is why sorting and searching are inseparable — you sort FIRST so you can search FAST.

---

## Python's `bisect` Module: Don't Reinvent the Wheel

Python has binary search built in. The `bisect` module gives you O(log n) insertion points into sorted lists:

```python
import bisect

scores = [55, 62, 70, 78, 85, 92]

# Where would 75 go to keep the list sorted?
pos = bisect.bisect_left(scores, 75)
print(pos)  # 3 — insert at index 3: [55, 62, 70, 75, 78, 85, 92]

# Where would 70 go? (value already exists)
pos = bisect.bisect_left(scores, 70)
print(pos)  # 2 — leftmost position of 70

pos = bisect.bisect_right(scores, 70)
print(pos)  # 3 — rightmost position (after existing 70s)

# Keep a list sorted as you add to it
leaderboard = []
bisect.insort(leaderboard, ("Alice", 95))   # [('Alice', 95)]
bisect.insort(leaderboard, ("Bob", 82))     # [('Bob', 82), ('Alice', 95)]
bisect.insort(leaderboard, ("Carol", 88))   # [('Bob', 82), ('Carol', 88), ('Alice', 95)]
```

`bisect_left` vs `bisect_right`: the difference only matters when the value already exists. Think "insert before" (left) vs "insert after" (right).

---

## Beyond Lists: Search in Different Structures

Binary search isn't the only kind of search. Different data structures give you different trade-offs:

| Structure | Search Speed | Needs Sorting? | Notes |
|-----------|-------------|----------------|-------|
| Unsorted list | O(n) — linear | No | Simplest, slowest |
| Sorted list | O(log n) — binary | Yes | Must sort first (O(n log n)) |
| Set / Dict | O(1) — hash | No | Instant! But uses more memory |
| BST (balanced) | O(log n) | Built-in | The tree IS the search structure |

The lesson: **how you store your data determines how fast you can find it.**

---

## Real-World Examples

```python
# Finding a word in a dictionary (binary search on sorted keys)
words = sorted(["python", "javascript", "rust", "go", "zig"])
index = binary_search(words, "rust")  # 3

# Finding the insertion point for a high score
high_scores = [100, 200, 350, 500, 750, 1000]
import bisect
rank = len(high_scores) - bisect.bisect_right(high_scores, 420) + 1
print(f"Score 420 is rank #{rank}")  # Rank 4

# Checking if a username is taken (O(1) with a set!)
usernames = {"alice", "bob", "carol", "dave"}
print("alice" in usernames)   # True — instant!
print("zara" in usernames)    # False — also instant!
```

---

## Practice: Implement Binary Search

**Your task:** Write `binary_search(items, target)` from scratch — WITHOUT looking at the code above.

Requirements:
- Return the **index** if found, `-1` if not found
- Handle empty lists (return -1)
- Use a `while` loop (no recursion — we'll save that for another day)

Then test it:

```python
# Test 1: Found at the beginning
assert binary_search([1, 2, 3, 4, 5], 1) == 0

# Test 2: Found at the end  
assert binary_search([1, 2, 3, 4, 5], 5) == 4

# Test 3: Found in the middle
assert binary_search([1, 2, 3, 4, 5], 3) == 2

# Test 4: Not found
assert binary_search([1, 2, 3, 4, 5], 6) == -1

# Test 5: Empty list
assert binary_search([], 1) == -1

# Test 6: Single element — found
assert binary_search([42], 42) == 0

# Test 7: Single element — not found
assert binary_search([42], 7) == -1

# Test 8: Even-length list
assert binary_search([10, 20, 30, 40], 20) == 1

# Test 9: Duplicates (return any match)
result = binary_search([1, 3, 3, 3, 5], 3)
assert result in [1, 2, 3]  # any position with 3 is valid

print("All tests passed! 🎉")
```

**Bonus challenge:** Modify your function to return the **insertion point** when the target isn't found — i.e., the index where `target` would go to keep the list sorted. This is what `bisect.bisect_left` does.

```python
assert binary_search_insert([1, 3, 5, 7], 4) == 2   # 4 goes between 3 and 5
assert binary_search_insert([1, 3, 5, 7], 0) == 0   # before first element
assert binary_search_insert([1, 3, 5, 7], 9) == 4   # after last element
```

---

Binary search is one of those algorithms that's simple to understand but tricky to get right on first try. The off-by-one errors are legendary — even professional developers mess them up. But now you know the intuition. 💛

---

**Next up:** sorting made binary search possible. But what if you don't want to store all the data at all? That's where **[Lesson 11: Iterables & Iterators](11-iterables-iterators.md)** come in — generate values on demand 🔄
