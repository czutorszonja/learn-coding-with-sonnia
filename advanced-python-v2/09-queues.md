# Lesson 9: Queues 🚶‍♂️

**← Back to [Lesson 8: Stacks](08-stacks.md)**

---

## The Problem: First Come, First Served

You're building a coffee shop ordering system. Customers arrive, place orders, and get served in order. First in line = first to get coffee.

```python
# The queue at the shop:
customers = ["Alice", "Bob", "Charlie"]

# Serve the first person:
# customers.pop(0)  # This 'works'... but it's expensive
```

`list.pop(0)` works for tiny lists, but every time you remove from the front, Python has to shift EVERY remaining element one position left. 10,000 customers = 9,999 shifts per serve. That's no good for anything real.

You need a data structure that's optimised for **removing from the front** without shifting everything else.

That's a **queue**.

---

## The Idea: FIFO — First In, First Out

**Plain English:** A queue is a line. People join at the back, get served from the front. First come, first served.

**Queue vs Stack:**

| | Stack | Queue |
|---|---|---|
| Order | Last in, first out (LIFO) | First in, first out (FIFO) |
| Add to | Top | Back |
| Remove from | Top | Front |
| Real-world | Stack of plates | Coffee shop queue |

Same idea as a stack — you can only add and remove. The difference is **which end you remove from**. Stack takes from the top (most recent). Queue takes from the front (oldest).

---

## The Right Tool: `collections.deque`

Python has a dedicated tool for this: **`deque`** (pronounced "deck" — short for double-ended queue). It's optimised for fast appends and pops from both ends.

```python
from collections import deque

queue = deque()

# Add to the back (enqueue)
queue.append("Alice")
queue.append("Bob")
queue.append("Charlie")

print(queue)      # deque(['Alice', 'Bob', 'Charlie'])
print(queue[0])   # 'Alice'  ← peek at the front

# Remove from the front (dequeue)
served = queue.popleft()
print(served)     # 'Alice'
print(queue)      # deque(['Bob', 'Charlie'])

# All operations are instant — no shifting required!
```

| Operation | Method |
|-----------|--------|
| Add to back | `queue.append(item)` |
| Remove from front | `queue.popleft()` |
| Peek at front | `queue[0]` |
| Check empty | `len(queue) == 0` |

---

## Wrapping It in a Class

Just like with stacks, a class makes the intent clear:

```python
from collections import deque


class Queue:
    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        """Add an item to the back of the queue."""
        self._items.append(item)

    def dequeue(self):
        """Remove and return the item at the front."""
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue")
        return self._items.popleft()

    def peek(self):
        """Look at the front item without removing it."""
        if self.is_empty():
            return None
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __str__(self):
        return f"Queue({list(self._items)})"
```

---

## Step by Step: Building a Print Queue

### Step 1: A Simple Job

Let's start with what a print job looks like:

```python
class PrintJob:
    def __init__(self, document, pages, owner):
        self.document = document
        self.pages = pages
        self.owner = owner

    def __str__(self):
        return f"'{self.document}' ({self.pages}pp) — {self.owner}"


job = PrintJob("Report.pdf", 10, "Szonja")
print(job)  # 'Report.pdf' (10pp) — Szonja
```

Nothing tricky — just a container for document, pages, and owner.

### Step 2: The Queue Manager

Now build a `PrintQueue` that processes jobs in order using a `deque`:

```python
from collections import deque


class PrintQueue:
    def __init__(self):
        self._queue = deque()    # Jobs waiting to be printed
        self._completed = []     # Already printed

    def submit(self, document, pages, owner):
        job = PrintJob(document, pages, owner)
        self._queue.append(job)   # Add to back of queue
        return f"Queued: {job}"

    def print_next(self):
        if not self._queue:
            return "No jobs waiting"
        job = self._queue.popleft()  # Remove from front!
        self._completed.append(job)
        return f"Printed: {job}"

    def pending(self):
        return len(self._queue)

    def list_queue(self):
        if not self._queue:
            return "No jobs waiting"
        return "\n".join(f"  {job}" for job in self._queue)


pq = PrintQueue()
pq.submit("Report.pdf", 10, "Szonja")
pq.submit("Invoice.docx", 2, "Arthur")
pq.submit("Slides.pptx", 25, "Cece")

print(f"Pending: {pq.pending()}")  # 3
print(pq.print_next())             # Szonja's Report.pdf — first in!
print(pq.print_next())             # Arthur's Invoice.docx
print(f"Pending: {pq.pending()}")  # 1
```

---

## Practice: A Support Ticket System

**Your task:** Build a support ticket queue where customers are helped in order of arrival.

1. Create a `Ticket` class with:
   - `customer` — who submitted it
   - `issue` — what's wrong
   - Auto-assigned ticket ID (use a class variable `_next_id`)

2. Create a `SupportQueue` class:
   - `submit(customer, issue)` — creates a ticket and adds it to the queue
   - `handle_next()` — handles (removes) the next ticket, returns it
   - `waiting` — property, how many tickets are pending
   - `list_waiting()` — shows all pending tickets

**Test it:**

```python
support = SupportQueue()
support.submit("Alice", "Can't log in")
support.submit("Bob", "Printer not working")
support.submit("Charlie", "Feature request")

print(support.handle_next())  # Alice's ticket — she called first
print(support.handle_next())  # Bob next
print(f"Still waiting: {support.waiting}")  # 1
```

Create `support_queue.py` and try it!

---

## Solution

```python
from collections import deque


class Ticket:
    _next_id = 1

    def __init__(self, customer, issue):
        self.id = Ticket._next_id
        Ticket._next_id += 1
        self.customer = customer
        self.issue = issue

    def __str__(self):
        return f"#{self.id} | {self.customer}: {self.issue}"


class SupportQueue:
    def __init__(self):
        self._queue = deque()
        self._completed = []

    def submit(self, customer, issue):
        ticket = Ticket(customer, issue)
        self._queue.append(ticket)
        return f"Ticket #{ticket.id} created for {customer}"

    def handle_next(self):
        if not self._queue:
            return "No tickets waiting"
        ticket = self._queue.popleft()
        self._completed.append(ticket)
        return f"Handled: {ticket}"

    @property
    def waiting(self):
        return len(self._queue)

    def list_waiting(self):
        if not self._queue:
            return "No tickets waiting"
        return "\n".join(str(t) for t in self._queue)


# Test
support = SupportQueue()
support.submit("Alice", "Can't log in")
support.submit("Bob", "Printer not working")
support.submit("Charlie", "Feature request")

print(f"\nWaiting: {support.waiting}")
print(support.handle_next())
print(support.handle_next())
print(f"Still waiting: {support.waiting}")
```

---

## What You Just Learned

- **Queue = FIFO** (First In, First Out) — fair, ordered processing
- **Use `collections.deque`**, never `list.pop(0)`
- **`append()`** adds to the back, **`popleft()`** removes from the front
- Queues model real-world lines: print jobs, support tickets, message processing

---

## What's Next?

A deque lets you add and remove from BOTH ends. It's a stack AND a queue combined — and it has some tricks that make it perfect for clipboard history, sliding windows, and "last N items" tracking.

Continue to **[Lesson 10: Deque](10-deque.md)** 🔁

---

**Your turn:** Build the support queue! Then add a `cancel(ticket_id)` method that removes a specific ticket by ID from the waiting list. 🚶‍♂️💛
