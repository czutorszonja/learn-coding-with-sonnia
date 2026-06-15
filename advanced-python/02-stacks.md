# Advanced Python Lesson 2: Stacks — Last In, First Out 📚

**← Back to [Lesson 1: OOP Deep Dive](01-oop-deep-dive.md)**

---

## What is a Stack?

**Plain English:** A stack is a collection where you can only add and remove from the _top_. The last item you put on is the first one you take off — LIFO (Last In, First Out).

**Real-world analogy:** A stack of plates at a buffet:
- You can only take the _top_ plate
- New plates go on _top_
- You can't pull one from the middle without toppling everything
- The plate you just put there is the first one someone grabs

---

## Core Operations

| Operation | What it does | Python |
|-----------|-------------|--------|
| Push | Add to the top | `stack.append(item)` |
| Pop | Remove from the top | `stack.pop()` |
| Peek | Look at the top without removing | `stack[-1]` |
| Is Empty? | Check if anything's there | `len(stack) == 0` |
| Size | How many items? | `len(stack)` |

**All O(1)** — instant, no matter how big the stack!

---

## Stack Using a Python List

```python
stack = []

# Push
stack.append("page1")
stack.append("page2")
stack.append("page3")

print(stack)     # ['page1', 'page2', 'page3']
print(stack[-1]) # 'page3' — peek at top

# Pop
top = stack.pop()
print(top)       # 'page3'
print(stack)     # ['page1', 'page2']

# Check if empty
print(len(stack) == 0)  # False
print(not stack)        # False (more Pythonic)
```

---

## Building a Stack Class

```python
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __str__(self):
        return f"Stack({self._items})"

    def __iter__(self):
        """Iterate from top to bottom."""
        return reversed(self._items)
```

---

## Real-World Use Cases

### 1. Undo/Redo (Every Editor Ever)

> 💡 **This example uses the `Stack` class.** Copy the Stack class from the [Building a Stack Class](#building-a-stack-class) section above first, or here's a compact version:

```python
# === Include this Stack class (from "Building a Stack Class" above) ===
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

# ================================================================

class TextEditor:
    def __init__(self):
        self._text = ""
        self._undo_stack = Stack()
        self._redo_stack = Stack()

    @property
    def text(self):
        return self._text

    def type(self, new_text):
        """Type something — save old state for undo."""
        self._undo_stack.push(self._text)
        self._text += new_text
        self._redo_stack = Stack()  # Clear redo on new action

    def delete_last(self, count=1):
        """Delete last n characters."""
        self._undo_stack.push(self._text)
        self._text = self._text[:-count]
        self._redo_stack = Stack()

    def undo(self):
        if self._undo_stack.is_empty():
            return "Nothing to undo"
        self._redo_stack.push(self._text)
        self._text = self._undo_stack.pop()
        return f"Undid! Text is now: '{self._text}'"

    def redo(self):
        if self._redo_stack.is_empty():
            return "Nothing to redo"
        self._undo_stack.push(self._text)
        self._text = self._redo_stack.pop()
        return f"Redid! Text is now: '{self._text}'"


editor = TextEditor()
editor.type("Hello")
editor.type(" World")
print(editor.text)   # "Hello World"

editor.delete_last(5)
print(editor.text)   # "Hello "

print(editor.undo()) # "Hello World" — back!
print(editor.redo()) # "Hello " — forward again
```

### 2. Balanced Parentheses

```python
# === Include this Stack class (from "Building a Stack Class" above) ===
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)
# ================================================================

def is_balanced(expression):
    """Check if brackets/parens/braces are balanced."""
    matching = {')': '(', ']': '[', '}': '{'}
    stack = Stack()

    for char in expression:
        if char in '([{':
            stack.push(char)
        elif char in ')]}':
            if stack.is_empty():
                return False
            if stack.pop() != matching[char]:
                return False

    return stack.is_empty()  # All opened brackets must be closed


print(is_balanced("(a + b) * (c - d)"))   # True
print(is_balanced("(a + b]"))              # False — mismatched
print(is_balanced("((a + b)"))            # False — unclosed bracket
print(is_balanced("{[()]}"))              # True
print(is_balanced("{[(])}"))              # False — crossing brackets
```

### 3. Call Stack Simulation

```python
# === Include this Stack class (from "Building a Stack Class" above) ===
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        """Iterate from top to bottom."""
        return reversed(self._items)
# ================================================================

class CallStack:
    def __init__(self):
        self._frames = Stack()

    def call(self, function_name, *args):
        self._frames.push({"function": function_name, "args": args, "locals": {}})
        print(f"→ Called {function_name}({', '.join(map(str, args))})")
        self._print_stack()

    def return_from(self):
        if self._frames.is_empty():
            return "Stack is empty"
        frame = self._frames.pop()
        print(f"← Returned from {frame['function']}")

    def _print_stack(self):
        print("  Call stack (top → bottom):")
        for i, frame in enumerate(self._frames):
            indent = "  " * i
            print(f"{indent}  {frame['function']}({frame['args']})")


cs = CallStack()
cs.call("main")
cs.call("calculate_total", 10, 20)
cs.call("apply_discount", 200.0, 0.15)
cs.return_from()
cs.return_from()
cs.return_from()

# → Called main()
# → Called calculate_total(10, 20)
# → Called apply_discount(200.0, 0.15)
# ← Returned from apply_discount
# ← Returned from calculate_total
# ← Returned from main
```

### 4. Expression Evaluation (Postfix Notation)

```python
# === Include this Stack class (from "Building a Stack Class" above) ===
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)
# ================================================================

def evaluate_postfix(expression):
    """Evaluate postfix (Reverse Polish Notation) expression.
    Example: "3 4 + 2 *" → (3 + 4) * 2 = 14
    """
    stack = Stack()

    for token in expression.split():
        if token.lstrip('-').isdigit():  # Number (including negative)
            stack.push(int(token))
        else:
            # Operator — pop two operands
            b = stack.pop()
            a = stack.pop()

            if token == '+':
                stack.push(a + b)
            elif token == '-':
                stack.push(a - b)
            elif token == '*':
                stack.push(a * b)
            elif token == '/':
                stack.push(a / b)
            elif token == '^':
                stack.push(a ** b)

    return stack.pop()


print(evaluate_postfix("3 4 +"))         # 7
print(evaluate_postfix("3 4 + 2 *"))     # 14
print(evaluate_postfix("5 1 2 + 4 * + 3 -"))  # 5 + (1+2)*4 - 3 = 14
print(evaluate_postfix("2 3 ^"))         # 8
```

---

## Stack vs List — When to Use a Stack

| Use a Stack when… | Use a List when… |
|------------------|-----------------|
| You only need LIFO access | You need random access by index |
| You want to _enforce_ LIFO (prevents bugs) | You need to insert in the middle |
| The problem is naturally stack-shaped | You need to iterate forward and backward |
| Undo/redo, backtracking, parsing | General-purpose collection |

---

## Common Stack Patterns

### Pattern 1: Monotonic Stack (Next Greater Element)

```python
# === Include this Stack class (from "Building a Stack Class" above) ===
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)
# ================================================================

def next_greater_element(arr):
    """For each element, find the next element that's larger."""
    result = [-1] * len(arr)
    stack = Stack()  # Stores INDICES, not values

    for i, value in enumerate(arr):
        # Pop while stack top's value < current value
        while not stack.is_empty() and arr[stack.peek()] < value:
            idx = stack.pop()
            result[idx] = value
        stack.push(i)

    return result


print(next_greater_element([4, 5, 2, 10, 8]))
# Output: [5, 10, 10, -1, -1]
# Explanation:
#   4 → next greater is 5
#   5 → next greater is 10
#   2 → next greater is 10
#  10 → no greater element (-1)
#   8 → no greater element (-1)
```

### Pattern 2: Two Stacks for a Queue

```python
# === Include this Stack class (from "Building a Stack Class" above) ===
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)
# ================================================================

class QueueFromStacks:
    """A queue implemented using two stacks."""

    def __init__(self):
        self._in = Stack()   # For enqueue
        self._out = Stack()  # For dequeue

    def enqueue(self, item):
        self._in.push(item)

    def dequeue(self):
        if self._out.is_empty():
            # Transfer everything from in to out (reverses order!)
            while not self._in.is_empty():
                self._out.push(self._in.pop())
        return self._out.pop()

    @property
    def is_empty(self):
        return self._in.is_empty() and self._out.is_empty()
```

---

## Practice Exercise

**Scenario:** You're building a browser's back/forward navigation system. Visiting a new page adds to history, back/forward navigates through it.

**Your task:**

1. Create `browser_history.py` with a `BrowserHistory` class that:
   - `visit(url)` — go to a new page (clears forward history!)
   - `back()` — go to the previous page, returns the URL
   - `forward()` — go to the next page, returns the URL
   - `current()` — returns the current URL
   - `history()` — returns list of pages in the back stack
   - `can_go_back()` and `can_go_forward()` — boolean checks

2. Use two stacks: one for back history, one for forward history

3. Handle edge cases:
   - Can't go back if there's no history
   - Going to a new page clears the forward stack
   - Current page isn't in either stack

4. Write a `BrowserHistory` that also tracks a `tab_id` so you can have multiple tabs

5. Test it:
   ```python
   bh = BrowserHistory()
   bh.visit("google.com")
   bh.visit("github.com")
   bh.visit("stackoverflow.com")
   bh.back()        # Should return "github.com"
   bh.back()        # Should return "google.com"
   bh.forward()     # Should return "github.com"
   bh.visit("reddit.com")  # Clears forward!
   print(bh.can_go_forward())  # False — forward cleared!
   ```

**Try it yourself first!** Solution below.

---

## Solution

```python
class Stack:
    """Simple stack implementation."""

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self):
        return self._items[-1] if self._items else None

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(reversed(self._items))

    def to_list(self):
        """Convert to list, top first."""
        return list(reversed(self._items))


class BrowserHistory:
    """Browser back/forward navigation using two stacks."""

    def __init__(self):
        self._back_stack = Stack()
        self._forward_stack = Stack()
        self._current = None

    def visit(self, url):
        """Navigate to a new URL. Clears forward history."""
        if self._current is not None:
            self._back_stack.push(self._current)
        self._current = url
        self._forward_stack = Stack()  # Clear forward history!
        return f"Visited: {url}"

    def back(self):
        """Go back one page. Returns the URL."""
        if self._back_stack.is_empty():
            return None  # Can't go back

        self._forward_stack.push(self._current)
        self._current = self._back_stack.pop()
        return self._current

    def forward(self):
        """Go forward one page. Returns the URL."""
        if self._forward_stack.is_empty():
            return None  # Can't go forward

        self._back_stack.push(self._current)
        self._current = self._forward_stack.pop()
        return self._current

    def current(self):
        """Return the current URL."""
        return self._current

    def can_go_back(self):
        return not self._back_stack.is_empty()

    def can_go_forward(self):
        return not self._forward_stack.is_empty()

    def history(self):
        """Return back history (oldest first)."""
        return self._back_stack.to_list()

    def __str__(self):
        back = self._back_stack.to_list()
        fwd = self._forward_stack.to_list()
        return (
            f"Back: {back}\n"
            f"→ Current: {self._current}\n"
            f"Forward: {fwd}"
        )


# --- Multi-tab version (stretch goal) ---

class MultiTabBrowser:
    """Browser with multiple tabs, each with its own history."""

    def __init__(self):
        self._tabs = {}  # tab_id → BrowserHistory

    def open_tab(self, tab_id):
        """Open a new tab."""
        self._tabs[tab_id] = BrowserHistory()
        return f"Opened tab '{tab_id}'"

    def close_tab(self, tab_id):
        """Close a tab."""
        if tab_id in self._tabs:
            del self._tabs[tab_id]
            return f"Closed tab '{tab_id}'"
        return f"No tab named '{tab_id}'"

    def get_tab(self, tab_id):
        """Get a tab's BrowserHistory."""
        if tab_id not in self._tabs:
            self.open_tab(tab_id)
        return self._tabs[tab_id]

    @property
    def tabs(self):
        return list(self._tabs.keys())


# --- Test ---
if __name__ == "__main__":
    print("=== Single Tab ===")
    bh = BrowserHistory()
    print(bh.visit("google.com"))
    print(bh.visit("github.com"))
    print(bh.visit("stackoverflow.com"))

    print(f"\nCurrent: {bh.current()}")
    print(f"Can go back: {bh.can_go_back()}")
    print(f"Back: {bh.back()}")
    print(f"Back: {bh.back()}")
    print(f"Current: {bh.current()}")
    print(f"Forward: {bh.forward()}")

    # Visit a new page — clears forward history
    print(f"\n{bh.visit('reddit.com')}")
    print(f"Can go forward: {bh.can_go_forward()}")  # False!

    print(f"\n=== Multi-tab ===")
    mb = MultiTabBrowser()
    mb.open_tab("work")
    mb.open_tab("fun")

    mb.get_tab("work").visit("github.com")
    mb.get_tab("work").visit("docs.python.org")
    mb.get_tab("fun").visit("youtube.com")
    mb.get_tab("fun").visit("netflix.com")

    print(f"Tabs: {mb.tabs}")
    print(f"\nWork tab:\n{mb.get_tab('work')}")
    print(f"\nFun tab:\n{mb.get_tab('fun')}")
```

---

## Quick Recap

- **Stack** — LIFO, push/pop/peek, all O(1)
- **Key use cases:** undo/redo, browser history, call stacks, expression evaluation, backtracking
- **Python list as stack:** `append()` / `pop()` from the end
- **Two-stack queue:** transfer between stacks to reverse order
- **Monotonic stack:** find next greater/smaller element efficiently
- **Wrapping in a class** enforces correct usage and prevents accidental index access

---

## What's Next?

Stacks are LIFO — now let's look at their sibling: the queue (FIFO). Continue to **[Lesson 3: Queues](03-queues.md)** 🚶‍♂️

---

**Your turn:** Build the browser history! Then try adding a `go_to_history_index(n)` method that jumps back n pages (e.g., `go_to_history_index(3)` goes back 3 pages at once). 📚💛
