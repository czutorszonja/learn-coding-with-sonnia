# Data Structures Lesson 2: Queues 🚶‍♂️

**← Back to [Lesson 1: Stacks](01-stacks.md)**

---

## What is a Queue?

**Plain English:** A queue is a line. People join at the back, get served from the front. First come, first served.

**Real-world analogy:** The coffee shop queue.
- You join at the back of the line
- The barista serves whoever's been waiting longest (at the front)
- No cutting in!
- The person who arrived first gets their coffee first

---

## Queue vs Stack

```
Stack (LIFO):  push → [ _ _ _ _ ] → pop     (last in, first out)
Queue (FIFO):  push → [ _ _ _ _ ] → pop     (first in, first out)
```

Same idea — you add and remove. The difference is WHICH end you remove from.

---

## The Wrong Way (and Why)

You might think: "I'll just use a list!"

```python
# ❌ Don't do this:
queue = [1, 2, 3]
queue.pop(0)  # Removes the first element

# It works for small lists. But pop(0) has to SHIFT every remaining
# element one position left. 10,000 items = 9,999 shifts. Every pop.
```

Python has a better tool: `collections.deque` (pronounced "deck"). It's optimised for exactly this kind of work.

---

## The Right Way: `collections.deque`

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

## Real Example: A Support Ticket System

```python
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
        self._queue = Queue()
        self._completed = []

    def submit(self, customer, issue):
        ticket = Ticket(customer, issue)
        self._queue.enqueue(ticket)
        return f"Ticket {ticket.id} created for {customer}"

    def handle_next(self):
        if self._queue.is_empty():
            return "No tickets waiting"
        ticket = self._queue.dequeue()
        self._completed.append(ticket)
        return f"Handled: {ticket}"

    @property
    def waiting(self):
        return len(self._queue)

    def list_waiting(self):
        if self._queue.is_empty():
            return "No tickets waiting"
        return "\n".join(str(t) for t in self._queue._items)


support = SupportQueue()
print(support.submit("Alice", "Can't log in"))
print(support.submit("Bob", "Printer not working"))
print(support.submit("Charlie", "Feature request"))

print(f"\nWaiting: {support.waiting}")
print(support.handle_next())  # Alice first — she submitted first
print(support.handle_next())  # Bob next
print(f"Still waiting: {support.waiting}")  # 1
```

---

## Practice: A Print Queue

**Your task:** Build a print queue system where documents are printed in the order they're submitted.

1. Create a `PrintJob` class with:
   - `document` (name of the file)
   - `pages` (number of pages)
   - `owner` (who submitted it)

2. Create a `PrintQueue` class:
   - `submit(document, pages, owner)` — adds a job to the queue
   - `print_next()` — prints (removes) the next job and returns it
   - `pending()` — returns how many jobs are waiting
   - `list_queue()` — shows all waiting jobs

**Test it:**

```python
pq = PrintQueue()
pq.submit("Report.pdf", 10, "Szonja")
pq.submit("Invoice.docx", 2, "Arthur")
pq.submit("Slides.pptx", 25, "Cece")

print(f"Pending: {pq.pending()}")   # 3
print(pq.print_next())              # Szonja's Report.pdf
print(pq.print_next())              # Arthur's Invoice.docx
print(f"Pending: {pq.pending()}")   # 1
```

Create `print_queue.py` and try it!

---

## Solution

```python
from collections import deque


class PrintJob:
    def __init__(self, document, pages, owner):
        self.document = document
        self.pages = pages
        self.owner = owner

    def __str__(self):
        return f"'{self.document}' ({self.pages}pp) — {self.owner}"


class PrintQueue:
    def __init__(self):
        self._queue = deque()
        self._completed = []

    def submit(self, document, pages, owner):
        job = PrintJob(document, pages, owner)
        self._queue.append(job)
        return f"Queued: {job}"

    def print_next(self):
        if not self._queue:
            return "No jobs waiting"
        job = self._queue.popleft()
        self._completed.append(job)
        return f"Printed: {job}"

    def pending(self):
        return len(self._queue)

    def list_queue(self):
        if not self._queue:
            return "No jobs waiting"
        return "\n".join(f"  {job}" for job in self._queue)


# Test
pq = PrintQueue()
pq.submit("Report.pdf", 10, "Szonja")
pq.submit("Invoice.docx", 2, "Arthur")
pq.submit("Slides.pptx", 25, "Cece")

print(f"Pending: {pq.pending()}")
print(pq.print_next())
print(pq.print_next())
print(f"Pending: {pq.pending()}")
print(pq.print_next())
print(f"Pending: {pq.pending()}")
```

---

## What You Just Learned

- **Queue = FIFO** (First In, First Out) — fair, ordered processing
- **Use `collections.deque`**, never `list.pop(0)`
- **`append()`** adds to the back, **`popleft()`** removes from the front
- Queues model real-world lines: print jobs, support tickets, message processing

---

## What's Next?**

A deque lets you add and remove from BOTH ends. It's a stack AND a queue combined — and it has some tricks that make it perfect for sliding windows, recent-items lists, and clipboard history.

Continue to **[Lesson 3: Deque](03-deque.md)** 🔁

---

**Your turn:** Build the print queue! Then add a `cancel(document_name)` method that removes a specific job from the queue by name. 🚶‍♂️💛
