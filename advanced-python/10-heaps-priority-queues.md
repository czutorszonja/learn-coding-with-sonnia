# Advanced Python Lesson 10: Heaps & Priority Queues ⛰️

**← Back to [Lesson 9: Trees & Binary Search Trees](09-trees-binary-search-trees.md)**

---

## What is a Heap?

**Plain English:** A heap is a special tree where the parent is always _smaller_ (min-heap) or _larger_ (max-heap) than its children. The smallest (or largest) item is always at the root — O(1) to grab it!

**Real-world analogy:** A hospital emergency room:
- Patients arrive in any order
- But the _most critical_ patient is always treated first
- New critical patients jump the queue
- Less urgent patients wait longer

This is a **priority queue** — and a heap is the data structure that makes it fast!

---

## Heap Property

### Min-Heap
```
        1          ← Smallest value at the root
       / \
      3   6
     / \ /
    5  9 8
```
**Rule:** Every parent ≤ its children. Root is the minimum.

### Max-Heap
```
       10          ← Largest value at the root
       / \
      7   9
     / \ /
    3  5 2
```
**Rule:** Every parent ≥ its children. Root is the maximum.

---

## Heap as an Array

Heaps are usually stored in an array (list), not with node objects:

```
        1           Index:  0   1   2   3   4   5
       / \          Array: [1,  3,  6,  5,  9,  8]
      3   6
     / \ /
    5  9 8
```

**Index magic:**
- Left child of `i` = `2i + 1`
- Right child of `i` = `2i + 2`
- Parent of `i` = `(i - 1) // 2`

This means no pointers needed — just math!

---

## Python's `heapq` Module

Python has a built-in min-heap:

```python
import heapq

# heapq implements a MIN-HEAP
heap = []

# Push items
heapq.heappush(heap, 5)
heapq.heappush(heap, 2)
heapq.heappush(heap, 8)
heapq.heappush(heap, 1)

print(heap)  # [1, 2, 8, 5] — min-heap order (not fully sorted!)

# Pop smallest item
smallest = heapq.heappop(heap)
print(smallest)  # 1
print(heap)      # [2, 5, 8]

# Peek at smallest without removing
print(heap[0])   # 2

# Convert a list into a heap in-place (O(n)!)
nums = [7, 3, 9, 1, 5]
heapq.heapify(nums)
print(nums)  # [1, 3, 9, 7, 5]
```

---

## Making a Max-Heap

Python only has min-heap — for max-heap, negate the values:

```python
import heapq

class MaxHeap:
    def __init__(self):
        self.heap = []

    def push(self, value):
        heapq.heappush(self.heap, -value)  # Negate!

    def pop(self):
        return -heapq.heappop(self.heap)   # Negate back!

    def peek(self):
        return -self.heap[0]

    def __len__(self):
        return len(self.heap)


mh = MaxHeap()
mh.push(5)
mh.push(2)
mh.push(8)
print(mh.pop())   # 8
print(mh.pop())   # 5
print(mh.pop())   # 2
```

---

## Priority Queue with Custom Items

Often you need items with a priority:

```python
import heapq

class Task:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    def __repr__(self):
        return f"Task('{self.name}', priority={self.priority})"


class PriorityQueue:
    def __init__(self):
        self._heap = []
        self._counter = 0  # Tiebreaker — ensures FIFO for equal priorities

    def push(self, task):
        # Heap compares tuples element by element:
        # (priority, counter, task) — counter breaks ties
        heapq.heappush(self._heap, (task.priority, self._counter, task))
        self._counter += 1

    def pop(self):
        if not self._heap:
            return None
        return heapq.heappop(self._heap)[2]  # Return just the task

    def peek(self):
        if not self._heap:
            return None
        return self._heap[0][2]

    def __len__(self):
        return len(self._heap)

    def __bool__(self):
        return len(self._heap) > 0


# --- Usage ---
pq = PriorityQueue()
pq.push(Task("Fix critical bug", 1))
pq.push(Task("Write docs", 3))
pq.push(Task("Reply to emails", 2))
pq.push(Task("Security patch", 1))  # Same priority as first task

while pq:
    print(pq.pop())

# Output (lower number = higher priority):
# Task('Fix critical bug', priority=1)     ← same priority, arrived first
# Task('Security patch', priority=1)       ← same priority, arrived second
# Task('Reply to emails', priority=2)
# Task('Write docs', priority=3)
```

---

## Common Heap Operations & Their Costs

| Operation | Time | Description |
|-----------|------|-------------|
| `heappush` | O(log n) | Insert and bubble up |
| `heappop` | O(log n) | Remove root and bubble down |
| `heap[0]` | O(1) | Peek at root (no removal) |
| `heapify` | O(n) | Build heap from list (faster than n pushes!) |
| `heapreplace` | O(log n) | Pop then push (more efficient than pop+push) |
| `nlargest(k, iter)` | O(n log k) | Find k largest items |
| `nsmallest(k, iter)` | O(n log k) | Find k smallest items |

---

## Real-World Use Cases

### 1. Task Scheduler

```python
import heapq
import time

scheduler = []
heapq.heappush(scheduler, (time.time() + 5, "Send reminder email"))
heapq.heappush(scheduler, (time.time() + 60, "Run database backup"))
heapq.heappush(scheduler, (time.time() + 10, "Check server health"))

# Process tasks as they become due
while scheduler:
    due_time, task = scheduler[0]  # Peek
    now = time.time()
    if due_time <= now:
        heapq.heappop(scheduler)
        print(f"Running: {task}")
    # (in real code you'd sleep, not busy-wait)
```

### 2. Top-K Elements

```python
import heapq

def top_k_scores(scores, k):
    """Find the k highest scores."""
    return heapq.nlargest(k, scores)

def bottom_k_scores(scores, k):
    """Find the k lowest scores."""
    return heapq.nsmallest(k, scores)

scores = [72, 95, 83, 68, 91, 78, 88, 55]
print(top_k_scores(scores, 3))    # [95, 91, 88]
print(bottom_k_scores(scores, 3)) # [55, 68, 72]
```

### 3. Running Median

```python
import heapq

class RunningMedian:
    """Track the median as numbers stream in."""

    def __init__(self):
        self.low = []   # Max-heap (negated) for lower half
        self.high = []  # Min-heap for upper half

    def add(self, num):
        # Always push to low first, then balance
        heapq.heappush(self.low, -num)

        # Move largest of low to high
        if self.low and self.high and -self.low[0] > self.high[0]:
            val = -heapq.heappop(self.low)
            heapq.heappush(self.high, val)

        # Balance sizes (differ by at most 1)
        if len(self.low) > len(self.high) + 1:
            val = -heapq.heappop(self.low)
            heapq.heappush(self.high, val)
        elif len(self.high) > len(self.low):
            val = heapq.heappop(self.high)
            heapq.heappush(self.low, -val)

    def median(self):
        if len(self.low) > len(self.high):
            return -self.low[0]
        return (-self.low[0] + self.high[0]) / 2
```

### 4. Dijkstra's Algorithm (Shortest Path)

```python
# Heaps power graph algorithms — more in the Graphs lesson!
import heapq

def dijkstra(graph, start):
    """Find shortest distances from start to all nodes."""
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    heap = [(0, start)]  # (distance, node)

    while heap:
        dist, node = heapq.heappop(heap)

        if dist > distances[node]:
            continue  # Stale entry, skip

        for neighbour, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbour]:
                distances[neighbour] = new_dist
                heapq.heappush(heap, (new_dist, neighbour))

    return distances
```

---

## Practice Exercise

**Scenario:** You're building an issue tracker for a dev team. Issues have priorities and deadlines, and the most urgent one should always be worked on next.

**Your task:**

1. Create `issue_tracker.py` with an `Issue` class:
   ```python
   class Issue:
       def __init__(self, title, severity, hours_due):
           # severity: 1 (critical) to 5 (cosmetic) — lower = more urgent
           # hours_due: how many hours until deadline
           self.title = title
           self.severity = severity
           self.hours_due = hours_due
   ```

2. Build a `IssueTracker` class that:
   - `add_issue(issue)` — add an issue to the tracker
   - `next_issue()` — return and remove the most urgent issue
   - `peek_next()` — return the most urgent issue without removing it
   - `count()` — total issues in the tracker

3. **Priority logic:** Issues are ranked by a composite score:
   - `urgency_score = (6 - severity) * 10 + hours_due`
   - Lower severity (more critical) → higher weight
   - Fewer hours until deadline → lower score
   - The issue with the **lowest** score is the most urgent

4. Add a `get_critical()` method that returns all severity-1 issues without removing them

5. Test your tracker:
   ```python
   tracker = IssueTracker()
   tracker.add_issue(Issue("Login broken", 1, 2))
   tracker.add_issue(Issue("Typo in footer", 5, 48))
   tracker.add_issue(Issue("Payment failing", 1, 4))
   tracker.add_issue(Issue("Add dark mode", 3, 72))

   print(f"Total issues: {tracker.count()}")

   next_up = tracker.next_issue()
   print(f"Working on: {next_up.title}")  # Should be "Login broken"

   critical = tracker.get_critical()
   print(f"Critical: {[i.title for i in critical]}")
   ```

**Try it yourself first!** Solution below.

---

## Solution

```python
import heapq


class Issue:
    """A dev team issue with severity and deadline."""

    def __init__(self, title, severity, hours_due):
        self.title = title
        self.severity = severity      # 1 = critical, 5 = cosmetic
        self.hours_due = hours_due    # Hours until deadline

    @property
    def urgency_score(self):
        """Composite score — lower = more urgent."""
        return (6 - self.severity) * 10 + self.hours_due

    def __repr__(self):
        return (f"Issue('{self.title}', sev={self.severity}, "
                f"due={self.hours_due}h, score={self.urgency_score})")


class IssueTracker:
    """Priority queue of issues, most urgent first."""

    def __init__(self):
        self._heap = []
        self._counter = 0  # FIFO tiebreaker

    def add_issue(self, issue):
        """Add an issue to the tracker."""
        heapq.heappush(
            self._heap,
            (issue.urgency_score, self._counter, issue)
        )
        self._counter += 1

    def next_issue(self):
        """Return and remove the most urgent issue."""
        if not self._heap:
            return None
        return heapq.heappop(self._heap)[2]

    def peek_next(self):
        """Return the most urgent issue without removing it."""
        if not self._heap:
            return None
        return self._heap[0][2]

    def count(self):
        return len(self._heap)

    def get_critical(self):
        """Return all severity-1 issues without removing them."""
        return [entry[2] for entry in self._heap if entry[2].severity == 1]

    def list_all(self):
        """Return all issues sorted by urgency (doesn't modify heap)."""
        sorted_entries = sorted(self._heap, key=lambda x: x[0])
        return [entry[2] for entry in sorted_entries]


# --- Test ---
if __name__ == "__main__":
    tracker = IssueTracker()
    tracker.add_issue(Issue("Login broken", 1, 2))
    tracker.add_issue(Issue("Typo in footer", 5, 48))
    tracker.add_issue(Issue("Payment failing", 1, 4))
    tracker.add_issue(Issue("Add dark mode", 3, 72))

    print(f"Total issues: {tracker.count()}")        # 4

    print("\nAll issues by urgency:")
    for issue in tracker.list_all():
        print(f"  {issue}")

    next_up = tracker.next_issue()
    print(f"\nWorking on: {next_up.title}")           # Login broken

    critical = tracker.get_critical()
    print(f"Critical remaining: {[i.title for i in critical]}")
    # ['Payment failing']
```

---

## Quick Recap

- **Heap** — tree where parent ≤ children (min) or parent ≥ children (max)
- **Root** always the extreme — O(1) peek, O(log n) push/pop
- **`heapq`** — Python's built-in min-heap; use negation for max-heap
- **Priority queue** — heap where items have priorities; most urgent dequeued first
- **`heapify`** — build a heap from a list in O(n) — faster than n individual pushes!
- **Tuple trick** — use `(priority, counter, item)` for custom ordering
- **Use cases** — task scheduling, top-K, running median, Dijkstra, merge K sorted lists

---

## What's Next?

Heaps give us the smallest instantly. Hash maps give us _anything_ instantly. Continue to **[Lesson 11: Hash Maps Deep Dive](11-hash-maps-deep-dive.md)** 🔑

---

**Your turn:** Build the issue tracker! Then try adding a `resolve_oldest()` method that removes the issue with the most hours_due (least urgent by deadline alone). ⛰️💛
