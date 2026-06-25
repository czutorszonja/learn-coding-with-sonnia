# Lesson 15: Stacks

**← Back to [Lesson 14: Time & Space Complexity](14-complexity.md)**

---

## The Problem: You Can Only See the Top

Imagine you're building a browser's back button. Every time you visit a page, you need to remember it. When you press back, you need the LAST page you visited.

You could use a list:

```python
history = []
history.append("Homepage")
history.append("About Us")
history.append("Contact")

# Press back — you want the last one:
print(history[-1])  # "Contact"
# Remove it so you can get to the previous:
history.pop()
print(history[-1])  # "About Us"
```

This works, but there's nothing stopping someone from doing `history[1]` or inserting in the middle. A browser's back button shouldn't let you skip three pages ahead or rearrange history — you should only be able to go back in reverse order. The last thing you saw is the first thing you leave.

That's exactly what a **stack** is. It's a list with one rule: only the top matters.

---

## The Idea: LIFO — Last In, First Out

**In plain English:** A stack is a pile where you can only add to the top and take from the top. The last thing you put on is the first thing you take off.

**Real-world analogy:** A stack of plates at a buffet.
- You can only grab the top plate
- New clean plates go on top
- You can't pull one from the middle
- The plate you just put there is the first one someone takes

**Three operations. That's it.**

| Operation | What it does | Python way |
|-----------|-------------|-----------|
| **Push** | Add an item to the top | `stack.append(item)` |
| **Pop** | Remove and return the top item | `stack.pop()` |
| **Peek** | Look at the top without removing | `stack[-1]` |

No inserting in the middle. No removing from the bottom. Just the top.

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

A raw list works, but nothing stops someone from doing `stack[1]` or inserting in the middle. A class enforces the rules:

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

## Step by Step: Building Undo One Layer at a Time

### Step 1: Undo Only

Let's start simple. A text editor that remembers the text before each change, so you can undo:

```python
class SimpleEditor:
    def __init__(self):
        self.text = ""
        self._history = []   # A stack of previous text states

    def type(self, new_text):
        self._history.append(self.text)   # Save current before changing
        self.text += new_text

    def undo(self):
        if not self._history:
            return "Nothing to undo"
        self.text = self._history.pop()   # Go back to previous state
        return self.text


editor = SimpleEditor()
editor.type("Hello")
editor.type(" World")
print(editor.text)       # Hello World
print(editor.undo())     # Hello
print(editor.undo())     # (empty)
```

Each time you type, the editor saves the old text onto the stack. Undo pops the top — the last saved state. **Last pushed, first popped.** That's the stack at work.

### Step 2: Add Redo

Now we want _redo_ too. Going back is great, but what if you undo too far? You need a way to go forward again.

The trick: when you undo, instead of throwing the current state away, push it onto a SEPARATE redo stack:

```python
class UndoRedoEditor:
    def __init__(self):
        self.text = ""
        self._undo_stack = []   # Previous states
        self._redo_stack = []   # Forward states (for redo)

    def type(self, new_text):
        self._undo_stack.append(self.text)  # Save current state
        self.text += new_text
        self._redo_stack = []               # New action = clear redo

    def undo(self):
        if not self._undo_stack:
            return "Nothing to undo"
        self._redo_stack.append(self.text)  # Save current for redo
        self.text = self._undo_stack.pop()
        return f"Undid! Text: '{self.text}'"

    def redo(self):
        if not self._redo_stack:
            return "Nothing to redo"
        self._undo_stack.append(self.text)  # Save current for undo
        self.text = self._redo_stack.pop()
        return f"Redid! Text: '{self.text}'"


editor = UndoRedoEditor()
editor.type("Hello")
editor.type(" World")
print(editor.text)                # Hello World

editor.undo()
print(editor.text)                # Hello

editor.undo()
print(editor.text)                # (empty)

editor.redo()
print(editor.text)                # Hello

editor.redo()
print(editor.text)                # Hello World

# New action clears redo — can't redo after typing:
editor.type("!!")
print(editor.redo())              # Nothing to redo
```

Two stacks, one purpose each:
- `_undo_stack` — saves old states as you make changes
- `_redo_stack` — saves undone states so you can go forward again

The key detail: when you make a NEW change, `self._redo_stack = []` clears the forward history — because you can't redo after changing something new.

---

## Practice: Browser History

**Your task:** Build a browser navigation system using two stacks.

Create a `BrowserHistory` class:
- `visit(url)` — go to a new page (clears forward history)
- `back()` — go to the previous page, return the URL
- `forward()` — go to the next page, return the URL
- `current()` — return the current URL
- `can_go_back()` and `can_go_forward()` — boolean checks

**Think about it like this:**
- When you visit a new page, push the old current page onto the **back stack**
- When you go back, push the current page onto the **forward stack**, then pop the back stack
- When you go forward, push the current page onto the **back stack**, then pop the forward stack
- Visiting a new page clears the forward stack (same as the editor's redo)

**Test it:**

```python
bh = BrowserHistory()
bh.visit("google.com")
bh.visit("github.com")
bh.visit("stackoverflow.com")

print(bh.back())     # github.com
print(bh.back())     # google.com
print(bh.forward())  # github.com
print(bh.current())  # github.com

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
- **Two stacks** can model back/forward, undo/redo — any two-way navigation
- **New action clears forward history** — can't redo/forward past a fresh change
- **A class enforces the rules** — no cheating with index access

---

## What's Next?

Stacks are LIFO. Queues are FIFO — first come, first served. Coffee shop line, print queue, message processing — all queues.

Continue to **[Lesson 16: Queues](16-queues.md)** 🚶‍♂️

---

**Your turn:** Build the browser! Then add a `go_back_to(url)` method that keeps going back until it finds a specific URL (or runs out of history). 📚💛

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

Continue to **[Lesson 16: Queues](16-queues.md)** 🚶‍♂️

---

**Your turn:** Build the browser! Then add a `go_back_to(url)` method that keeps going back until it finds a specific URL (or runs out of history). 📚💛
