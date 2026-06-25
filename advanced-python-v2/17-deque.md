# Lesson 17: Deque — Add and Remove from Both Ends

**← Back to [Lesson 16: Queues](16-queues.md)**

---

## The Problem: A Queue That Can Do Both

Stacks are great for "last thing first." Queues are great for "first thing first."

But what about a clipboard that remembers your last 10 copies? You add to the end, and when you add an 11th, the oldest gets pushed out. That's adding at the back AND removing from the front — in the same structure. You'd have to manage both ends.

Or a deck of cards where you can draw from the top or the bottom. A list can do `pop(0)` but it's slow. A deque does both ends instantly.

---

## The Idea: Double-Ended

A **deque** (pronounced "deck", short for double-ended queue) lets you add and remove from EITHER end. It's a stack and a queue rolled into one.

```python
from collections import deque

d = deque(['a', 'b', 'c'])

# Right side (like a list)
d.append('d')          # Add to right:  deque(['a', 'b', 'c', 'd'])
d.pop()                # Remove right:  → 'd'

# Left side (impossible with a regular list!)
d.appendleft('z')      # Add to left:   deque(['z', 'a', 'b', 'c'])
d.popleft()            # Remove left:   → 'z'

# Peek at either end
d[0]                   # Leftmost
d[-1]                  # Rightmost
```

---

## The Secret Superpower: `maxlen`

Set a maximum size, and old items get **automatically evicted** when new ones arrive:

```python
from collections import deque

# A "last 5 items" tracker — no manual cleanup needed!
recent = deque(maxlen=5)

for i in range(1, 10):
    recent.append(f"event-{i}")
    print(list(recent))

# Output:
# ['event-1']
# ['event-1', 'event-2']
# ['event-1', 'event-2', 'event-3']
# ['event-1', 'event-2', 'event-3', 'event-4']
# ['event-1', 'event-2', 'event-3', 'event-4', 'event-5']
# ['event-2', 'event-3', 'event-4', 'event-5', 'event-6']  ← event-1 auto-evicted!
# ['event-3', 'event-4', 'event-5', 'event-6', 'event-7']
# ['event-4', 'event-5', 'event-6', 'event-7', 'event-8']
# ['event-5', 'event-6', 'event-7', 'event-8', 'event-9']
```

No `if len > 5: remove oldest` — `maxlen` handles it for you.

**Use cases:** browser history (last 10 pages), terminal scrollback, undo buffer, recent searches, error logs.

---

## Another Trick: `rotate()`

Shift all elements left or right:

```python
from collections import deque

d = deque(['a', 'b', 'c', 'd', 'e'])
print(d)  # deque(['a', 'b', 'c', 'd', 'e'])

d.rotate(2)   # Move everything right by 2
print(d)  # deque(['d', 'e', 'a', 'b', 'c'])

d.rotate(-1)  # Move everything left by 1
print(d)  # deque(['e', 'a', 'b', 'c', 'd'])
```

Useful for round-robin scheduling ("whose turn is it next?") or games where turns cycle.

---

## When to Use What

| Structure | Use case |
|-----------|----------|
| `list` | Random access by index, mostly append-only |
| Stack (list-based) | Undo/redo, back button, expression evaluation |
| Queue (deque-based) | Fair processing: print queue, ticket system |
| `deque(maxlen=N)` | "Last N items" — auto-eviction! |
| `deque` (unlimited) | Palindromes, BFS, sliding windows |

---

## Practice: Clipboard History

**Your task:** Build a clipboard that remembers your last 10 copies and lets you cycle through them.

Create a `Clipboard` class:
- `copy(text)` — adds text to the clipboard (max 10 items, oldest auto-evicted)
- `paste()` — returns the most recently copied text
- `cycle_back()` — move one step back in history
- `cycle_forward()` — move one step forward
- `current()` — returns the currently selected item

**Think about it:** The clipboard uses `maxlen=10` so old items automatically disappear. The cursor starts at `-1` (the newest item). Moving back makes it `-2`, `-3`, etc. Copying new text resets the cursor to `-1`.

**Test it:**

```python
cb = Clipboard()
cb.copy("Hello")
cb.copy("World")
cb.copy("Python")

print(cb.paste())       # Python (most recent)
print(cb.cycle_back())  # World
print(cb.cycle_back())  # Hello
print(cb.cycle_forward())  # World

cb.copy("New text")
print(cb.current())     # New text (cursor reset)
```

Create `clipboard.py` and try it!

---

## Solution

```python
from collections import deque


class Clipboard:
    MAX_ITEMS = 10

    def __init__(self):
        self._items = deque(maxlen=self.MAX_ITEMS)
        self._cursor = -1  # -1 = newest item

    def copy(self, text):
        """Add text to clipboard. Resets cursor to newest."""
        self._items.append(text)
        self._cursor = -1
        return f"Copied: '{text}'"

    def paste(self):
        """Return the currently selected item."""
        if not self._items:
            return None
        return self._items[self._cursor]

    def current(self):
        return self.paste()

    def cycle_back(self):
        """Move to an older item."""
        if not self._items:
            return None
        oldest = -len(self._items)
        if self._cursor > oldest:
            self._cursor -= 1
        return self._items[self._cursor]

    def cycle_forward(self):
        """Move to a newer item."""
        if not self._items:
            return None
        if self._cursor < -1:
            self._cursor += 1
        return self._items[self._cursor]

    def __len__(self):
        return len(self._items)


# Test
cb = Clipboard()
cb.copy("Hello")
cb.copy("World")
cb.copy("Python")

print(cb.paste())          # Python
print(cb.cycle_back())     # World
print(cb.cycle_back())     # Hello
print(cb.cycle_forward())  # World

cb.copy("New text")
print(cb.current())        # New text
```

---

## What You Just Learned

- **Deque = double-ended queue** — add/remove from either end
- **`maxlen`** — automatic eviction, perfect for "last N items"
- **`rotate()`** — cycle elements without manual shuffling
- **Use `deque` for queues**, never `list.pop(0)`

---

## What's Next?

You've now got stacks, queues, and deques. All of them are iterable — you can loop over them. But how does iteration actually WORK in Python? What's happening behind `for item in collection:`?

Continue to **[Lesson 18: Linked Lists](18-linked-lists.md)** ⛓️

---

**Your turn:** Build the clipboard! Then add a `show_all()` method that prints all items with `→` marking the current selection. 🔁💛
