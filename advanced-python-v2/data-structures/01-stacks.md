# Data Structures Lesson 1: Stacks 📚

**← Back to [OOP Lesson 4: Composition](../oop/04-composition.md)**

---

## What is a Stack?

**Plain English:** A stack is a pile of things where you can only add to the top and take from the top. The last thing you put on is the first thing you take off.

**Real-world analogy:** A stack of plates at a buffet.
- You can only grab the top plate
- New clean plates go on top
- You can't pull one from the middle
- The plate you just put there is the first one someone takes

---

## The Operations

A stack only needs three things:

| Operation | What it does | Python way |
|-----------|-------------|-----------|
| Push | Add an item to the top | `stack.append(item)` |
| Pop | Remove and return the top item | `stack.pop()` |
| Peek | Look at the top without removing | `stack[-1]` |

That's it. No inserting in the middle. No removing from the bottom. Just the top.

---

## The Simplest Stack: A Python List

```python
stack = []

# Push (add to top)
stack.append("page1")
stack.append("page2")
stack.append("page3")

print(stack)      # ['page1', 'page2', 'page3']
print(stack[-1])  # 'page3'  ← peek at the top

# Pop (remove from top)
top = stack.pop()
print(top)        # 'page3'
print(stack)      # ['page1', 'page2']

# Check if empty
print(len(stack) == 0)  # False
print(not stack)        # False  (more Pythonic way)
```

---

## Wrapping It in a Class

A raw list works, but there's nothing stopping someone from doing `stack[1]` or inserting in the middle. A class enforces the rules:

```python
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        """Add an item to the top."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item."""
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack")
        return self._items.pop()

    def peek(self):
        """Look at the top item without removing it."""
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        """Is the stack empty?"""
        return len(self._items) == 0

    def __len__(self):
        """How many items are in the stack?"""
        return len(self._items)

    def __str__(self):
        return f"Stack({self._items})"
```

---

## The Classic Example: Undo/Redo

Stacks are PERFECT for undo — every action gets pushed onto a stack, and undo just pops:

```python
class TextEditor:
    def __init__(self):
        self._text = ""
        self._undo_stack = Stack()
        self._redo_stack = Stack()

    @property
    def text(self):
        return self._text

    def type(self, new_text):
        """Type something — save current state before changing."""
        self._undo_stack.push(self._text)
        self._text += new_text
        self._redo_stack = Stack()  # Clear redo on new action

    def delete_last(self, count=1):
        """Delete characters — save state first."""
        self._undo_stack.push(self._text)
        self._text = self._text[:-count]
        self._redo_stack = Stack()

    def undo(self):
        if self._undo_stack.is_empty():
            return "Nothing to undo"
        self._redo_stack.push(self._text)
        self._text = self._undo_stack.pop()
        return f"Undid! Text: '{self._text}'"

    def redo(self):
        if self._redo_stack.is_empty():
            return "Nothing to redo"
        self._undo_stack.push(self._text)
        self._text = self._redo_stack.pop()
        return f"Redid! Text: '{self._text}'"


editor = TextEditor()
editor.type("Hello")
editor.type(" World")
print(editor.text)    # Hello World

editor.delete_last(5)
print(editor.text)    # Hello

print(editor.undo())  # Hello World — back!
print(editor.redo())  # Hello — forward again
```

Two stacks: one for undo, one for redo. When you type something new, the redo stack gets cleared — you can't redo after making a new change.

---

## Practice: Browser Back/Forward

**Your task:** Build a browser history system using two stacks.

Create a `BrowserHistory` class:
- `visit(url)` — go to a new page (clears forward history)
- `back()` — go to the previous page, return the URL
- `forward()` — go to the next page, return the URL
- `current()` — return the current URL
- `can_go_back()` and `can_go_forward()` — boolean checks

**Test it:**

```python
bh = BrowserHistory()
bh.visit("google.com")
bh.visit("github.com")
bh.visit("stackoverflow.com")

print(bh.back())     # github.com
print(bh.back())     # google.com
print(bh.forward())  # github.com

bh.visit("reddit.com")  # Visiting clears forward!
print(bh.can_go_forward())  # False
```

Create `browser_history.py` and try it!

---

## Solution

```python
class BrowserHistory:
    def __init__(self):
        self._back_stack = []
        self._forward_stack = []
        self._current = None

    def visit(self, url):
        """Navigate to a page. Clears forward history."""
        if self._current is not None:
            self._back_stack.append(self._current)
        self._current = url
        self._forward_stack = []  # Clear forward
        return f"Visited: {url}"

    def back(self):
        """Go back one page."""
        if not self._back_stack:
            return None
        self._forward_stack.append(self._current)
        self._current = self._back_stack.pop()
        return self._current

    def forward(self):
        """Go forward one page."""
        if not self._forward_stack:
            return None
        self._back_stack.append(self._current)
        self._current = self._forward_stack.pop()
        return self._current

    def current(self):
        return self._current

    def can_go_back(self):
        return len(self._back_stack) > 0

    def can_go_forward(self):
        return len(self._forward_stack) > 0

    def __str__(self):
        return (
            f"Back: {self._back_stack}\n"
            f"→ Current: {self._current}\n"
            f"Forward: {self._forward_stack}"
        )


# Test
bh = BrowserHistory()
bh.visit("google.com")
bh.visit("github.com")
bh.visit("stackoverflow.com")

print(bh.back())        # github.com
print(bh.back())        # google.com
print(bh.forward())     # github.com

bh.visit("reddit.com")
print(bh.can_go_forward())  # False
```

---

## What You Just Learned

- **Stack = LIFO** (Last In, First Out) — only the top matters
- **Push** adds to the top, **pop** removes from the top
- **Two stacks** can model back/forward, undo/redo, and many other patterns
- **A class enforces the rules** — no cheating with index access

---

## What's Next?

Stacks are LIFO. Queues are FIFO — first come, first served. Coffee shop line, print queue, message processing — all queues.

Continue to **[Lesson 2: Queues](02-queues.md)** 🚶‍♂️

---

**Your turn:** Build the browser! Then add a `go_back_to(url)` method that keeps going back until it finds a specific URL (or runs out of history). 📚💛
