# Advanced Python Lesson 6: Sorting Algorithms 📊

**← Back to [Lesson 5: Hash Maps Deep Dive](05-hash-maps-deep-dive.md)**

---

## Why Learn Sorting?

Python's `list.sort()` and `sorted()` are fantastic — they use **Timsort**, a hybrid algorithm that's O(n log n) in the worst case and O(n) on nearly-sorted data. You should use them in production!

But understanding _how_ sorting works teaches you:
- **Divide and conquer** — one of the most powerful problem-solving patterns
- **Algorithm analysis** — why O(n²) vs O(n log n) matters
- **Recursion in practice** — sorting is recursion's killer app
- **Interview readiness** — sorting questions are everywhere

---

## The Big Picture

| Algorithm | Best | Average | Worst | Space | Stable? |
|-----------|------|---------|-------|-------|---------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | ❌ |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | ✅ |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | ❌ |
| Timsort (Python) | O(n) | O(n log n) | O(n log n) | O(n) | ✅ |

**Stable** means equal elements keep their relative order — important when sorting by multiple criteria!

---

## Merge Sort — The Elegant One

**Strategy:** Divide the list in half, sort each half recursively, then _merge_ the two sorted halves.

```
[38, 27, 43, 3, 9, 82, 10]
         ↓ divide
[38, 27, 43, 3]  |  [9, 82, 10]
    ↓ divide          ↓ divide
[38, 27] [43, 3]  [9, 82] [10]
  ↓ divide  ...      ...     ...
[38] [27] [43] [3] [9] [82] [10]   ← all size 1 (sorted!)
  ↓ merge
[27, 38] [3, 43] [9, 82] [10]
    ↓ merge            ↓ merge
[3, 27, 38, 43]  [9, 10, 82]
         ↓ merge
[3, 9, 10, 27, 38, 43, 82]  ✅
```

### Implementation

```python
def merge_sort(arr):
    """Sort a list using merge sort. Returns a new sorted list."""
    # Base case: 0 or 1 element is already sorted
    if len(arr) <= 1:
        return arr

    # Divide
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    # Conquer — merge the two sorted halves
    return merge(left, right)


def merge(left, right):
    """Merge two sorted lists into one sorted list."""
    result = []
    i = j = 0

    # Compare and take the smaller element
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append any remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**Key insight:** The merge step is O(n). Dividing is O(log n) levels deep. Total: O(n log n).

---

## Quick Sort — The Pragmatic One

**Strategy:** Pick a _pivot_, partition the list into "smaller than pivot" and "larger than pivot", then recursively sort each partition.

```
[38, 27, 43, 3, 9, 82, 10]
Pivot: 38
  Smaller: [27, 3, 9, 10]
  Equal:   [38]
  Larger:  [43, 82]

Sort smaller: [3, 9, 10, 27]
Sort larger:  [43, 82]

Result: [3, 9, 10, 27, 38, 43, 82] ✅
```

### Implementation

```python
def quick_sort(arr):
    """Sort a list using quick sort. Returns a new sorted list."""
    # Base case
    if len(arr) <= 1:
        return arr

    # Choose pivot (middle element — better than first/last on average)
    pivot = arr[len(arr) // 2]

    # Partition
    smaller = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    larger = [x for x in arr if x > pivot]

    # Recursively sort and combine
    return quick_sort(smaller) + equal + quick_sort(larger)
```

**In-place version** (more memory-efficient, but trickier):

```python
def quick_sort_inplace(arr, low=0, high=None):
    """Sort a list in-place using quick sort."""
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_index = partition(arr, low, high)
        quick_sort_inplace(arr, low, pivot_index - 1)
        quick_sort_inplace(arr, pivot_index + 1, high)


def partition(arr, low, high):
    """Partition around a pivot. Returns the pivot's final position."""
    pivot = arr[high]  # Choose last element as pivot
    i = low - 1        # Index of the smaller element

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # Swap

    # Place pivot in its final position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

**⚠️ Quick sort's Achilles' heel:** Choosing a bad pivot (e.g., always the first element on an already-sorted list) gives O(n²). That's why real implementations use "median-of-three" or random pivots.

---

## Insertion Sort — The Simple One (That Timsort Loves)

**Strategy:** Build the sorted list one element at a time by inserting each new element into its correct position.

```python
def insertion_sort(arr):
    """Sort a list using insertion sort."""
    arr = arr.copy()  # Don't modify the original

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # Shift elements greater than key to the right
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key  # Insert key in its correct position

    return arr
```

**Why it matters:** O(n²) in general, but O(n) on _nearly sorted_ data — and very fast for small arrays. Timsort uses insertion sort for small runs (≤ 64 elements).

---

## Visualising the Differences

For `[5, 2, 4, 6, 1, 3]`:

**Insertion Sort:**
```
[5| 2, 4, 6, 1, 3]  ← sorted part | unsorted part
[2, 5| 4, 6, 1, 3]
[2, 4, 5| 6, 1, 3]
[2, 4, 5, 6| 1, 3]
[1, 2, 4, 5, 6| 3]
[1, 2, 3, 4, 5, 6|] ✅
```

**Merge Sort:**
```
[5, 2, 4, 6, 1, 3]
[5, 2, 4] [6, 1, 3]
[5] [2, 4] [6] [1, 3]
[5] [2] [4] [6] [1] [3]
[5] [2, 4] [6] [1, 3]
[2, 4, 5] [1, 3, 6]
[1, 2, 3, 4, 5, 6] ✅
```

---

## Custom Sorting in Python

### The `key` Parameter

```python
# Sort by a specific attribute
words = ["banana", "apple", "Cherry", "date"]
print(sorted(words, key=len))         # ['date', 'apple', 'banana', 'Cherry']
print(sorted(words, key=str.lower))   # ['apple', 'banana', 'Cherry', 'date']

# Sort objects
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
    def __repr__(self):
        return f"{self.name} ({self.grade})"

students = [
    Student("Alice", 85),
    Student("Bob", 92),
    Student("Charlie", 78),
]

# Sort by grade
print(sorted(students, key=lambda s: s.grade))
# [Charlie (78), Alice (85), Bob (92)]

# Sort by grade descending, then name ascending
print(sorted(students, key=lambda s: (-s.grade, s.name)))
# [Bob (92), Alice (85), Charlie (78)]
```

### The `functools.cmp_to_key` Bridge

```python
from functools import cmp_to_key

def compare_strings_by_vowels(a, b):
    """Sort by number of vowels, then alphabetically."""
    vowels = set("aeiouAEIOU")
    count_a = sum(1 for c in a if c in vowels)
    count_b = sum(1 for c in b if c in vowels)

    if count_a != count_b:
        return count_a - count_b
    return -1 if a < b else (1 if a > b else 0)

words = ["hello", "sky", "beautiful", "aeiou", "why"]
print(sorted(words, key=cmp_to_key(compare_strings_by_vowels)))
# ['sky', 'why', 'hello', 'aeiou', 'beautiful']
```

---

## Practice Exercise

**Scenario:** You're building a music library that sorts songs in different ways. You need to implement your own sorting and compare it against Python's built-in sort.

**Your task:**

1. Create `sorting_lab.py`

2. Implement these functions:
   - `merge_sort(arr)` — your own merge sort
   - `quick_sort(arr)` — your own quick sort
   - `insertion_sort(arr)` — your own insertion sort

3. Create a `Song` class:
   ```python
   class Song:
       def __init__(self, title, artist, duration_secs, plays):
           self.title = title
           self.artist = artist
           self.duration = duration_secs
           self.plays = plays
       def __repr__(self):
           return f"'{self.title}' by {self.artist} ({self.duration}s, {self.plays} plays)"
   ```

4. Write a `sort_songs(songs, by)` function that sorts by different criteria:
   - `"title"` — alphabetically by title (case-insensitive)
   - `"artist"` — alphabetically by artist, then by title
   - `"plays"` — most played first
   - `"duration"` — shortest first

5. Write a `benchmark(sort_fn, arr)` function that:
   - Uses `time.perf_counter()` to measure sorting time
   - Returns the time in milliseconds
   - Test all three algorithms on lists of different sizes (100, 1000, 10000)

6. Test everything:
   ```python
   songs = [
       Song("Bohemian Rhapsody", "Queen", 354, 1500),
       Song("Stairway to Heaven", "Led Zeppelin", 482, 1200),
       Song("Hotel California", "Eagles", 391, 900),
       Song("Imagine", "John Lennon", 183, 2000),
       Song("Yesterday", "The Beatles", 125, 1800),
   ]

   print("By plays:", sort_songs(songs, "plays"))
   print("By title:", sort_songs(songs, "title"))

   # Benchmark
   import random
   big_list = [random.randint(1, 10000) for _ in range(1000)]
   print(f"Merge sort: {benchmark(merge_sort, big_list):.2f}ms")
   print(f"Quick sort: {benchmark(quick_sort, big_list):.2f}ms")
   print(f"Insertion sort: {benchmark(insertion_sort, big_list):.2f}ms")
   print(f"Python's sort: {benchmark(sorted, big_list):.2f}ms")
   ```

**Try it yourself first!** Solution below.

---

## Solution

```python
import time
import random


# ── Sorting Algorithms ──────────────────────────────────────────

def merge_sort(arr):
    """Merge sort — O(n log n), stable."""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return _merge(left, right)


def _merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr):
    """Quick sort — O(n log n) average, not stable."""
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    smaller = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    larger = [x for x in arr if x > pivot]

    return quick_sort(smaller) + equal + quick_sort(larger)


def insertion_sort(arr):
    """Insertion sort — O(n²), but O(n) on nearly-sorted data."""
    result = arr.copy()
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result


# ── Song Class ──────────────────────────────────────────────────

class Song:
    def __init__(self, title, artist, duration_secs, plays):
        self.title = title
        self.artist = artist
        self.duration = duration_secs
        self.plays = plays

    def __repr__(self):
        return f"'{self.title}' by {self.artist} ({self.duration}s, {self.plays} plays)"


# ── Song Sorting ────────────────────────────────────────────────

def sort_songs(songs, by="title"):
    """Sort songs by different criteria."""
    songs_copy = list(songs)  # Don't modify original

    if by == "title":
        return sorted(songs_copy, key=lambda s: s.title.lower())
    elif by == "artist":
        return sorted(songs_copy, key=lambda s: (s.artist.lower(), s.title.lower()))
    elif by == "plays":
        return sorted(songs_copy, key=lambda s: s.plays, reverse=True)
    elif by == "duration":
        return sorted(songs_copy, key=lambda s: s.duration)
    else:
        raise ValueError(f"Unknown sort criterion: {by}")


# ── Benchmark ───────────────────────────────────────────────────

def benchmark(sort_fn, arr):
    """Time a sorting function. Returns milliseconds."""
    arr_copy = list(arr)  # Fresh copy for each test

    start = time.perf_counter()
    sort_fn(arr_copy)
    end = time.perf_counter()

    return (end - start) * 1000  # Convert to ms


# ── Test ────────────────────────────────────────────────────────

if __name__ == "__main__":
    songs = [
        Song("Bohemian Rhapsody", "Queen", 354, 1500),
        Song("Stairway to Heaven", "Led Zeppelin", 482, 1200),
        Song("Hotel California", "Eagles", 391, 900),
        Song("Imagine", "John Lennon", 183, 2000),
        Song("Yesterday", "The Beatles", 125, 1800),
    ]

    print("By plays (most first):")
    for song in sort_songs(songs, "plays"):
        print(f"  {song}")

    print("\nBy title (alphabetical):")
    for song in sort_songs(songs, "title"):
        print(f"  {song}")

    print("\nBy artist, then title:")
    for song in sort_songs(songs, "artist"):
        print(f"  {song}")

    print("\nBy duration (shortest first):")
    for song in sort_songs(songs, "duration"):
        print(f"  {song}")

    # Benchmark
    print("\n--- Benchmark (1000 random ints) ---")

    small = [random.randint(1, 10000) for _ in range(100)]
    medium = [random.randint(1, 10000) for _ in range(1000)]
    large = [random.randint(1, 10000) for _ in range(5000)]

    for label, size, data in [("100", 100, small), ("1000", 1000, medium), ("5000", 5000, large)]:
        print(f"\nSize {label}:")
        print(f"  Merge sort:     {benchmark(merge_sort, data):.3f}ms")
        print(f"  Quick sort:     {benchmark(quick_sort, data):.3f}ms")
        print(f"  Insertion sort: {benchmark(insertion_sort, data):.3f}ms")
        print(f"  Python sorted:  {benchmark(sorted, data):.3f}ms")
```

---

## Quick Recap

- **Merge sort** — divide & conquer, O(n log n), stable, uses extra memory
- **Quick sort** — partition around pivot, O(n log n) average, in-place version saves memory
- **Insertion sort** — O(n²) general, O(n) on nearly-sorted data, used inside Timsort
- **Timsort** — Python's hybrid sort, best of merge + insertion, O(n log n)
- **`key` parameter** — custom sorting without writing comparison functions
- **Stable sort** — equal elements stay in original order (merge sort ✅, quick sort ❌)
- **Use `sorted()` and `.sort()`** in real code — but understanding the algorithms makes you a stronger programmer

---

## What's Next?

You've covered linked lists, recursion, trees, heaps, hash maps, and sorting — the core building blocks of algorithms. Ready for graphs? Continue to **[Lesson 7: Graphs & Traversal](07-graphs-traversal.md)** 🕸️

---

**Your turn:** Build the sorting lab! Then try adding `counting_sort(arr, max_value)` — a non-comparison sort that's O(n + k) for integers in a known range. 📊💛
