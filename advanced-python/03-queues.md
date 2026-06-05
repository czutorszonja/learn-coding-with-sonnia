# Advanced Python Lesson 3: Queues — First In, First Out 🚶‍♂️

**← Back to [Lesson 2: Stacks](02-stacks.md)**

---

## What is a Queue?

**Plain English:** A queue is a collection where items are added at the _back_ and removed from the _front_. The first item in is the first one out — FIFO (First In, First Out).

**Real-world analogy:** A queue at a coffee shop:
- People join at the back of the line
- The barista serves the person at the front
- The person who's been waiting longest gets served first
- No cutting in line!

---

## Core Operations

| Operation | What it does | Python (deque) |
|-----------|-------------|----------------|
| Enqueue | Add to the back | `queue.append(item)` |
| Dequeue | Remove from the front | `queue.popleft()` |
| Peek | Look at the front | `queue[0]` |
| Is Empty? | Check if anything's there | `len(queue) == 0` |
| Size | How many items? | `len(queue)` |

**All O(1)** with `collections.deque`!

---

## Why Not Use a List?

```python
# ❌ BAD: list.pop(0) is O(n) — shifts every element!
queue = [1, 2, 3]
first = queue.pop(0)  # Removes index 0, shifts [2, 3] left

# ✅ GOOD: deque.popleft() is O(1)
from collections import deque
queue = deque([1, 2, 3])
first = queue.popleft()  # Instant!
```

---

## Queue Using `collections.deque`

```python
from collections import deque

queue = deque()

# Enqueue (add to back)
queue.append("Alice")
queue.append("Bob")
queue.append("Charlie")

print(queue)      # deque(['Alice', 'Bob', 'Charlie'])
print(queue[0])   # 'Alice' — peek at front
print(queue[-1])  # 'Charlie' — peek at back

# Dequeue (remove from front)
served = queue.popleft()
print(served)     # 'Alice'
print(queue)      # deque(['Bob', 'Charlie'])

print(len(queue)) # 2
print(len(queue) == 0)  # False
```

---

## Building a Queue Class

```python
from collections import deque


class Queue:
    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self._items.popleft()

    def peek(self):
        if self.is_empty():
            return None
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __str__(self):
        return f"Queue({list(self._items)})"

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, item):
        return item in self._items
```

---

## Real-World Use Cases

### 1. Print Queue (Job Processing)

```python
class PrintJob:
    def __init__(self, document, pages, owner):
        self.document = document
        self.pages = pages
        self.owner = owner

    def __repr__(self):
        return f"PrintJob('{self.document}', {self.pages}pp, by {self.owner})"


class PrintQueue:
    def __init__(self):
        self._queue = Queue()
        self._completed = []

    def submit(self, document, pages, owner):
        job = PrintJob(document, pages, owner)
        self._queue.enqueue(job)
        return f"Queued: {job}"

    def process_next(self):
        if self._queue.is_empty():
            return "No jobs in queue"
        job = self._queue.dequeue()
        self._completed.append(job)
        return f"Printed: {job}"

    @property
    def pending(self):
        return len(self._queue)

    @property
    def queue_list(self):
        return list(self._queue)


pq = PrintQueue()
pq.submit("Report.pdf", 10, "Szonja")
pq.submit("Invoice.docx", 2, "Arthur")
pq.submit("Slides.pptx", 25, "Cece")

print(pq.pending)        # 3
print(pq.process_next()) # Printed: Report.pdf
print(pq.process_next()) # Printed: Invoice.docx
print(pq.pending)        # 1
```

### 2. Breadth-First Search (BFS)

```python
def bfs(graph, start):
    """Breadth-first traversal of a graph using a queue."""
    queue = Queue()
    visited = set()

    queue.enqueue(start)
    visited.add(start)

    traversal_order = []

    while not queue.is_empty():
        node = queue.dequeue()
        traversal_order.append(node)

        for neighbour in graph.get(node, []):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.enqueue(neighbour)

    return traversal_order


# Graph: A → B → D
#        ↓   ↓
#        C   E
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': [],
    'D': [],
    'E': []
}

print(bfs(graph, 'A'))  # ['A', 'B', 'C', 'D', 'E']
# Level by level: A, then B & C, then D & E
```

### 3. Message Broker / Task Queue

```python
import time


class TaskQueue:
    """A simple message broker — producers add tasks, workers process them."""

    def __init__(self):
        self._queue = Queue()
        self._processed = 0
        self._failed = []

    def publish(self, task_name, data):
        """Producer: add a task to the queue."""
        self._queue.enqueue({"task": task_name, "data": data, "timestamp": time.time()})
        return f"Published: {task_name}"

    def consume(self, worker_name):
        """Worker: take the next task and process it."""
        if self._queue.is_empty():
            return None

        task = self._queue.dequeue()
        try:
            # Simulate processing
            result = f"[{worker_name}] Completed: {task['task']}"
            self._processed += 1
            return result
        except Exception as e:
            self._failed.append(task)
            return f"[{worker_name}] Failed: {task['task']} — {e}"

    @property
    def stats(self):
        return {
            "pending": len(self._queue),
            "processed": self._processed,
            "failed": len(self._failed)
        }


broker = TaskQueue()
broker.publish("send_email", {"to": "szonja@example.com"})
broker.publish("resize_image", {"path": "/photos/cat.jpg", "width": 800})
broker.publish("backup_db", {"database": "production"})

print(broker.consume("worker-1"))  # Completed: send_email
print(broker.consume("worker-1"))  # Completed: resize_image
print(broker.stats)                # {'pending': 1, 'processed': 2, 'failed': 0}
```

### 4. Sliding Window with a Queue

```python
from collections import deque

def moving_average(stream, window_size):
    """Calculate the moving average over a sliding window."""
    window = deque()
    total = 0

    for value in stream:
        window.append(value)
        total += value

        if len(window) > window_size:
            total -= window.popleft()

        if len(window) == window_size:
            yield total / window_size


prices = [10, 12, 15, 14, 13, 16, 18, 20, 19]
for avg in moving_average(prices, 3):
    print(f"Moving average: {avg:.1f}")

# Output:
# Moving average: 12.3  ← (10+12+15)/3
# Moving average: 13.7  ← (12+15+14)/3
# Moving average: 14.0
# Moving average: 14.3
# Moving average: 15.7
# Moving average: 18.0
# Moving average: 19.0
```

---

## Queue Variations

### Circular Queue (Ring Buffer)

```python
class CircularQueue:
    """A fixed-size queue that wraps around."""

    def __init__(self, capacity):
        self._buffer = [None] * capacity
        self._capacity = capacity
        self._front = 0   # Index of the front element
        self._rear = 0    # Index where next element goes
        self._size = 0

    def enqueue(self, item):
        if self.is_full():
            raise OverflowError("Circular queue is full")
        self._buffer[self._rear] = item
        self._rear = (self._rear + 1) % self._capacity
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Circular queue is empty")
        item = self._buffer[self._front]
        self._buffer[self._front] = None  # Help garbage collection
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return item

    def is_empty(self):
        return self._size == 0

    def is_full(self):
        return self._size == self._capacity

    def __len__(self):
        return self._size

    def __str__(self):
        items = []
        for i in range(self._size):
            idx = (self._front + i) % self._capacity
            items.append(str(self._buffer[idx]))
        return f"CircularQueue([{', '.join(items)}])"


cq = CircularQueue(3)
cq.enqueue(1)
cq.enqueue(2)
cq.enqueue(3)
print(cq.is_full())  # True
print(cq.dequeue())  # 1
cq.enqueue(4)        # Wraps around!
print(cq)            # CircularQueue([2, 3, 4])
```

---

## Practice Exercise

**Scenario:** You're building a customer support ticketing system. Customers submit tickets, and agents handle them in order. Each ticket has a priority, but within the same priority, it's first-come-first-served.

**Your task:**

1. Create `support_queue.py` with these classes:

2. `Ticket` class:
   - `ticket_id` — auto-incrementing
   - `customer_name`
   - `issue` — description of the problem
   - `priority` — 1 (urgent), 2 (normal), 3 (low)
   - `created_at` — timestamp (`time.time()`)

3. `SupportQueue` class:
   - `submit(customer_name, issue, priority)` — create and enqueue a ticket
   - `next_ticket()` — return and remove the highest-priority, earliest ticket
   - `peek_next()` — look at next ticket without removing
   - `pending()` — total tickets in all queues
   - `pending_by_priority(priority)` — count for a specific priority
   - `wait_time(priority)` — estimate: (tickets ahead in same or higher priority) × 5 minutes

4. **Priority handling:** Use _three separate queues_, one per priority level. `next_ticket()` checks priority 1 first, then 2, then 3.

5. Add an `escalate(ticket_id)` method that moves a ticket to the next higher priority (3→2, 2→1)

6. Test it:
   ```python
   sq = SupportQueue()
   sq.submit("Alice", "Can't log in", 1)
   sq.submit("Bob", "Printer not working", 2)
   sq.submit("Charlie", "Feature request", 3)
   sq.submit("Dave", "Server down!", 1)
   sq.submit("Eve", "Password reset", 2)

   print(sq.next_ticket())  # Alice (first urgent)
   print(sq.next_ticket())  # Dave (second urgent)
   print(sq.next_ticket())  # Bob (first normal)
   print(sq.pending_by_priority(3))  # 1
   print(sq.wait_time(3))   # ~5 min (only Charlie's ahead in priority 3)
   ```

**Try it yourself first!** Solution below.

---

## Solution

```python
import time
from collections import deque


class Ticket:
    """A support ticket with auto-incrementing ID."""

    _next_id = 1

    def __init__(self, customer_name, issue, priority):
        self.ticket_id = Ticket._next_id
        Ticket._next_id += 1
        self.customer_name = customer_name
        self.issue = issue
        self.priority = priority
        self.created_at = time.time()

    def __repr__(self):
        prio_label = {1: "🔴 URGENT", 2: "🟡 NORMAL", 3: "🟢 LOW"}
        return (
            f"#{self.ticket_id} [{prio_label.get(self.priority, '?')}] "
            f"{self.customer_name}: {self.issue}"
        )


class SupportQueue:
    """Priority-based support ticket queue with three priority lanes."""

    PRIORITY_LEVELS = [1, 2, 3]

    def __init__(self):
        # One queue per priority level
        self._queues = {p: deque() for p in self.PRIORITY_LEVELS}
        self._ticket_map = {}  # ticket_id → (priority, position info)

    def submit(self, customer_name, issue, priority):
        """Create a ticket and add to the appropriate queue."""
        if priority not in self.PRIORITY_LEVELS:
            raise ValueError(f"Priority must be 1, 2, or 3, got {priority}")

        ticket = Ticket(customer_name, issue, priority)
        self._queues[priority].append(ticket)
        self._ticket_map[ticket.ticket_id] = ticket
        return ticket

    def next_ticket(self):
        """Return the highest-priority, earliest ticket."""
        for priority in self.PRIORITY_LEVELS:
            if self._queues[priority]:
                ticket = self._queues[priority].popleft()
                del self._ticket_map[ticket.ticket_id]
                return ticket
        return None  # All queues empty

    def peek_next(self):
        """Look at the next ticket without removing it."""
        for priority in self.PRIORITY_LEVELS:
            if self._queues[priority]:
                return self._queues[priority][0]
        return None

    def pending(self):
        """Total tickets across all priorities."""
        return sum(len(q) for q in self._queues.values())

    def pending_by_priority(self, priority):
        """Number of tickets in a specific priority."""
        return len(self._queues[priority])

    def wait_time(self, priority):
        """Estimate wait time in minutes."""
        # Tickets at same or higher priority that are ahead
        ahead = 0
        for p in self.PRIORITY_LEVELS:
            if p <= priority:
                ahead += len(self._queues[p])
        return ahead * 5  # 5 minutes per ticket

    def escalate(self, ticket_id):
        """Move a ticket to the next higher priority."""
        if ticket_id not in self._ticket_map:
            return f"Ticket #{ticket_id} not found"

        ticket = self._ticket_map[ticket_id]
        if ticket.priority == 1:
            return f"Ticket #{ticket_id} is already at highest priority"

        # Remove from current queue
        self._queues[ticket.priority].remove(ticket)

        # Upgrade priority
        ticket.priority -= 1

        # Add to higher priority queue (at the end — fair)
        self._queues[ticket.priority].append(ticket)

        return f"Escalated ticket #{ticket_id} to priority {ticket.priority}"

    def list_all(self):
        """Return all tickets sorted by priority, then by arrival."""
        all_tickets = []
        for priority in self.PRIORITY_LEVELS:
            all_tickets.extend(self._queues[priority])
        return all_tickets


# --- Test ---
if __name__ == "__main__":
    sq = SupportQueue()

    sq.submit("Alice", "Can't log in", 1)
    sq.submit("Bob", "Printer not working", 2)
    sq.submit("Charlie", "Feature request", 3)
    sq.submit("Dave", "Server down!", 1)
    sq.submit("Eve", "Password reset", 2)

    print("--- All Tickets ---")
    for t in sq.list_all():
        print(f"  {t}")

    print(f"\nPending: {sq.pending()}")
    print(f"Urgent: {sq.pending_by_priority(1)}")
    print(f"Normal: {sq.pending_by_priority(2)}")
    print(f"Low: {sq.pending_by_priority(3)}")

    print(f"\n--- Processing ---")
    print(f"Next: {sq.next_ticket()}")  # Alice (first urgent)
    print(f"Next: {sq.next_ticket()}")  # Dave (second urgent)
    print(f"Next: {sq.next_ticket()}")  # Bob (first normal)

    print(f"\nWait time for priority 3: {sq.wait_time(3)} min")

    # Escalate Charlie's feature request
    charlie_ticket = sq.list_all()[0]  # Charlie is now the first remaining
    print(f"\n{sq.escalate(charlie_ticket.ticket_id)}")
    print(f"Normal tickets: {sq.pending_by_priority(2)}")
    print(f"Low tickets: {sq.pending_by_priority(3)}")
```

---

## Quick Recap

- **Queue** — FIFO, enqueue at back, dequeue from front, all O(1) with `deque`
- **`collections.deque`** — the right tool; never use `list.pop(0)` for a queue
- **Use cases:** job processing, BFS, message brokers, sliding windows, print queues
- **Circular queue** — fixed-size ring buffer, efficient for bounded capacity
- **Priority queues** (next lesson!) — dequeue by priority, not arrival time
- **Multi-queue pattern** — separate queues per priority level, process highest first

---

## What's Next?

Queues have one entrance and one exit. A deque has _two_ — you can add and remove from both ends! Continue to **[Lesson 4: Deque](04-deque.md)** 🔁

---

**Your turn:** Build the support queue! Then add a `reassign(ticket_id, new_priority)` method that changes a ticket's priority (removes from old queue, adds to new one at the back). 🚶‍♂️💛
