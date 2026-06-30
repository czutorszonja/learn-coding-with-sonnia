# Lesson 19: Trees

**← Back to [Lesson 18: Linked Lists](18-linked-lists.md)**

---

## The Problem: Data That Branches

Linked lists are great for linear sequences. But what about data that naturally branches?

- A file system (folders inside folders inside folders)
- An HTML document (tags nested in tags)
- A game AI's possible moves (each move leads to more possible moves)
- A family tree (parents, children, siblings)
- A decision tree ("if yes go here, if no go there")

These aren't chains — they're **trees**. Each node can have multiple children instead of just one `next`.

---

## The Idea: Nodes With Multiple Children

A **tree** is like a linked list, but each node can point to many other nodes.

```
        root
         │
     ┌───┼───┬────┐
     │   │   │    │
   child child child child
     │
   ┌─┼──┐
   │ │  │
  ... ...
```

**Tree vocabulary:**

- **Root** — the topmost node (where the tree starts)
- **Node** — holds a value, may have children
- **Child** — a node directly below another node
- **Parent** — a node directly above another node
- **Leaf** — a node with no children
- **Depth** — distance from the root
- **Height** — maximum depth of the tree

---

## Binary Trees: The Most Common Kind

A **binary tree** is a tree where each node has at most **two** children — left and right.

```
        "root"
       /      \
  "left"     "right"
   /   \         \
"LL"  "LR"      "RR"
```

Why two? Binary trees are the sweet spot: simple enough to reason about, powerful enough to build search engines, compilers, and AI.

```python
class BinaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
```

It's a linked list node with two `next` pointers!

---

## Binary Search Trees (BST)

A **Binary Search Tree** follows one rule:

> For any node: all values in the left subtree are SMALLER, all values in the right subtree are LARGER.

```
        10
       /  \
      5    15
     / \     \
    3   7     20
```

This rule makes searching incredibly fast. To find 7:

1. Start at 10. 7 < 10 → go left ✅
2. At 5. 7 > 5 → go right ✅
3. At 7. Found it! 🎉

Each comparison eliminates half the remaining tree. That's **O(log n)** — logarithms are about dividing, not linear scanning.

---

## Building a BST Step by Step

### Insert

```python
class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        """Insert a value in the correct position."""
        if self.root is None:
            self.root = BinaryTreeNode(value)
            return
        self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = BinaryTreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = BinaryTreeNode(value)
            else:
                self._insert_recursive(node.right, value)
        # If equal — typically skip (no duplicates)

    def search(self, value):
        """Return True if the value exists in the tree."""
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        if node is None:
            return False
        if node.value == value:
            return True
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)
```

```python
bst = BST()
for v in [10, 5, 15, 3, 7, 20]:
    bst.insert(v)

print(bst.search(7))   # True
print(bst.search(12))  # False
```

---

## Delete: The Tricky Operation

Insert is easy — you find an empty spot and drop the node there. Delete is harder because removing a node might leave a gap in the tree. There are **three cases**:

| Case | What to do |
|------|-----------|
| **1. Leaf** (no children) | Just remove it |
| **2. One child** | Replace the node with its child |
| **3. Two children** | Find the inorder successor, copy its value, delete the successor |

### Case 1: Leaf Node

Simply set the parent's left or right pointer to `None`.

```
      10                   10
     /  \                 /  \
    5    15      →       5    15
         /
        12                   (12 is gone)
```

```python
def _delete(self, node, value):
    if node is None:
        return None

    # Step 1: Find the node
    if value < node.value:
        node.left = self._delete(node.left, value)
    elif value > node.value:
        node.right = self._delete(node.right, value)
    else:
        # Found it! Now handle the three cases

        # Case 1: No children (leaf)
        if node.left is None and node.right is None:
            return None
        # ... cases 2 & 3 coming ...

    return node
```

Look at that `return None` — the parent receives `None` and sets its pointer to it. The leaf is gone.

### Case 2: One Child

Replace the node with its only child.

```
      10                   10
     /  \                 /  \
    5    15      →       5    12
         /                      \
        12                       13
          \
           13
```

```python
# Case 2a: Only right child
if node.left is None:
    return node.right

# Case 2b: Only left child
if node.right is None:
    return node.left
```

The parent receives the child node and connects to it directly. Simple.

### Case 3: Two Children

This is the interesting one. You can't just remove the node — you'd have two orphans.

The trick: **find the inorder successor** — the smallest value in the right subtree. It's guaranteed to be larger than everything in the left subtree *and* smaller than everything else in the right subtree. Copy its value into the node, then delete the successor (it's always a leaf or has one child, so cases 1 or 2 handle it).

```
Delete 10:

      10                       12
     /  \                     /  \
    5    15      →          5    15
         /  \                    /  \
        12   20                 13   20
          \
           13

  10 is gone. 12 (the inorder successor) took its place.
  13 moved up as 12's old child.
```

```python
# Case 3: Two children
successor = self._min_value(node.right)   # smallest in right subtree
node.value = successor.value              # copy the value up
node.right = self._delete(node.right, successor.value)  # delete the original successor

def _min_value(self, node):
    """Find the smallest value in a subtree — follow left forever."""
    current = node
    while current.left is not None:
        current = current.left
    return current
```

### Putting It All Together

```python
class BST:
    def __init__(self):
        self.root = None

    # ... insert, search (same as before) ...

    def delete(self, value):
        """Delete a value from the BST. Does nothing if not found."""
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        if node is None:
            return None

        # Search phase
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            # Found the node — apply the correct case

            # Case 1: Leaf
            if node.left is None and node.right is None:
                return None

            # Case 2a: Only right child
            if node.left is None:
                return node.right

            # Case 2b: Only left child
            if node.right is None:
                return node.left

            # Case 3: Two children
            successor = self._min_value(node.right)
            node.value = successor.value
            node.right = self._delete(node.right, successor.value)

        return node

    def _min_value(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
```

```python
bst = BST()
for v in [10, 5, 15, 3, 7, 12, 20]:
    bst.insert(v)

bst.delete(3)   # Case 1: leaf — easy
bst.delete(20)  # Case 1: leaf — easy
bst.delete(15)  # Case 3: two children — 20 was already deleted, now 15 has only 12...
                # Wait, 15 now has one child (12) so it's actually Case 2!

# Let's be more explicit:
bst2 = BST()
for v in [50, 30, 70, 20, 40, 60, 80]:
    bst2.insert(v)

bst2.delete(20)  # Case 1: leaf
bst2.delete(30)  # Case 3: two children (20 and 40). Successor is 40.
bst2.delete(70)  # Case 3: two children (60 and 80). Successor is 80.
bst2.delete(50)  # Case 3: root! Two children. Successor is 60.
```

### Practice: Write `tree_max()`

You've seen `_min_value` — follow left forever. Now write the counterpart:

```python
def _max_value(self, node):
    # Your code here — which direction do you follow?
    pass
```

**Hint:** If the smallest value is all the way left... where's the largest?

---

## Walking the Tree: Three Traversals

There are three classic ways to visit every node in a binary tree:

```python
def inorder(node):
    """Left → Node → Right — visits in sorted order for BST."""
    if node is None:
        return
    inorder(node.left)
    print(node.value, end=" ")
    inorder(node.right)

def preorder(node):
    """Node → Left → Right — useful for copying a tree."""
    if node is None:
        return
    print(node.value, end=" ")
    preorder(node.left)
    preorder(node.right)

def postorder(node):
    """Left → Right → Node — useful for deleting a tree."""
    if node is None:
        return
    postorder(node.left)
    postorder(node.right)
    print(node.value, end=" ")
```

```python
print("Inorder:", end=" ")
inorder(bst.root)
# 3 5 7 10 15 20  — sorted! That's the BST property in action

print("\nPreorder:", end=" ")
preorder(bst.root)
# 10 5 3 7 15 20

print("\nPostorder:", end=" ")
postorder(bst.root)
# 3 7 5 20 15 10
```

Inorder traversal of a BST gives you sorted order. That's a property you can rely on — no additional sorting needed.

---

## Tree Height

```python
def height(node):
    """Return the height of a subtree."""
    if node is None:
        return -1  # Empty tree has height -1 (by convention)
    left_height = height(node.left)
    right_height = height(node.right)
    return max(left_height, right_height) + 1


print(height(bst.root))  # 2
```

The height of our tree is 2 (root at 0, then 5 & 15 at depth 1, then 3, 7, 20 at depth 2). That's well-balanced!

### Height vs Diameter: What's the Longest Path?

**Height** = longest path from root to a leaf. That's what `height()` returns.

But what if the longest path *doesn't* go through the root?

```
        A
       / \
      B   C
     / \
    D   E
   /       \
  F         G
 /           \
H             I

Height from root = 3   (A → B → D → F → H, edges)
Diameter = 7           (H → F → D → B → E → G → I, edges)
```

The **diameter** is the longest path between *any* two nodes in the tree. For each node, it's: left height + right height + 2 (the two edges connecting through this node). The overall diameter is the **maximum** of that across all nodes.

```python
def diameter(node):
    """Return the diameter (longest path between any two nodes) of the tree."""
    if node is None:
        return 0

    # Option 1: the longest path goes through this node
    # It spans from deepest left leaf → node → deepest right leaf
    through_root = height(node.left) + height(node.right) + 2

    # Option 2: the longest path is entirely in the left subtree
    left_diameter = diameter(node.left)

    # Option 3: the longest path is entirely in the right subtree
    right_diameter = diameter(node.right)

    return max(through_root, left_diameter, right_diameter)
```

```python
# Test
bst = BST()
for v in [10, 5, 15, 3, 7, 12, 20]:
    bst.insert(v)

print(height(bst.root))    # 2 — longest root-to-leaf path
print(diameter(bst.root))  # 4 — longest path between any two nodes
                            # (3 → 5 → 10 → 15 → 20, 4 edges)

# The unbalanced tree actually has a large diameter too:
unbalanced = BST()
for v in [1, 2, 3, 4, 5]:
    unbalanced.insert(v)
print(diameter(unbalanced.root))  # 4 — it's just a straight line
```

**To summarise:**
- `height()` → longest path from **root** to any leaf
- `diameter()` → longest path between **any two nodes** in the tree

If someone asks for "the length of the longest path," clarify which one they mean — but in coding challenges it's almost always the diameter!

### Depth: Distance From Root to a Specific Node

Height tells you the deepest leaf. Diameter tells you the longest *any-to-any* path. But what if you want the distance from the root to a **specific** value? That's **depth** — the number of edges from root to that node.

```
        10          ← depth 0
       /  \
      5    15       ← depth 1
     / \     \
    3   7    20     ← depth 2
```

```python
def depth(self, value):
    """Return the number of edges from the root to a given value.
    Returns -1 if the value is not in the tree."""
    return self._depth_recursive(self.root, value, 0)

def _depth_recursive(self, node, value, current_depth):
    if node is None:
        return -1                     # Not found
    if node.value == value:
        return current_depth          # Found it!
    if value < node.value:
        return self._depth_recursive(node.left, value, current_depth + 1)
    return self._depth_recursive(node.right, value, current_depth + 1)
```

```python
bst = BST()
for v in [10, 5, 15, 3, 7, 20]:
    bst.insert(v)

print(bst.depth(10))   # 0 — the root is 0 edges from itself
print(bst.depth(5))    # 1 — one step left
print(bst.depth(20))   # 2 — two steps right
print(bst.depth(99))   # -1 — not in the tree
```

The trick: start at depth 0 at the root, add 1 every time you step down. When you find the node, that's the depth. Recursion carries the running count for you.

**Three tree measurements, summarised:**

| Function | Answers |
|----------|---------|
| `height(node)` | Longest path from this node to any leaf |
| `diameter(node)` | Longest path between *any* two nodes |
| `depth(value)` | Number of edges from root to this specific value |

Depth also tells you how many comparisons `search()` needed — every comparison takes you one level deeper. In a balanced BST, depth is O(log n).

---

## Practice: Check if a Tree is Balanced

**Your task:** A binary tree is **balanced** if for every node, the height of its left and right subtrees differ by at most 1. Write a function that returns `True` if a BST is balanced and `False` otherwise.

```python
def is_balanced(root):
    # Your code here
    pass


# Test on a balanced tree:
balanced = BST()
for v in [10, 5, 15, 3, 7, 12, 20]:
    balanced.insert(v)
print(is_balanced(balanced.root))  # True

# Test on an unbalanced tree:
unbalanced = BST()
for v in [1, 2, 3, 4, 5]:  # Inserted in order — straight line!
    unbalanced.insert(v)
print(is_balanced(unbalanced.root))  # False
```

**Think about it:** You need the `height()` function. For every node, check three things:
1. Is the left subtree balanced?
2. Is the right subtree balanced?
3. Do the heights differ by at most 1?

All three must be true.

Save as `balanced_tree.py` and try it!

---

## Solution

```python
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = TreeNode(value)
            return
        self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)


def height(node):
    if node is None:
        return -1
    return max(height(node.left), height(node.right)) + 1


def is_balanced(node):
    if node is None:
        return True
    left_height = height(node.left)
    right_height = height(node.right)
    return (
        abs(left_height - right_height) <= 1
        and is_balanced(node.left)
        and is_balanced(node.right)
    )


# Test
balanced = BST()
for v in [10, 5, 15, 3, 7, 12, 20]:
    balanced.insert(v)
print(f"Balanced tree: {is_balanced(balanced.root)}")  # True

unbalanced = BST()
for v in [1, 2, 3, 4, 5]:
    unbalanced.insert(v)
print(f"Unbalanced tree: {is_balanced(unbalanced.root)}")  # False
```

Notice that inserting in sorted order creates a "straight line" — basically a linked list. That's why real BSTs need **self-balancing** (like AVL or Red-Black trees) to maintain O(log n) performance.

---

## What You Just Learned

- **Tree** = linked list but each node can have multiple children
- **Binary tree** = each node has at most 2 children (left and right)
- **BST** = left < node < right — enables O(log n) search, insert, and delete
- **BST delete** = three cases: leaf (easy), one child (bypass), two children (find inorder successor)
- **Traversals** = inorder (sorted), preorder (copy), postorder (delete)
- **Height** = longest path from root to leaf
- **Diameter** = longest path between *any* two nodes — may not pass through root
- **Depth** = distance (edges) from root to a specific node
- **Balancing** matters — a BST is only fast if it's balanced

---

## What's Next?

Trees are everywhere in CS. Now let's look at the algorithms that make sense of data — starting with sorting.

Next up: **[Lesson 20: Heaps](20-heaps.md)** — a tree-based structure that always gives you the smallest element instantly ⛰️

---

**Your turn:** Build the BST, implement `is_balanced`, and try deleting nodes from different cases (leaf, one child, two children). Then implement `_max_value()` and `tree_min()` — what's the smallest value in a BST? Which side should you follow? 💛

### Bonus Solution: tree_max() and tree_min()

```python
def _min_value(self, node):
    """Smallest value — follow left forever."""
    current = node
    while current.left is not None:
        current = current.left
    return current

def _max_value(self, node):
    """Largest value — follow right forever."""
    current = node
    while current.right is not None:
        current = current.right
    return current
```

It's symmetrical: `tree_min()` goes left, `tree_max()` goes right. No recursion needed — just a simple loop until you hit `None`.
