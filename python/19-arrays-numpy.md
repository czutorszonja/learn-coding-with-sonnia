# Python Lesson: Arrays — When Lists Aren't Enough

**Prerequisites:** [Lists](03-lists-explained.md), [Loops](04-loops-explained.md)

---

## 1. What Are Arrays?

A Python **list** is flexible — it can hold anything:

```python
mixed = ["hello", 42, True, [1, 2, 3]]  # strings, numbers, booleans, even other lists!
```

That flexibility costs memory and speed. An **array** is the opposite: every element must be the **same type**, and that type is locked in when you create it. In exchange, arrays are leaner and faster.

Python gives you two kinds of arrays:

| Kind | Where | When to use |
|------|-------|------------|
| `array.array` | Built-in `array` module | Small, fixed-type number storage |
| `numpy.ndarray` | Third-party `numpy` | Data science, maths, big datasets |

---

## 2. array.array — Python's Built-in Array

Import the module, pick a type code, and you're off:

```python
import array

# 'i' = signed integer, 'f' = float, 'd' = double
scores = array.array('i', [85, 92, 78, 95])

print(scores)      # array('i', [85, 92, 78, 95])
print(scores[0])   # 85 — same square-bracket access as lists
print(scores[2])   # 78
```

### The type codes you'll actually use:

| Code | Type | Example |
|------|------|---------|
| `'i'` | signed integer | `array('i', [1, 2, 3])` |
| `'f'` | float (32-bit) | `array('f', [1.5, 2.0])` |
| `'d'` | double (64-bit float) | `array('d', [1.5, 2.0])` |
| `'b'` | signed char | `array('b', [1, 2])` |

### Everything is the same type — enforced:

```python
scores = array.array('i', [85, 92, 78, 95])
scores.append(88)        # ✅ another integer
scores.append("hello")   # ❌ TypeError: integer required
```

### Accessing elements — just like lists:

```python
scores[0]        # 85 — index
scores[-1]       # 95 — negative index (last)
scores[1:3]      # array('i', [92, 78]) — slicing works
len(scores)      # 4
for s in scores:  # looping works
    print(s)
```

### When to bother with array.array?

Honestly? Rarely. Use it if you're storing thousands of numbers and memory matters. Otherwise, lists or NumPy.

---

## 3. What Is NumPy?

NumPy is the **real** array library — the engine behind every data science tool in Python. Its main type is `ndarray` (n-dimensional array).

The killer feature? **Vectorised operations** — you do maths on the whole array at once, no loops:

```python
import numpy as np

nums = np.array([1, 2, 3, 4, 5])

# Without NumPy (list):
# doubled = [n * 2 for n in nums]  ← loop needed

# With NumPy:
doubled = nums * 2          # array([2, 4, 6, 8, 10]) — no loop!
squared = nums ** 2         # array([1, 4, 9, 16, 25])
big = nums[nums > 3]        # array([4, 5]) — boolean filtering
```

That `nums * 2` — compare with a list where `[1, 2, 3] * 2` gives you `[1, 2, 3, 1, 2, 3]` (repetition, not multiplication).

NumPy arrays also have a fixed **dtype**:

```python
arr = np.array([1, 2, 3])
print(arr.dtype)  # int64 (or int32, depending on your machine)

arr_float = np.array([1, 2, 3], dtype=np.float64)
print(arr_float)  # [1. 2. 3.]
```

### 2D arrays and beyond:

```python
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

print(matrix[0, 0])     # 1 — row 0, column 0
print(matrix[1, 2])     # 6 — row 1, column 2
print(matrix[:, 0])     # [1 4 7] — all rows, column 0
print(matrix.sum())     # 45
print(matrix.mean())    # 5.0
```

---

## 4. What Are Linked Lists?

A linked list is a chain of **nodes**. Each node holds two things:
- A **value**
- A **pointer** to the next node (or `None` if it's the end)

```
[5 | → ] → [12 | → ] → [7 | → ] → None
```

Unlike an array (where everything sits in one block of memory), linked list nodes are scattered. You follow the arrows.

### Types of linked lists:

| Type | Structure |
|------|-----------|
| **Singly linked** | Each node points to the next. One-way only. |
| **Doubly linked** | Each node points to next AND previous. Can go both ways. |
| **Circular** | The last node points back to the first (loop). |

### Pros and cons:

**✅ Pros:**
- Insert/delete at the start: **O(1)** — just relink (array would shift everything)
- Dynamic size — no resizing overhead
- No wasted capacity

**❌ Cons:**
- No random access — to get item #500, you walk through 499 nodes (**O(n)**)
- More memory per element (storing pointers)
- Worse cache performance (nodes scattered in memory)

Python doesn't have a built-in linked list. The closest thing is `collections.deque`, which is a doubly-linked list under the hood. But the deeper lesson on building your own linked list is in **Lesson 18: Linked Lists**.

---

## 5. Quick Cheat Sheet

```python
# --- array.array ---
import array
a = array.array('i', [1, 2, 3])
a[0]          # 1
a.append(4)   # array('i', [1, 2, 3, 4])
a[1:3]        # slice: array('i', [2, 3])

# --- NumPy ---
import numpy as np
b = np.array([1, 2, 3])
b * 2         # array([2, 4, 6]) ← vectorised!
b > 1         # array([False, True, True])
b[b > 1]      # array([2, 3]) ← boolean mask
b.sum()       # 6
b.mean()      # 2.0

# --- Linked List (from collections.deque) ---
from collections import deque
ll = deque([1, 2, 3])
ll.appendleft(0)   # deque([0, 1, 2, 3])
ll.popleft()        # 0
```

---

## Practice

1. Create an `array.array('i')` with the numbers 10, 20, 30, 40. Print the third element.
2. Create the same thing as a NumPy array and multiply every element by 3.
3. What happens if you try to `append("hello")` to your `array.array('i')`? Try it.
4. Why would you use an `array.array` instead of a list? When would NumPy be the better choice?

---

## Answers

<details>
<summary>Click to reveal</summary>

```python
# 1. array.array
import array
a = array.array('i', [10, 20, 30, 40])
print(a[2])  # 30 (third element, 0-indexed)

# 2. NumPy
import numpy as np
b = np.array([10, 20, 30, 40])
print(b * 3)  # [30 60 90 120]

# 3. What happens
a.append("hello")  # ❌ TypeError: integer required

# 4. Why?
# array.array → storing thousands of pure numbers, memory-conscious
# NumPy → any maths, data science, big datasets, multi-dimensional
# list → general purpose, mixed types, small collections
```

</details>

---

Happy learning! 🧮
