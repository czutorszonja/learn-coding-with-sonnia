# Advanced Python Lesson 8: Recursion Deep Dive — Functions That Call Themselves 🔄

**← Back to [Lesson 7: Linked Lists](07-linked-lists.md)**

---

## What is Recursion?

**Plain English:** Recursion is when a function calls _itself_ to solve a smaller version of the same problem, until it reaches the simplest possible case.

**Real-world analogy:** Imagine you're looking up a word in the dictionary:
1. You read the definition
2. It uses a word you don't know
3. You look up _that_ word
4. It uses another unfamiliar word…
5. Eventually you reach a word defined with words you already know
6. Now you work _backwards_, understanding each definition in turn

Each lookup is a "recursive call" — and the word you already know is the "base case."

---

## The Two Essential Parts

Every recursive function needs **two things**:

```python
def recursive_function(problem):
    # 1. BASE CASE — the simplest version, stop here!
    if problem_is_trivial:
        return trivial_answer

    # 2. RECURSIVE CASE — break it down and call yourself
    smaller_problem = make_smaller(problem)
    partial_answer = recursive_function(smaller_problem)
    return combine(partial_answer)
```

**Without a base case → infinite recursion → stack overflow → 💥**

---

## Classic Example: Factorial

```
5! = 5 × 4 × 3 × 2 × 1 = 120
```

Notice: `5! = 5 × 4!` and `4! = 4 × 3!` … and `1! = 1` (base case!)

```python
def factorial(n):
    # Base case: 1! = 1 (also 0! = 1)
    if n <= 1:
        return 1

    # Recursive case: n! = n × (n-1)!
    return n * factorial(n - 1)


print(factorial(5))  # 120
```

**What happens in the call stack:**

```
factorial(5)
  → 5 * factorial(4)
       → 4 * factorial(3)
            → 3 * factorial(2)
                 → 2 * factorial(1)
                      → 1          ← base case!
                 ← 2 * 1 = 2
            ← 3 * 2 = 6
       ← 4 * 6 = 24
  ← 5 * 24 = 120
```

The calls "stack up" waiting for answers, then "unwind" as each answer bubbles back up!

---

## Visualising the Call Stack

```python
def countdown(n):
    """Print numbers counting down, then back up."""
    if n <= 0:
        print("Blast off! 🚀")
        return

    print(f"Entering: {n}")     # Before recursive call
    countdown(n - 1)
    print(f"Exiting:  {n}")     # After recursive call


countdown(3)

# Output:
# Entering: 3
# Entering: 2
# Entering: 1
# Blast off! 🚀
# Exiting:  1
# Exiting:  2
# Exiting:  3
```

**Everything before** the recursive call happens on the way _down_. **Everything after** happens on the way _back up_.

---

## Recursion on Data Structures

### Summing a Linked List (Recursively)

Builds on your linked list knowledge!

```python
def sum_list(head):
    """Sum all values in a linked list."""
    # Base case: empty list
    if head is None:
        return 0

    # Recursive case: current value + sum of the rest
    return head.data + sum_list(head.next)
```

### Reversing a Linked List (Recursively)

```python
def reverse_recursive(head):
    """Reverse a linked list recursively."""
    # Base case: empty or single node
    if head is None or head.next is None:
        return head

    # Recursive case: reverse the rest, then attach current to the end
    new_head = reverse_recursive(head.next)
    head.next.next = head   # The node after current now points back
    head.next = None        # Current becomes the new tail
    return new_head
```

### Fibonacci (Classic — But Watch Out!)

```python
def fib(n):
    """Return the nth Fibonacci number."""
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

# fib(5) = fib(4) + fib(3)
#        = (fib(3) + fib(2)) + (fib(2) + fib(1))
#        = ... lots of repeated work!
```

⚠️ **This is O(2ⁿ) — terribly slow for n > 35!** Every call spawns two more. This is why we need…

---

## Memoization — Remember What You've Seen

```python
def fib_memo(n, memo=None):
    """Fibonacci with memoization — O(n)!"""
    if memo is None:
        memo = {}

    # Have we solved this before?
    if n in memo:
        return memo[n]

    # Base case
    if n <= 1:
        return n

    # Solve, store, return
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


print(fib_memo(100))  # 354224848179261915075 — instant!
```

Memoization is a **cache** — you trade a bit of memory for massive speed.

---

## Recursion vs Iteration

| Aspect | Recursion | Iteration (Loops) |
|--------|-----------|-------------------|
| Readability | Elegant for tree/graph problems | Clearer for simple loops |
| Memory | Uses call stack (risk: overflow) | Uses constant memory |
| Speed | Slightly slower (function call overhead) | Slightly faster |
| Best for | Trees, graphs, divide & conquer | Linear repetition |

**Rule of thumb:** Use recursion when the problem is _naturally recursive_ (trees, graphs, backtracking). Use iteration for simple repetition.

---

## Tail Recursion (For the Curious)

Python does NOT optimise tail recursion, but it's good to know:

```python
# Normal recursion: must keep stack frame (waiting for multiply)
def fact_normal(n):
    if n <= 1:
        return 1
    return n * fact_normal(n - 1)  # Must wait for result, then multiply

# Tail recursion: no work left after recursive call
def fact_tail(n, accumulator=1):
    if n <= 1:
        return accumulator
    return fact_tail(n - 1, n * accumulator)  # Nothing to wait for!
```

In languages like Scheme or Haskell, tail recursion is as efficient as a loop. Python doesn't optimise it (Guido's choice), but the pattern is still elegant.

---

## Practice Exercise

**Scenario:** You're building a file system explorer that can search through nested folders.

**Your task:**

1. Create a file called `recursive_explorer.py`

2. Build a `FileNode` class representing either a file or folder:
   ```python
   class FileNode:
       def __init__(self, name, is_folder=False):
           self.name = name
           self.is_folder = is_folder
           self.children = []      # Files/folders inside (if folder)
           self.size = 0           # File size in KB (if file)
   ```

3. Implement these recursive functions:
   - `count_files(node)` — return total number of files (not folders) in the tree
   - `total_size(node)` — return total size of all files in KB
   - `find_by_name(node, name)` — return the node with that name, or None
   - `list_all_paths(node, prefix="")` — return a list of full paths like `["/home/docs/report.pdf", "/home/photos/sunset.jpg"]`
   - `max_depth(node)` — return the deepest nesting level (a file in root = depth 1)

4. Create a test tree and verify your functions:
   ```python
   root = FileNode("home", is_folder=True)
   docs = FileNode("docs", is_folder=True)
   photos = FileNode("photos", is_folder=True)
   report = FileNode("report.pdf", is_folder=False)
   report.size = 150
   notes = FileNode("notes.txt", is_folder=False)
   notes.size = 25
   sunset = FileNode("sunset.jpg", is_folder=False)
   sunset.size = 500

   docs.children.extend([report, notes])
   photos.children.append(sunset)
   root.children.extend([docs, photos])
   ```

**Expected output:**
```
Total files: 3
Total size: 675 KB
Find 'sunset.jpg': <FileNode object>
Find 'missing.txt': None
Paths: ['/home/docs/report.pdf', '/home/docs/notes.txt', '/home/photos/sunset.jpg']
Max depth: 3
```

**Try it yourself first!** Solution below.

---

## Solution

```python
class FileNode:
    """A node in a file system tree — either a file or a folder."""

    def __init__(self, name, is_folder=False):
        self.name = name
        self.is_folder = is_folder
        self.children = []      # Contents (if folder)
        self.size = 0           # Size in KB (if file)

    def __repr__(self):
        kind = "📁" if self.is_folder else "📄"
        return f"{kind} {self.name}"


def count_files(node):
    """Count all files (not folders) in the tree."""
    if node is None:
        return 0

    # If it's a file, count as 1
    if not node.is_folder:
        return 1

    # It's a folder — sum up all children recursively
    total = 0
    for child in node.children:
        total += count_files(child)
    return total


def total_size(node):
    """Sum the size of all files in the tree."""
    if node is None:
        return 0

    if not node.is_folder:
        return node.size

    total = 0
    for child in node.children:
        total += total_size(child)
    return total


def find_by_name(node, name):
    """Search the tree for a node with the given name."""
    if node is None:
        return None

    if node.name == name:
        return node

    if node.is_folder:
        for child in node.children:
            result = find_by_name(child, name)
            if result is not None:
                return result

    return None


def list_all_paths(node, prefix=""):
    """Return a list of full paths to every file."""
    if node is None:
        return []

    current_path = f"{prefix}/{node.name}"

    if not node.is_folder:
        return [current_path]

    # It's a folder — collect paths from all children
    paths = []
    for child in node.children:
        paths.extend(list_all_paths(child, current_path))
    return paths


def max_depth(node):
    """Return the deepest nesting level (root = depth 0)."""
    if node is None:
        return 0

    if not node.is_folder or len(node.children) == 0:
        # A file or empty folder has depth 1 from this point
        return 1

    # Folder with children — deepest child + 1
    deepest = 0
    for child in node.children:
        child_depth = max_depth(child)
        deepest = max(deepest, child_depth)
    return deepest + 1


# --- Test ---
if __name__ == "__main__":
    root = FileNode("home", is_folder=True)

    docs = FileNode("docs", is_folder=True)
    photos = FileNode("photos", is_folder=True)

    report = FileNode("report.pdf", is_folder=False)
    report.size = 150
    notes = FileNode("notes.txt", is_folder=False)
    notes.size = 25
    sunset = FileNode("sunset.jpg", is_folder=False)
    sunset.size = 500

    docs.children.extend([report, notes])
    photos.children.append(sunset)
    root.children.extend([docs, photos])

    print(f"Total files: {count_files(root)}")          # 3
    print(f"Total size: {total_size(root)} KB")         # 675
    print(f"Find 'sunset.jpg': {find_by_name(root, 'sunset.jpg')}")
    print(f"Find 'missing.txt': {find_by_name(root, 'missing.txt')}")
    print(f"Paths: {list_all_paths(root)}")
    print(f"Max depth: {max_depth(root)}")              # 3
```

---

## Quick Recap

- **Recursion** — function that calls itself with a smaller problem
- **Base case** — the simplest version; without it, infinite recursion!
- **Recursive case** — break problem down, call yourself, combine results
- **Call stack** — each call stacks up, then unwinds as answers bubble back
- **Memoization** — cache results to avoid repeated work (critical for Fibonacci!)
- **Best for** — trees, graphs, backtracking, divide-and-conquer
- **Watch out for** — stack overflow on deep recursion (Python's limit is ~1000)

---

## What's Next?

Recursion + linked lists = the perfect setup for trees! Continue to **[Lesson 9: Trees & Binary Search Trees](09-trees-binary-search-trees.md)** 🌳

---

**Your turn:** Build the file explorer! Then try adding `find_largest_file(node)` — returns the file node with the biggest size. 🔄💛
