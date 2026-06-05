# Advanced Python Lesson 1: Linked Lists — Chains of Data 🔗

---

## What is a Linked List?

**Plain English:** A linked list is a chain of _nodes_, where each node holds some data and a _pointer_ to the next node. Unlike a list (array), the nodes aren't stored next to each other in memory — they're linked together like a treasure hunt.

**Real-world analogy:** Think of a conga line at a party:
- Each person (node) has their hands on the shoulders of the person in front
- You can only go forward through the line — you can't jump to person #7 directly
- To add someone, you break the chain at the right spot and link them in
- To remove someone, you reconnect the people on either side

---

## Why Linked Lists?

| Operation | Python List | Linked List |
|-----------|------------|-------------|
| Access by index | O(1) — instant | O(n) — must walk the chain |
| Insert at front | O(n) — shift everything | O(1) — just change the head |
| Insert in middle | O(n) | O(1) once you're at the spot |
| Delete at front | O(n) | O(1) |

Linked lists shine when you're constantly adding and removing from the _front_ or _middle_ — no shifting required!

---

## The Node — Building Block

```python
class Node:
    def __init__(self, data):
        self.data = data    # The value this node holds
        self.next = None    # Pointer to the next node (None = end of chain)
```

---

## Building a Singly Linked List

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None    # Start of the chain
        self._size = 0      # Track how many nodes we have

    def __len__(self):
        return self._size

    def append(self, data):
        """Add a new node to the end of the list."""
        new_node = Node(data)
        self._size += 1

        if self.head is None:
            # Empty list — new node becomes the head
            self.head = new_node
            return

        # Walk to the end of the chain
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    def prepend(self, data):
        """Add a new node to the front — O(1)!"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def insert_after(self, target_data, data):
        """Insert a new node after the first node containing target_data."""
        current = self.head
        while current is not None:
            if current.data == target_data:
                new_node = Node(data)
                new_node.next = current.next
                current.next = new_node
                self._size += 1
                return True
            current = current.next
        return False  # target not found

    def delete(self, data):
        """Delete the first node with the given data."""
        if self.head is None:
            return False

        # Special case: deleting the head
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return True

        # Walk the chain, looking one step ahead
        current = self.head
        while current.next is not None:
            if current.next.data == data:
                current.next = current.next.next  # Skip over it
                self._size -= 1
                return True
            current = current.next
        return False

    def find(self, data):
        """Search for a node by value. Returns True if found."""
        current = self.head
        while current is not None:
            if current.data == data:
                return True
            current = current.next
        return False

    def __str__(self):
        """Pretty-print the list."""
        if self.head is None:
            return "[]"

        nodes = []
        current = self.head
        while current is not None:
            nodes.append(str(current.data))
            current = current.next
        return " → ".join(nodes)

    def to_list(self):
        """Convert linked list to a normal Python list."""
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result
```

---

## Doubly Linked List

A **doubly** linked list has pointers going _both_ directions:

```python
class DoublyNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None    # Points backward too!


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None    # Direct access to the end!
        self._size = 0

    def append(self, data):
        new_node = DoublyNode(data)
        self._size += 1

        if self.head is None:
            self.head = self.tail = new_node
            return

        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node

    def prepend(self, data):
        new_node = DoublyNode(data)
        self._size += 1

        if self.head is None:
            self.head = self.tail = new_node
            return

        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node

    def delete(self, data):
        current = self.head
        while current is not None:
            if current.data == data:
                # Re-link the neighbours
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next  # Was the head

                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev  # Was the tail

                self._size -= 1
                return True
            current = current.next
        return False

    def __str__(self):
        if self.head is None:
            return "[]"
        nodes = []
        current = self.head
        while current is not None:
            nodes.append(str(current.data))
            current = current.next
        return " ↔ ".join(nodes)
```

---

## Linked List vs Deque

Python's `collections.deque` is actually implemented as a doubly-linked list of blocks! Now you know what's under the hood.

```python
from collections import deque

# These operations are all O(1) because deque uses linked blocks:
dq = deque()
dq.append(1)       # Add right
dq.appendleft(2)   # Add left — like prepend
dq.pop()           # Remove right
dq.popleft()       # Remove left
```

---

## Common Patterns & Tricks

### The "Two Pointer" (Fast & Slow) Pattern

```python
def find_middle(head):
    """Find the middle node using fast/slow pointers."""
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next        # Moves 1 step
        fast = fast.next.next   # Moves 2 steps
    # When fast reaches the end, slow is at the middle
    return slow
```

### Detecting Cycles (Floyd's Algorithm)

```python
def has_cycle(head):
    """Check if a linked list has a cycle (loop)."""
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True  # They met — there's a cycle!
    return False
```

### Reversing a Linked List

```python
def reverse(head):
    """Reverse a linked list in place. Returns new head."""
    prev = None
    current = head
    while current is not None:
        next_node = current.next  # Save the next node
        current.next = prev       # Reverse the pointer
        prev = current            # Move prev forward
        current = next_node       # Move current forward
    return prev  # New head (old tail)
```

---

## Practice Exercise

**Scenario:** You're building a music playlist where songs can be added, removed, and shuffled through.

**Your task:**

1. Create a file called `playlist.py` with a `Song` node class and a `Playlist` linked list class

2. Your `Playlist` must support:
   - `add_song(title)` — add a song to the end
   - `add_next(title)` — add a song to the front (play next!)
   - `remove_song(title)` — remove the first occurrence of a song
   - `play_next()` — remove and return the first song (like a queue)
   - `find_song(title)` — return True if the song is in the playlist
   - `list_songs()` — return a list of all song titles in order
   - `__len__` — return how many songs are in the playlist

3. Write a `shuffle_playlist(playlist)` function that:
   - Converts the linked list to a Python list
   - Shuffles it (`import random; random.shuffle()`)
   - Builds a NEW linked list from the shuffled order
   - Returns the new shuffled playlist

4. Test your code:
   ```python
   p = Playlist()
   p.add_song("Bohemian Rhapsody")
   p.add_song("Stairway to Heaven")
   p.add_next("Hotel California")  # Goes to front
   p.add_song("Imagine")
   print(len(p))         # Should be 4
   print(p.list_songs()) # ['Hotel California', 'Bohemian Rhapsody', 'Stairway to Heaven', 'Imagine']
   p.remove_song("Stairway to Heaven")
   print(p.find_song("Stairway to Heaven"))  # False
   next_up = p.play_next()
   print(next_up)        # 'Hotel California'
   print(len(p))         # 2
   ```

**Try it yourself first!** Solution below.

---

## Solution

```python
import random


class Song:
    """A node in the playlist — one song."""

    def __init__(self, title):
        self.title = title
        self.next = None


class Playlist:
    """A singly linked list of songs."""

    def __init__(self):
        self.head = None
        self._size = 0

    def __len__(self):
        return self._size

    def add_song(self, title):
        """Add a song to the end of the playlist."""
        new_song = Song(title)
        self._size += 1

        if self.head is None:
            self.head = new_song
            return

        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_song

    def add_next(self, title):
        """Add a song to the front — it plays next!"""
        new_song = Song(title)
        new_song.next = self.head
        self.head = new_song
        self._size += 1

    def remove_song(self, title):
        """Remove the first song with the given title."""
        if self.head is None:
            return False

        if self.head.title == title:
            self.head = self.head.next
            self._size -= 1
            return True

        current = self.head
        while current.next is not None:
            if current.next.title == title:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False

    def play_next(self):
        """Remove and return the first song's title (FIFO)."""
        if self.head is None:
            return None

        title = self.head.title
        self.head = self.head.next
        self._size -= 1
        return title

    def find_song(self, title):
        """Check if a song exists in the playlist."""
        current = self.head
        while current is not None:
            if current.title == title:
                return True
            current = current.next
        return False

    def list_songs(self):
        """Return all song titles as a Python list."""
        titles = []
        current = self.head
        while current is not None:
            titles.append(current.title)
            current = current.next
        return titles


def shuffle_playlist(playlist):
    """Create a new shuffled playlist from an existing one."""
    songs = playlist.list_songs()
    random.shuffle(songs)

    new_playlist = Playlist()
    for title in songs:
        new_playlist.add_song(title)
    return new_playlist


# --- Quick test ---
if __name__ == "__main__":
    p = Playlist()
    p.add_song("Bohemian Rhapsody")
    p.add_song("Stairway to Heaven")
    p.add_next("Hotel California")
    p.add_song("Imagine")

    print(f"Length: {len(p)}")                  # 4
    print(f"Songs: {p.list_songs()}")
    # ['Hotel California', 'Bohemian Rhapsody', 'Stairway to Heaven', 'Imagine']

    p.remove_song("Stairway to Heaven")
    print(f"Find 'Stairway': {p.find_song('Stairway to Heaven')}")  # False

    next_up = p.play_next()
    print(f"Now playing: {next_up}")             # Hotel California
    print(f"Remaining: {len(p)}")                # 2

    shuffled = shuffle_playlist(p)
    print(f"Shuffled: {shuffled.list_songs()}")
```

---

## Quick Recap

- **Linked List** — chain of nodes, each pointing to the next
- **Node** — holds data + a pointer; the building block
- **Singly** linked — one direction only; **doubly** linked — both directions
- **Prepend/delete at front** — O(1), no shifting needed
- **Fast & slow pointers** — find middle, detect cycles
- **Reversal** — classic interview pattern: prev/current/next dance

---

## What's Next?

Now that you can build chains of nodes, let's master the art of functions that call themselves! Continue to **[Lesson 2: Recursion Deep Dive](02-recursion-deep-dive.md)** 🔄

---

**Your turn:** Build the playlist! Then try adding a `skip_forward(n)` method that skips ahead `n` songs and returns the one you land on. 🔗💛
