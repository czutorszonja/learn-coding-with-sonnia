# Data Structures Lesson 6: Trees 🌳

**← Back to [Linked Lists](05-linked-lists.md)**

---

## The Problem: Data That Has Branches

Linked lists are great for linear sequences. But what about data that naturally branches?

- A file system (folders inside folders inside folders)
- An HTML document (tags nested in tags)
- A game AI's possible moves (each move leads to more moves)
- A family tree (parents, children, siblings)

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

## Building a BST

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

## Walking the Tree: Traversals

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

Inorder traversal of a BST gives you sorted order. That's not a coincidence — it's a property you can rely on.

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

Hints:
- You'll need the `height()` function (it's recursive!)
- Check if left and right subtrees are balanced, AND their heights differ by ≤ 1
- Both conditions must be true for every node

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
    # Check current node AND all subtrees
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
- **BST** = left < node < right — enables O(log n) search
- **Traversals** = inorder (sorted), preorder (copy), postorder (delete)
- **Balancing** matters — a BST is only fast if it's balanced

---

## What's Next?

Trees are everywhere in CS. Now let's look at the algorithms that make sense of data — starting with sorting.

Next up: **[Sorting](../algorithms/02-sorting.md)** — bubble sort, merge sort, and why it matters 📊

---

**Trees click differently for everyone.** For some people, it's the visual shape that makes sense. For others, it's the recursive definition. Find your angle. 💛
