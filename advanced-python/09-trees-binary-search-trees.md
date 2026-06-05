# Advanced Python Lesson 9: Trees & Binary Search Trees 🌳

**← Back to [Lesson 8: Recursion Deep Dive](08-recursion-deep-dive.md)**

---

## What is a Tree?

**Plain English:** A tree is a hierarchical data structure made of nodes. Unlike a linked list (one path), a tree _branches out_ — each node can have multiple children. It's the recursive data structure: every subtree is itself a tree.

**Real-world analogy:** Think of a family tree:
- You have parents, grandparents, great-grandparents (ancestors)
- You might have siblings, children, grandchildren (descendants)
- Everyone has exactly one "parent" above them… except the root ancestor
- Each branch of the family is a smaller family tree

---

## Tree Vocabulary

```
         [A]              ← root (top node, no parent)
        /   \
      [B]   [C]           ← children of A
     /   \     \
   [D]   [E]   [F]        ← leaf nodes (no children)
```

- **Root** — the top node (A)
- **Parent** — a node with children (A is parent of B, C)
- **Child** — a node below another (B is child of A)
- **Leaf** — a node with no children (D, E, F)
- **Depth** — how far from the root (A=0, B=1, D=2)
- **Height** — longest path from root to any leaf (this tree: 2)
- **Subtree** — any node and all its descendants (B-D-E is a subtree)

---

## Binary Tree

A **binary** tree means each node has _at most 2_ children (left and right):

```python
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None    # Left child
        self.right = None   # Right child
```

---

## Tree Traversal — Three Ways to Walk the Tree

Given this tree:
```
        1
       / \
      2   3
     / \
    4   5
```

### 1. Pre-order: Root → Left → Right

```python
def preorder(node):
    if node is None:
        return
    print(node.value, end=" ")   # Visit root FIRST
    preorder(node.left)          # Then left subtree
    preorder(node.right)         # Then right subtree

# Output: 1 2 4 5 3
```

**Use case:** Saving/exporting a tree (root-first serialisation).

### 2. In-order: Left → Root → Right

```python
def inorder(node):
    if node is None:
        return
    inorder(node.left)           # Left subtree FIRST
    print(node.value, end=" ")   # Then root
    inorder(node.right)          # Then right subtree

# Output: 4 2 5 1 3
```

**Use case:** For a BST, this visits values in **sorted order**!

### 3. Post-order: Left → Right → Root

```python
def postorder(node):
    if node is None:
        return
    postorder(node.left)         # Left subtree
    postorder(node.right)        # Right subtree
    print(node.value, end=" ")   # Root LAST

# Output: 4 5 2 3 1
```

**Use case:** Deleting a tree (delete children before parent).

---

## Binary Search Tree (BST)

A BST has a special rule:

> **Left child < Parent < Right child**

```
        8
       / \
      3   10
     / \    \
    1   6    14
       / \   /
      4   7 13
```

Every node's left subtree contains _only smaller_ values, and its right subtree contains _only larger_ values. This rule makes **searching incredibly fast** — O(log n) for balanced trees!

---

## BST Operations

### Search

```python
def search(node, target):
    """Search for target in BST. Returns True if found."""
    if node is None:
        return False

    if node.value == target:
        return True
    elif target < node.value:
        return search(node.left, target)   # Go left
    else:
        return search(node.right, target)  # Go right
```

At each step, you **eliminate half** the remaining tree!

### Insert

```python
def insert(node, value):
    """Insert value into BST. Returns the (possibly new) root."""
    if node is None:
        return TreeNode(value)

    if value < node.value:
        node.left = insert(node.left, value)
    elif value > node.value:
        node.right = insert(node.right, value)
    # If equal, value already exists — do nothing (or handle duplicates)

    return node
```

### Find Minimum / Maximum

```python
def find_min(node):
    """Smallest value — keep going left!"""
    if node is None:
        return None
    while node.left is not None:
        node = node.left
    return node.value

def find_max(node):
    """Largest value — keep going right!"""
    if node is None:
        return None
    while node.right is not None:
        node = node.right
    return node.value
```

---

## Level-Order Traversal (BFS)

Walk the tree level by level, left to right:

```python
from collections import deque

def level_order(root):
    """Visit nodes level by level (BFS)."""
    if root is None:
        return []

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        result.append(node.value)

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return result

# For the BST above: [8, 3, 10, 1, 6, 14, 4, 7, 13]
```

This uses a **queue** — just like the ones you already know!

---

## Tree Height & Balance

```python
def height(node):
    """Return the height of the tree (-1 for empty tree)."""
    if node is None:
        return -1
    return 1 + max(height(node.left), height(node.right))

def is_balanced(node):
    """Check if tree is balanced (heights differ by at most 1)."""
    if node is None:
        return True

    left_height = height(node.left)
    right_height = height(node.right)

    if abs(left_height - right_height) > 1:
        return False

    return is_balanced(node.left) and is_balanced(node.right)
```

**Why balance matters:** A degenerate BST (all nodes in one line) degrades to O(n) — no better than a linked list!

---

## Practice Exercise

**Scenario:** You're building a contact book that stays sorted — insert a contact and find them instantly.

**Your task:**

1. Create `bst_contacts.py` with a `Contact` class:
   ```python
   class Contact:
       def __init__(self, name, phone):
           self.name = name
           self.phone = phone
   ```

2. Build a `ContactBook` BST that:
   - `add(name, phone)` — insert a contact (ordered by name)
   - `find(name)` — return the Contact or None
   - `list_alphabetical()` — return all contacts in alphabetical order (hint: use in-order!)
   - `find_range(start_name, end_name)` — return all contacts between two names (inclusive)
   - `count()` — return total number of contacts

3. Bonus: Add a `delete(name)` method. This is the hardest BST operation — three cases:
   - Leaf node (no children) — just remove it
   - One child — replace node with its child
   - Two children — find the in-order successor (smallest in right subtree), swap values, delete the successor

4. Test your code:
   ```python
   book = ContactBook()
   book.add("Szonja", "555-0101")
   book.add("Arthur", "555-0102")
   book.add("Cece", "555-0103")
   book.add("David", "555-0104")
   book.add("Bea", "555-0105")

   print(book.list_alphabetical())
   # [('Arthur', '555-0102'), ('Bea', '555-0105'), ('Cece', '555-0103'),
   #  ('David', '555-0104'), ('Szonja', '555-0101')]

   print(book.find_range("Arthur", "Cece"))
   # [('Arthur', '555-0102'), ('Bea', '555-0105'), ('Cece', '555-0103')]

   print(book.count())  # 5
   ```

**Try it yourself first!** Solution below.

---

## Solution

```python
class Contact:
    """A contact with name and phone number."""

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def __repr__(self):
        return f"Contact('{self.name}', '{self.phone}')"


class BSTNode:
    """A node in the contact book BST."""

    def __init__(self, contact):
        self.contact = contact
        self.left = None
        self.right = None


class ContactBook:
    """A binary search tree of contacts, ordered by name."""

    def __init__(self):
        self.root = None
        self._count = 0

    def add(self, name, phone):
        """Insert a contact into the BST."""
        self.root = self._insert(self.root, Contact(name, phone))
        self._count += 1

    def _insert(self, node, contact):
        if node is None:
            return BSTNode(contact)

        if contact.name < node.contact.name:
            node.left = self._insert(node.left, contact)
        elif contact.name > node.contact.name:
            node.right = self._insert(node.right, contact)
        # Duplicate name — could update phone here

        return node

    def find(self, name):
        """Find a contact by name. Returns Contact or None."""
        return self._search(self.root, name)

    def _search(self, node, name):
        if node is None:
            return None

        if name == node.contact.name:
            return node.contact
        elif name < node.contact.name:
            return self._search(node.left, name)
        else:
            return self._search(node.right, name)

    def list_alphabetical(self):
        """Return all contacts sorted by name (in-order traversal)."""
        result = []
        self._inorder(self.root, result)
        return [(c.name, c.phone) for c in result]

    def _inorder(self, node, result):
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.contact)
        self._inorder(node.right, result)

    def find_range(self, start_name, end_name):
        """Return contacts with names between start and end (inclusive)."""
        result = []
        self._range_search(self.root, start_name, end_name, result)
        return [(c.name, c.phone) for c in result]

    def _range_search(self, node, low, high, result):
        if node is None:
            return

        name = node.contact.name

        # Only go left if there might be matches there
        if name > low:
            self._range_search(node.left, low, high, result)

        # Add current if in range
        if low <= name <= high:
            result.append(node.contact)

        # Only go right if there might be matches there
        if name < high:
            self._range_search(node.right, low, high, result)

    def count(self):
        return self._count

    def delete(self, name):
        """Delete a contact by name. Returns True if found."""
        found = [False]
        self.root = self._delete(self.root, name, found)
        if found[0]:
            self._count -= 1
        return found[0]

    def _delete(self, node, name, found):
        if node is None:
            return None

        if name < node.contact.name:
            node.left = self._delete(node.left, name, found)
        elif name > node.contact.name:
            node.right = self._delete(node.right, name, found)
        else:
            found[0] = True
            # Case 1 & 2: 0 or 1 child
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # Case 3: 2 children — find successor
            successor = self._find_min_node(node.right)
            node.contact = successor.contact
            node.right = self._delete(node.right, successor.contact.name, [True])

        return node

    def _find_min_node(self, node):
        while node.left is not None:
            node = node.left
        return node


# --- Test ---
if __name__ == "__main__":
    book = ContactBook()
    book.add("Szonja", "555-0101")
    book.add("Arthur", "555-0102")
    book.add("Cece", "555-0103")
    book.add("David", "555-0104")
    book.add("Bea", "555-0105")

    print("Alphabetical:", book.list_alphabetical())
    print("Range Arthur-Cece:", book.find_range("Arthur", "Cece"))
    print("Count:", book.count())

    # Test find
    contact = book.find("Arthur")
    print(f"Found: {contact}")

    # Test delete
    book.delete("Cece")
    print("After deleting Cece:", book.list_alphabetical())
    print("Count:", book.count())
```

---

## Quick Recap

- **Tree** — hierarchical, recursive data structure; every subtree is a tree
- **Binary tree** — each node has ≤ 2 children (left, right)
- **BST** — left < parent < right; enables O(log n) search
- **Traversals:** pre-order (root first), in-order (sorted!), post-order (children first), level-order (BFS)
- **Balance** matters — unbalanced BST degrades to linked-list performance
- **Deletion** has 3 cases — leaf, one child, two children (use successor)

---

## What's Next?

Trees are great for ordered data — but what if you need the _smallest_ or _largest_ item instantly? That's where heaps come in. Continue to **[Lesson 10: Heaps & Priority Queues](10-heaps-priority-queues.md)** ⛰️

---

**Your turn:** Build the contact book! Then try adding a `height()` method that tells you how deep your BST is. 🌳💛
