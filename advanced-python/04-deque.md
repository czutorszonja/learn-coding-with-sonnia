# Advanced Python Lesson 4: Deque — The Double-Ended Queue 🔁

**← Back to [Lesson 3: Queues](03-queues.md)**

---

## What is a Deque?

**Plain English:** A deque (pronounced "deck", short for _double-ended queue_) is a collection where you can add or remove from _either end_ in O(1) time. It's the flexible sibling of stacks and queues — it can be both!

**Real-world analogy:** A deck of cards in your hands:
- You can draw from the top OR the bottom
- You can place a card on top OR tuck it underneath
- You can flip through from either direction
- Unlike a real deck, you can also peek at cards in the middle (but you shouldn't rely on it)

---

## Deque vs Stack vs Queue

```
Stack:     → [ _ _ _ _ ] →     push at right, pop from right (LIFO)
Queue:     → [ _ _ _ _ ] →     push at right, pop from left  (FIFO)
Deque:    ←→ [ _ _ _ _ ] ←→    push/pop from BOTH ends!
```

A deque can _be_ a stack, a queue, or something more flexible.

---

## `collections.deque` — The Real Thing

```python
from collections import deque

d = deque()

# Right-side operations (like a list)
d.append('a')           # Add to right
d.append('b')
d.pop()                 # Remove from right → 'b'

# Left-side operations (impossible with list in O(1)!)
d.appendleft('x')       # Add to left
d.appendleft('y')
d.popleft()             # Remove from left → 'y'

# All O(1)!
```

---

## Full API Reference

```python
from collections import deque

d = deque(['a', 'b', 'c'])

# ── Adding ──────────────────────────
d.append('d')          # Right: deque(['a', 'b', 'c', 'd'])
d.appendleft('z')      # Left:  deque(['z', 'a', 'b', 'c', 'd'])

# ── Removing ────────────────────────
d.pop()                # Right: → 'd',    deque(['z', 'a', 'b', 'c'])
d.popleft()            # Left:  → 'z',    deque(['a', 'b', 'c'])

# ── Peeking ─────────────────────────
d[0]                   # Leftmost:  'a'
d[-1]                  # Rightmost: 'c'

# ── Extending (multiple items) ──────
d.extend(['d', 'e'])   # Right: deque(['a', 'b', 'c', 'd', 'e'])
d.extendleft(['z', 'y'])# Left: deque(['y', 'z', 'a', 'b', 'c', 'd', 'e'])
#                           ↑ note: order is reversed!

# ── Rotation ────────────────────────
d.rotate(1)            # Move right: last becomes first
d.rotate(-2)           # Move left: first becomes last

# ── Utility ─────────────────────────
len(d)                 # Size
d.clear()              # Empty it
d.count('a')           # Count occurrences
d.index('b')           # Find index (O(n) — avoid in loops!)

# ── Capacity (optional) ─────────────
d = deque(maxlen=3)    # Fixed-size deque — old items auto-evicted!
d.append(1)
d.append(2)
d.append(3)
d.append(4)            # deque([2, 3, 4]) — 1 was pushed out!
```

---

## Pattern 1: Deque as Stack + Queue

```python
from collections import deque

class Steque:
    """Stack-ended queue — push at either end, pop from left only."""

    def __init__(self):
        self._items = deque()

    def push(self, item):
        """Add to right (normal queue)."""
        self._items.append(item)

    def push_front(self, item):
        """Add to left (like stack push)."""
        self._items.appendleft(item)

    def pop(self):
        """Remove from left (FIFO)."""
        return self._items.popleft()

    def __len__(self):
        return len(self._items)
```

---

## Pattern 2: Rolling Window / Sliding Window

```python
from collections import deque

def max_in_window(arr, k):
    """Find the maximum in each sliding window of size k."""
    if not arr or k == 0:
        return []

    dq = deque()  # Stores INDICES, not values
    result = []

    for i, value in enumerate(arr):
        # Remove indices that are out of this window
        if dq and dq[0] <= i - k:
            dq.popleft()

        # Remove indices of smaller values (they'll never be max)
        while dq and arr[dq[-1]] <= value:
            dq.pop()

        dq.append(i)

        # Window is full — record the max
        if i >= k - 1:
            result.append(arr[dq[0]])

    return result


print(max_in_window([1, 3, -1, -3, 5, 3, 6, 7], 3))
# Output: [3, 3, 5, 5, 6, 7]

# Explanation:
# Window [1, 3, -1] → max 3
# Window [3, -1, -3] → max 3
# Window [-1, -3, 5] → max 5
# ...
```

This uses a _monotonic deque_ — values in the deque are always decreasing, so the leftmost is always the max!

---

## Pattern 3: Palindrome Checker

```python
from collections import deque

def is_palindrome(text):
    """Check if a string is a palindrome using a deque."""
    # Clean the text: lowercase, remove non-alphanumeric
    cleaned = ''.join(c.lower() for c in text if c.isalnum())
    dq = deque(cleaned)

    while len(dq) > 1:
        left = dq.popleft()
        right = dq.pop()
        if left != right:
            return False

    return True


print(is_palindrome("racecar"))              # True
print(is_palindrome("A man, a plan, a canal: Panama"))  # True
print(is_palindrome("hello"))                # False
```

---

## Pattern 4: Recent Items with `maxlen`

```python
from collections import deque

class RecentItems:
    """Keep track of the N most recent items."""

    def __init__(self, max_items=5):
        self._items = deque(maxlen=max_items)

    def add(self, item):
        self._items.append(item)

    def get_all(self):
        return list(self._items)

    @property
    def most_recent(self):
        return self._items[-1] if self._items else None

    def __contains__(self, item):
        return item in self._items

    def __len__(self):
        return len(self._items)


recent = RecentItems(3)
recent.add("page1")
recent.add("page2")
recent.add("page3")
recent.add("page4")  # page1 is auto-evicted!

print(recent.get_all())     # ['page2', 'page3', 'page4']
print("page1" in recent)   # False
print(recent.most_recent)  # 'page4'
```

**`maxlen` is the secret superpower** — no manual eviction logic needed!

---

## Pattern 5: Breadth-First Search (Clean Version)

```python
from collections import deque

def bfs_shortest_path(graph, start, target):
    """Find shortest path (in edges) from start to target using BFS."""
    queue = deque([(start, [start])])  # (node, path_to_node)
    visited = {start}

    while queue:
        node, path = queue.popleft()

        if node == target:
            return path

        for neighbour in graph.get(node, []):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, path + [neighbour]))

    return None  # No path found


graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

print(bfs_shortest_path(graph, 'A', 'F'))
# ['A', 'C', 'F'] — shortest path is 2 edges
```

---

## Performance: Deque vs List

```python
from collections import deque
import time

def benchmark():
    n = 100_000

    # List — append and pop(0)
    lst = list(range(n))
    start = time.perf_counter()
    for _ in range(1000):
        lst.append(42)
        lst.pop(0)  # O(n) — shifts everything!
    list_time = time.perf_counter() - start

    # Deque — append and popleft
    dq = deque(range(n))
    start = time.perf_counter()
    for _ in range(1000):
        dq.append(42)
        dq.popleft()  # O(1)!
    deque_time = time.perf_counter() - start

    print(f"List:  {list_time:.4f}s")
    print(f"Deque: {deque_time:.4f}s")
    print(f"Deque is {list_time / deque_time:.0f}x faster!")

# List:  ~0.5s
# Deque: ~0.001s
# Deque is ~500x faster!
```

---

## When to Use Which

| Structure | Use When |
|-----------|----------|
| `list` | Random access by index, mostly append-only, small collections |
| `deque` | Adding/removing from both ends, queues, stacks, sliding windows |
| `deque(maxlen=N)` | Keeping only the last N items (auto-eviction!) |
| Stack (custom) | You want to enforce LIFO-only access |
| Queue (custom) | You want to enforce FIFO-only access |

---

## Practice Exercise

**Scenario:** You're building a text editor's clipboard history. You can copy multiple items, but your clipboard only remembers the last 10. You can also cycle back through your copy history and paste older items.

**Your task:**

1. Create `clipboard_history.py` with a `Clipboard` class that:
   - `copy(text)` — adds text to clipboard history (max 10 items!)
   - `paste()` — returns the most recently copied text
   - `cycle_back()` — move one step back in clipboard history
   - `cycle_forward()` — move one step forward
   - `current()` — returns the currently selected clipboard item
   - `all_items()` — returns all items in the clipboard (most recent first)

2. Use a `deque` with `maxlen=10` to store items

3. Use a separate index/cursor to track the "currently selected" item for cycling

4. Handle edge cases:
   - Cycling past the oldest item
   - Cycling forward past the newest
   - Copying resets the cursor to the newest item

5. Test it:
   ```python
   cb = Clipboard()
   cb.copy("Hello")
   cb.copy("World")
   cb.copy("Python")
   cb.copy("Deque")
   cb.copy("Clipboard")

   print(cb.paste())         # "Clipboard" (most recent)
   print(cb.cycle_back())    # "Deque"
   print(cb.cycle_back())    # "Python"
   print(cb.cycle_forward()) # "Deque"

   cb.copy("New text")       # Resets cursor!
   print(cb.current())       # "New text"
   print(cb.all_items())     # Shows last 10, newest first
   ```

**Try it yourself first!** Solution below.

---

## Solution

```python
from collections import deque


class Clipboard:
    """Clipboard history with back/forward cycling, max 10 items."""

    MAX_ITEMS = 10

    def __init__(self):
        self._items = deque(maxlen=self.MAX_ITEMS)
        self._cursor = -1  # Index into _items (-1 = newest)

    def copy(self, text):
        """Add text to clipboard. Resets cursor to newest."""
        self._items.append(text)
        self._cursor = -1  # Reset to newest
        return f"Copied: '{text}'"

    def paste(self):
        """Return the currently selected clipboard item."""
        if not self._items:
            return None
        return self._items[self._cursor]

    def current(self):
        """Alias for paste — returns current item without removing."""
        return self.paste()

    def cycle_back(self):
        """Move selection one step back (older). Returns the item."""
        if not self._items:
            return None

        # Can't go further back than the oldest item
        oldest_idx = -len(self._items)
        if self._cursor > oldest_idx:
            self._cursor -= 1

        return self._items[self._cursor]

    def cycle_forward(self):
        """Move selection one step forward (newer). Returns the item."""
        if not self._items:
            return None

        # Can't go further forward than the newest item
        if self._cursor < -1:
            self._cursor += 1

        return self._items[self._cursor]

    def all_items(self):
        """Return all items, newest first."""
        return list(reversed(self._items))

    def position_info(self):
        """Show where the cursor is in the history."""
        if not self._items:
            return "Clipboard empty"

        total = len(self._items)
        # Convert negative index to position from newest
        position = abs(self._cursor + 1)  # 0 = newest, 1 = second newest, etc.
        return f"Item {position + 1} of {total}"

    def __len__(self):
        return len(self._items)

    def __str__(self):
        if not self._items:
            return "Clipboard: (empty)"

        items = []
        for i, item in enumerate(reversed(self._items)):
            marker = " ← CURRENT" if -(i + 1) == self._cursor else ""
            items.append(f"  [{i}] '{item}'{marker}")
        return "Clipboard:\n" + "\n".join(items)


# --- Test ---
if __name__ == "__main__":
    cb = Clipboard()

    # Copy some text
    cb.copy("Hello")
    cb.copy("World")
    cb.copy("Python")
    cb.copy("Deque")
    cb.copy("Clipboard")

    print(cb)
    print(f"\nPaste: '{cb.paste()}'")       # Clipboard
    print(f"Position: {cb.position_info()}")

    # Cycle through history
    print(f"\n--- Cycling ---")
    print(f"Back:  '{cb.cycle_back()}'")     # Deque
    print(f"Back:  '{cb.cycle_back()}'")     # Python
    print(f"Forward: '{cb.cycle_forward()}'") # Deque
    print(f"Position: {cb.position_info()}")

    # Copy resets cursor
    print(f"\n--- After new copy ---")
    cb.copy("Brand new!")
    print(f"Current: '{cb.current()}'")
    print(cb)

    # Test maxlen by adding 15 items
    print(f"\n--- Max 10 items test ---")
    cb2 = Clipboard()
    for i in range(15):
        cb2.copy(f"Item {i}")
    print(f"Total items: {len(cb2)}")  # Should be 10
    print(f"All items: {cb2.all_items()}")
    # First 5 items (0-4) should have been evicted
    print(f"Has 'Item 0': {'Item 0' in cb2.all_items()}")  # False
    print(f"Has 'Item 14': {'Item 14' in cb2.all_items()}") # True
```

---

## Quick Recap

- **Deque** — double-ended queue, O(1) append/pop from both ends
- **`collections.deque`** — the only correct choice for queue-like behaviour in Python
- **`maxlen`** — automatic eviction; perfect for "last N items" patterns
- **`rotate(n)`** — shift elements; positive=right, negative=left
- **`extendleft()`** — note that items are added in _reverse_ order
- **Use cases:** sliding windows, palindromes, BFS, clipboard history, recent items, undo buffers
- **Never** use `list.pop(0)` — it's O(n) and silently kills performance

---

## What's Next?**

Deques are built on iteration. Now let's go deep into how iteration actually works in Python — iterables, iterators, and generators. Continue to **[Lesson 5: Iterables & Iterators](05-iterables-iterators.md)** 🔄

---

**Your turn:** Build the clipboard! Then try adding an `undo_stack` — when you paste, the old clipboard state is saved so you can undo accidental pastes. 🔁💛
