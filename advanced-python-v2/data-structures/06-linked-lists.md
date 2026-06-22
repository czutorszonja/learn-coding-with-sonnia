# Data Structures Lesson 6: Linked Lists ⛓️

**← Back to [Lesson 5: Functions as First-Class Citizens](05-functions-first-class.md)**

---

## The Problem: Lists That Hate Insertion

Python lists are amazing for random access: `my_list[500]` is instant. But they're terrible at inserting or deleting in the middle:

```python
items = [10, 20, 30, 40, 50]

# This looks simple...
items.insert(2, 25)  # Insert 25 at position 2
```

Behind the scenes, Python has to **shift every element after position 2** to make room. For a list of 1,000 items, that's ~998 elements moved. For 1,000,000, that's nearly a million elements just to insert ONE item.

The same thing happens on deletion — elements shift left to fill the gap.

What if we could insert and delete without moving anything?

---

## The Idea: Data That Points to the Next One

A **linked list** solves this by not storing items in contiguous memory slots. Instead, each item (node) holds:

1. Its **value**
2. A **pointer** to the next node

```
[10 | →]  →  [20 | →]  →  [30 | →]  →  [40 | None]
```

Each node lives wherever it wants in memory. To get from one to the next, you follow the pointer. The last node points to `None` — the end of the list.

**Insertion is just pointer changes:**

```
Before:  [10 | →]  →  [20 | →]  →  [30 | →]  →  [40 | None]

Insert 25 between 20 and 30:
Step 1: Point 25 to 30
         [25 | →]  ───────┐
                          ↓
Before:  [10 | →]  →  [20 | →]  →  [30 | →]  →  [40 | None]

Step 2: Point 20 to 25
         [25 | →]  ───────┐
                          ↓
Before:  [10 | →]  →  [20 | ]     [30 | →]  →  [40 | None]
                            │              ↑
                            └──────────────┘

Result:  [10 | →]  →  [20 | →]  →  [25 | →]  →  [30 | →]  →  [40 | None]
```

No shifting. No copying. Just two pointer changes.

---

## Building a Linked List Step by Step

### Step 1: The Node

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
```

That's it. A node has a value and a pointer to the next node. `None` means "end of list."

### Step 2: Append (Add to the End)

```python
class LinkedList:
    def __init__(self):
        self.head = None  # Start empty

    def append(self, value):
        """Add a value to the end."""
        new_node = Node(value)
        if self.head is None:
            # List is empty — this node IS the list
            self.head = new_node
            return
        # Walk to the end
        current = self.head
        while current.next:
            current = current.next
        # current is now the last node
        current.next = new_node

    def display(self):
        """Print the list in a readable form."""
        values = []
        current = self.head
        while current:
            values.append(str(current.value))
            current = current.next
        print(" → ".join(values) + " → None")
```

Let's see it in action:

```python
ll = LinkedList()
ll.append(10)
ll.append(20)
ll.append(30)
ll.display()
# 10 → 20 → 30 → None
```

### Step 3: Insert in the Middle

```python
def insert_after(self, target, value):
    """Insert a new node after the first occurrence of target."""
    current = self.head
    while current:
        if current.value == target:
            new_node = Node(value)
            new_node.next = current.next
            current.next = new_node
            return True
        current = current.next
    return False  # target not found
```

Notice: no element shifting. Just two pointer reassignments. This is O(1) once you're at the right position — compared to O(n) for a Python list.

### The Tradeoff

Linked lists are great at **insertion and deletion in the middle**, but they're slow at:

- **Random access** (`ll[500]`) — you have to walk 500 nodes from the head. O(n) vs O(1) for Python lists.
- **Memory** — each node stores extra data (the pointer). ~8-16 bytes overhead per element.
- **Cache locality** — nodes are scattered in memory, so the CPU can't prefetch them.

So linked lists are niche. But they're a **foundational concept** — trees, graphs, and many advanced data structures build on this exact idea.

### The Recursive Nature

Linked lists are naturally recursive:

```
A linked list is either:
  • Empty (None), or
  • A node whose .next points to a linked list
```

```python
def recursive_display(node):
    """Print a linked list recursively."""
    if node is None:
        print("None")
        return
    print(node.value, end=" → ")
    recursive_display(node.next)
```

---

## Practice: Find the Middle

**Your task:** Add a `find_middle()` method to `LinkedList` that returns the middle element. If the list has an even number of elements, return the second middle (the one closer to the end).

Don't use `len()` — linked lists don't track length by default.

**Two approaches to try:**
1. **Count then walk:** Count the nodes first, then walk half that many steps
2. **Tortoise and hare:** One pointer moves one step, another moves two. When the hare reaches the end, the tortoise is at the middle.

```python
ll = LinkedList()
for v in [1, 2, 3, 4, 5]:
    ll.append(v)

print(ll.find_middle())  # 3

ll.append(6)
print(ll.find_middle())  # 4
```

Save as `linkedlist_middle.py` and try it!

---

## Solution

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def find_middle_count(self):
        """Approach 1: count then walk halfway."""
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next

        middle = count // 2
        current = self.head
        for _ in range(middle):
            current = current.next
        return current.value

    def find_middle_fast_slow(self):
        """Approach 2: tortoise and hare (more efficient)."""
        if self.head is None:
            return None
        slow = self.head
        fast = self.head
        while fast and fast.next:
            slow = slow.next       # Move one step
            fast = fast.next.next  # Move two steps
        return slow.value

    def display(self):
        values = []
        current = self.head
        while current:
            values.append(str(current.value))
            current = current.next
        print(" → ".join(values) + " → None")


ll = LinkedList()
for v in [1, 2, 3, 4, 5]:
    ll.append(v)
ll.display()
print(f"Middle (count): {ll.find_middle_count()}")       # 3
print(f"Middle (fast/slow): {ll.find_middle_fast_slow()}")  # 3

ll.append(6)
ll.display()
print(f"Middle (fast/slow): {ll.find_middle_fast_slow()}")  # 4
```

---

## What You Just Learned

- **Linked list** = nodes connected by pointers, not contiguous memory
- **Insertion/deletion** = O(1) after finding position (vs O(n) shifting for Python lists)
- **Random access** = O(n) (vs O(1) for Python lists) — the tradeoff
- The **slow-fast pointer technique** is a classic linked list pattern
- Linked lists are **foundational** — they're the basis for trees and graphs

---

## What's Next?

Now that you know the node-pointer pattern, you're ready for the most important self-referential structure in computer science: **trees** 🌳

Next up: **[Lesson 7: Trees](07-trees.md)** — the data structure behind file systems, HTML, and AI decision-making.

---

**Your turn:** Build the linked list and implement `find_middle()` both ways. Then try implementing `reverse()` — can you flip the pointers without creating a new list? 💛
