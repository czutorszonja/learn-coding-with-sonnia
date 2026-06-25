# Lesson 20: Heaps — Always Grab the Smallest Instantly

**← Back to [Lesson 19: Trees](19-trees.md)**

---

## The Problem: Finding Smallest in a Shifting Pile

You've got a list of tasks, each with a priority. New tasks keep arriving. At any moment, you need the **most urgent** one.

```python
tasks = [("Fix login", 3), ("Send report", 1), ("Reply email", 5)]

# New task arrives — it's urgent!
tasks.append(("Server down", 1))

# What's the most urgent right now?
# We'd have to scan the whole list... again...
most_urgent = min(tasks, key=lambda t: t[1])
```

Every time a new task arrives, finding the minimum means checking every item. For 10 items, fine. For 10,000, that's 10,000 comparisons every time you need the most urgent one.

If only there were a data structure where the **smallest thing is always right at the top**, no scanning needed…

---

## The Idea: Keep the Smallest at the Root

A **heap** is a list with a special arrangement rule:

> Every parent must be ≤ (smaller than or equal to) its children.

That's it. One rule. And it guarantees the smallest element is always at position `[0]`.

```
        2          ← Smallest, always at the root
       / \
      5   8
     / \ /
    9  7 10
```

This is a **min-heap**. The smallest value rises to the top like a bubble.

You don't create nodes and pointers like a tree — the heap is stored as a **plain Python list**:

```python
heap = [2, 5, 8, 9, 7, 10]
#      root  children of 2  children of 5
```

The magic is in the arithmetic:
- Left child of position `i` = position `2*i + 1`
- Right child of position `i` = position `2*i + 2`
- Parent of position `i` = position `(i - 1) // 2`

No node classes. No pointers. Just a list and some index math — Python's `heapq` handles all of it for you.

**What about a max-heap?** Same idea, but parent ≥ children — largest at the root. Python only has min-heap built in, so for max-heap you flip the sign (negate values).

---

## Step by Step

### Part 1: Your First Heap

```python
import heapq

tasks = []

# Push items — heapq keeps the min-heap property
heapq.heappush(tasks, 5)
heapq.heappush(tasks, 2)
heapq.heappush(tasks, 8)
heapq.heappush(tasks, 1)

print(tasks)  # [1, 2, 8, 5] — smallest at [0], rest in heap order

# Pop the smallest
print(heapq.heappop(tasks))  # 1
print(heapq.heappop(tasks))  # 2
print(heapq.heappop(tasks))  # 5
print(heapq.heappop(tasks))  # 8
```

Three key operations:

| What | How | Time |
|------|-----|------|
| Add an item | `heapq.heappush(heap, item)` | O(log n) |
| Remove smallest | `heapq.heappop(heap)` | O(log n) |
| Peek at smallest | `heap[0]` (no removal!) | O(1) |

That O(1) peek is the superpower — the smallest item is **always** at `heap[0]`, instantly.

### Part 2: Turning a Messy List into a Heap

Already have a list? `heapify` converts it to a heap in O(n):

```python
import heapq

scores = [7, 3, 9, 1, 5, 2, 8]
heapq.heapify(scores)
print(scores)     # [1, 3, 2, 7, 5, 9, 8]
print(scores[0])  # 1 — smallest is now at position 0
```

This is faster than pushing each item one by one (O(n) vs O(n log n)).

### Part 3: Making a Max-Heap

Python's `heapq` is min-heap only. For max-heap, negate your values:

```python
import heapq

class MaxHeap:
    def __init__(self):
        self._heap = []

    def push(self, value):
        heapq.heappush(self._heap, -value)  # Store the negative

    def pop(self):
        return -heapq.heappop(self._heap)    # Negate back

    def peek(self):
        return -self._heap[0]


scores = MaxHeap()
scores.push(45)
scores.push(92)
scores.push(67)
print(scores.pop())  # 92 — largest
print(scores.pop())  # 67
```

### Part 4: Priority Queue — Items with a Score

Most real uses need items with priorities, not just numbers. The trick: push **tuples** — Python compares them element by element:

```python
import heapq

queue = []

# Push (priority, item) — sorted by priority first
heapq.heappush(queue, (1, "Fix critical bug"))
heapq.heappush(queue, (3, "Write docs"))
heapq.heappush(queue, (2, "Reply to emails"))

print(heapq.heappop(queue))  # (1, "Fix critical bug")
print(heapq.heappop(queue))  # (2, "Reply to emails")
print(heapq.heappop(queue))  # (3, "Write docs")
```

**Breaking ties:** What if two items have the same priority? Add a counter:

```python
class PriorityQueue:
    def __init__(self):
        self._heap = []
        self._counter = 0

    def push(self, item, priority):
        # Tuple: (priority, counter, item) — counter breaks ties
        heapq.heappush(self._heap, (priority, self._counter, item))
        self._counter += 1

    def pop(self):
        if not self._heap:
            return None
        return heapq.heappop(self._heap)[2]  # Return just the item


pq = PriorityQueue()
pq.push("Fix login", 1)
pq.push("Refactor module", 3)
pq.push("Security patch", 1)  # Same priority as "Fix login"

print(pq.pop())  # "Fix login" — same priority, arrived first
print(pq.pop())  # "Security patch" — same priority, arrived second
print(pq.pop())  # "Refactor module"
```

The counter ensures FIFO order when priorities are equal — first to arrive gets served first.

---

## Practice

Build an **Issue Tracker** for a dev team. Issues have a severity (1 = critical, 5 = cosmetic) and a deadline in hours.

1. Create an `Issue` class with `title`, `severity`, and `hours_due`
2. Give it an `urgency` property that calculates: `urgency = (6 - severity) * 10 + hours_due` (lower = more urgent)
3. Build an `IssueTracker` class using `heapq` with:
   - `add(issue)` — add an issue
   - `next()` — return and remove the most urgent issue
   - `peek()` — show the most urgent without removing
   - `count` — how many issues remain

Lower severity and fewer hours → more urgent → popped first.

```python
# Your code here:


# After you write it:
# tracker = IssueTracker()
# tracker.add(Issue("Login broken", severity=1, hours_due=2))
# tracker.add(Issue("Typo in footer", severity=5, hours_due=48))
# tracker.add(Issue("Payment failing", severity=1, hours_due=4))
#
# tracker.next()  # Should be "Login broken" (score = 52 vs 54)
# tracker.next()  # Should be "Payment failing"
```

---

## Solution

<details>
<summary>Click to reveal</summary>

```python
import heapq


class Issue:
    def __init__(self, title, severity, hours_due):
        self.title = title
        self.severity = severity      # 1 = critical, 5 = cosmetic
        self.hours_due = hours_due

    @property
    def urgency(self):
        """Lower = more urgent."""
        return (6 - self.severity) * 10 + self.hours_due

    def __repr__(self):
        return f"Issue('{self.title}', sev={self.severity}, due={self.hours_due}h)"


class IssueTracker:
    def __init__(self):
        self._heap = []
        self._counter = 0

    def add(self, issue):
        # Push (urgency, counter, issue) — counter breaks ties
        heapq.heappush(self._heap, (issue.urgency, self._counter, issue))
        self._counter += 1

    def next(self):
        if not self._heap:
            return None
        return heapq.heappop(self._heap)[2]

    def peek(self):
        if not self._heap:
            return None
        return self._heap[0][2]

    @property
    def count(self):
        return len(self._heap)


# --- Test ---
tracker = IssueTracker()
tracker.add(Issue("Login broken", severity=1, hours_due=2))
tracker.add(Issue("Typo in footer", severity=5, hours_due=48))
tracker.add(Issue("Payment failing", severity=1, hours_due=4))

print(f"Total: {tracker.count}")
print(f"Next: {tracker.next().title}")   # Login broken
print(f"Next: {tracker.next().title}")   # Payment failing
print(f"Next: {tracker.next().title}")   # Typo in footer
```

Login broken: urgency = (6-1)×10 + 2 = 52  
Payment failing: urgency = (6-1)×10 + 4 = 54  
Typo: urgency = (6-5)×10 + 48 = 58  
→ Login broken is the lowest → popped first. ✅

</details>

---

## Recap

- **Heap** — array where parent ≤ children, smallest always at `[0]`
- **Min-heap** — use `heapq` directly
- **Max-heap** — negate values before pushing, negate back after popping
- **Peek is O(1)** — `heap[0]` gives the smallest instantly
- **Push/pop are O(log n)** — way faster than scanning a list
- **Priority queue** — push `(priority, counter, item)` tuples
- **`heapify`** — turn any list into a heap in O(n), faster than n pushes
- **Use when** you need the smallest/largest item repeatedly from a changing collection

---

**Next: [Lesson 22: Hash Map Superpowers](22-hash-map-superpowers.md) →**
