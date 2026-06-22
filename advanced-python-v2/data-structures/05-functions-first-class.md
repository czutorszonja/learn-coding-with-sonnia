# Data Structures Lesson 5: Functions as First-Class Citizens 🎭

**← Back to [Lesson 4: Iterables & Iterators](04-iterables-iterators.md)**

---

## The Problem: Functions Feel Like Fixed Tools

You've written dozens of functions. They take inputs, do things, return outputs:

```python
def add(a, b):
    return a + b

def greet(name):
    return f"Hello, {name}!"

print(add(3, 4))       # 7
print(greet("Szonja"))  # Hello, Szonja!
```

But functions always felt like fixed appliances — you call them by name, they do their one job. What if you wanted to **choose which function to call at runtime**? Or **create new functions on the fly**? Or have a function that **builds other functions**?

In some languages, functions are second-class — they can only be defined and called. Python is different.

---

## The Idea: Functions Are Just Values

In Python, **functions are objects**. They're just values, like `5` or `"hello"` or `[1, 2, 3]`. Anything you can do with a value, you can do with a function:

| With a number | With a function |
|---|---|
| `x = 5` | `f = len` |
| `[5, 10, 15]` | `[len, max, sorted]` |
| `return 5` | `return some_function` |
| `process(5)` | `map(str.upper, names)` |

Python calls this **"functions are first-class citizens."** Once you internalise this, a whole layer of the language opens up.

---

## Step by Step

### Part 1: Assigning Functions to Variables

You can give a function a new name just by assigning it:

```python
def greet(name):
    return f"Hello, {name}!"

say_hello = greet  # No parentheses! We're not calling it — we're pointing to it.

print(say_hello("Szonja"))  # Hello, Szonja!
print(say_hello is greet)   # True — they're the SAME function object
```

**The `()` is the call operator.** Without it, you're just referencing the function object. With it, you're executing it:

```python
x = greet          # x IS the function
y = greet("Ana")   # y is the RESULT "Hello, Ana!"
```

### Part 2: Passing Functions as Arguments

This is where things get powerful. You can pass a function to another function:

```python
def apply(func, value):
    return func(value)

def double(x):
    return x * 2

def shout(x):
    return str(x).upper()

print(apply(double, 7))    # 14
print(apply(shout, "hi"))  # HI
```

You've actually used this pattern already — `sorted()` with a `key`:

```python
words = ["banana", "apple", "cherry", "date"]

# key is a function — we're passing str.lower as an argument
print(sorted(words, key=str.lower))  # ['apple', 'banana', 'cherry', 'date']
print(sorted(words, key=len))        # ['date', 'apple', 'banana', 'cherry']
```

### Part 3: Returning Functions from Functions

A function can **build and return** another function:

```python
def make_multiplier(factor):
    def multiply_by(x):
        return x * factor
    return multiply_by  # Returning the FUNCTION, not a number

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(10))  # 20
print(triple(10))  # 30
```

Wait — how does `multiply_by` remember `factor` after `make_multiplier` has finished? That's a **closure**, and it's one of Python's most elegant features.

### Part 4: Nested Functions (Functions Inside Functions)

You can define functions **inside** other functions. They're called nested functions:

```python
def describe_list(items):
    def plural(n):
        """Helper: returns 'is' or 'are' based on count."""
        return "is" if n == 1 else "are"

    def items_word(n):
        """Helper: returns 'item' or 'items'."""
        return "item" if n == 1 else "items"

    count = len(items)
    return f"There {plural(count)} {count} {items_word(count)} in the list."

print(describe_list([42]))          # There is 1 item in the list.
print(describe_list([1, 2, 3]))     # There are 3 items in the list.
```

Nested functions are perfect for **helpers that only matter inside one function**. They keep your namespace clean — no one else needs to see `plural()` and `items_word()`.

### Part 5: Closures — Nested Functions That Remember

A **closure** is a nested function that remembers values from its enclosing scope, even after the outer function has returned:

```python
def make_counter(start=0):
    count = [start]  # Using a list so we can mutate it

    def increment():
        count[0] += 1
        return count[0]

    return increment

counter_a = make_counter(0)
counter_b = make_counter(100)

print(counter_a())  # 1
print(counter_a())  # 2
print(counter_a())  # 3
print(counter_b())  # 101 — separate counter, separate memory!
```

Each time you call `make_counter()`, Python creates a **brand new** `count` list and a **brand new** `increment` function that's forever bound to its own `count`. They don't interfere.

The nonlocal version (cleaner, Python 3+):

```python
def make_counter(start=0):
    count = start

    def increment():
        nonlocal count  # "Use the count from the enclosing scope"
        count += 1
        return count

    return increment
```

`nonlocal` tells Python: "count is not local to increment, and it's not global either — it's in the outer function's scope."

### Part 6: Why This Matters for Data Structures

When we build linked lists, trees, and other structures, we'll use these patterns constantly:

```python
# Sorting a linked list with a custom comparison:
def sort_list(head, key_func):
    # key_func is passed in — could be lambda n: n.age or str.lower
    ...

# Traversing a tree with a visitor function:
def walk_tree(node, visit_func):
    visit_func(node)
    if node.left:
        walk_tree(node.left, visit_func)  # Same visitor for left subtree
    if node.right:
        walk_tree(node.right, visit_func) # Same visitor for right subtree

# Building a custom data structure with a closure:
def make_stack_factory():
    stack = []
    def push(item): stack.append(item)
    def pop(): return stack.pop()
    def peek(): return stack[-1] if stack else None
    return push, pop, peek  # Returns three functions sharing the same stack!
```

### Part 7: Lambda — Quick, Nameless Functions

Sometimes a function is so short that giving it a name feels wasteful. `lambda` creates a function without a `def`:

```python
# These are equivalent:

def by_length(word):
    return len(word)

sorted(words, key=by_length)

# vs.

sorted(words, key=lambda word: len(word))
```

Lambda syntax: `lambda arguments: expression`

```python
add = lambda a, b: a + b
print(add(3, 4))  # 7

# Lambda shines as an argument:
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x ** 2, numbers))
print(squares)  # [1, 4, 9, 16, 25]
```

**Lambda rule:** Use it for one-liners passed to other functions. If the logic needs more than one line, use `def`.

---

## Practice

Build a **`create_multiplier`** function that takes a number `n` and returns a **new function**. That returned function should multiply whatever you give it by `n`.

Then use it to build:
1. A `double` function (multiplies by 2)
2. A `triple` function (multiplies by 3)
3. A `times_ten` function (multiplies by 10)

```python
# Your code here:


# After you write it, this should work:
# double = create_multiplier(2)
# triple = create_multiplier(3)
# times_ten = create_multiplier(10)
#
# print(double(5))    # 10
# print(triple(5))    # 15
# print(times_ten(5)) # 50
```

---

## Solution

<details>
<summary>Click to reveal</summary>

```python
def create_multiplier(n):
    def multiply(x):
        return x * n
    return multiply

double = create_multiplier(2)
triple = create_multiplier(3)
times_ten = create_multiplier(10)

print(double(5))    # 10
print(triple(5))    # 15
print(times_ten(5)) # 50
```

**What's happening:** `create_multiplier(2)` returns a `multiply` function that has `n=2` baked in. When you call `double(5)`, that `multiply` function still has access to `n=2` — that's the closure. Each call to `create_multiplier` creates a fresh `n` and a fresh `multiply` bound to it.

</details>

---

## Recap

- **Functions are values.** Assign them, pass them, return them, store them.
- **`()` is the call operator.** `greet` is the function. `greet("Ana")` calls it.
- **Nested functions** are defined inside other functions — perfect for private helpers.
- **Closures** are nested functions that remember their enclosing scope, even after the outer function returns.
- **`nonlocal`** lets a nested function modify a variable in the outer scope.
- **`lambda`** creates quick, one-expression functions — use it for simple callbacks.
- **Higher-order functions** take or return other functions — `sorted(..., key=...)`, `map()`, `filter()`.

---

**Next: [Lesson 6: Linked Lists](06-linked-lists.md) →**
