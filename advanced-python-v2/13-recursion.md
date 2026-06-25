# Lesson 13: Recursion

**← Back to [Lesson 12: Decorators](12-decorators.md)**

---

## The Idea: A Function That Calls Itself

Recursion sounds trippy at first: **a function that calls itself**. But it's actually one of the most natural ways to solve certain problems.

Think about a Russian nesting doll (matryoshka):

```
To open a matryoshka:
  1. Look at the doll in front of you
  2. If there's no smaller doll inside → you're at the centre, done ✅
  3. If there IS a smaller doll inside → open it and repeat from step 1 🔄
```

That's recursion. A process that repeats itself on a smaller version of the same problem until it reaches the simplest possible case.

---

## The Two Parts

Every recursive function needs two things:

1. **Base case** — the stopping condition. "When do I stop calling myself?"
2. **Recursive case** — the self-call. "How do I get closer to the base case?"

Without a base case, the function calls itself forever and you get a `RecursionError`.

---

## The Classic: Factorial

Factorial is the "Hello World" of recursion:

- `5!` = 5 × 4 × 3 × 2 × 1 = 120
- `4!` = 4 × 3 × 2 × 1 = 24

Notice something? `5!` = 5 × `4!`

That's the recursive insight: **a factorial is `n` times the factorial of `n - 1`**.

```python
def factorial(n):
    # Base case: 0! and 1! are both 1
    if n <= 1:
        return 1
    # Recursive case: n! = n × (n-1)!
    return n * factorial(n - 1)

print(factorial(5))  # 120
print(factorial(0))  # 1
```

Here's what actually happens when you call `factorial(5)`:

```
factorial(5)
  → 5 * factorial(4)
    → 4 * factorial(3)
      → 3 * factorial(2)
        → 2 * factorial(1)
          → 1           ← base case reached, start returning
        ← 2 * 1 = 2
      ← 3 * 2 = 6
    ← 4 * 6 = 24
  ← 5 * 24 = 120
```

Each call waits for the next one to finish. When the base case finally returns, the answers cascade back up. This is called the **call stack**.

---

## Tracing With Print — See It Unfold

```python
def factorial(n, depth=0):
    indent = "  " * depth
    print(f"{indent}→ factorial({n})")
    if n <= 1:
        print(f"{indent}← 1 (base case)")
        return 1
    result = n * factorial(n - 1, depth + 1)
    print(f"{indent}← {result}")
    return result

factorial(4)
```

Output:
```
→ factorial(4)
  → factorial(3)
    → factorial(2)
      → factorial(1)
      ← 1 (base case)
    ← 2
  ← 6
← 24
```

You can literally see the stack build up (going deeper) then unwind (coming back). That's the heart of recursion.

---

## Recursion vs Loops

**Anything you can do with recursion, you can do with a loop. And vice versa.**

```python
# Loop version
def factorial_loop(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Recursive version
def factorial_recursive(n):
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)
```

So why use recursion? Because **some problems are naturally recursive**. Try writing a loop for a tree structure, or a nested folder search, or something like the example below.

---

## When Recursion Shines: Nested Structures

```python
# Nested folders (a tree)
filesystem = {
    "home": {
        "sonnia": {
            "hello.py": "print('hi')",
            "projects": {
                "python": {
                    "lesson.md": "# Python"
                }
            }
        },
        "arthur": {}
    },
    "etc": {
        "config": {
            "settings.txt": "theme=dark"
        }
    }
}

def find_deepest(directory, depth=0):
    """Find the deepest nested subdirectory."""
    max_depth = depth
    deepest_name = "."
    for name, contents in directory.items():
        if isinstance(contents, dict):
            sub_depth, sub_name = find_deepest(contents, depth + 1)
            if sub_depth > max_depth:
                max_depth = sub_depth
                deepest_name = f"{name}/{sub_name}"
    return max_depth, deepest_name

depth, name = find_deepest(filesystem)
print(f"Deepest: {name} (depth {depth})")
# Deepest: home/sonnia/projects/python (depth 3)
```

Try writing this with a loop. It's possible, but it's much messier — you'd need to manually manage a stack. Recursion handles the stack for you.

---

## The Recursion Limit

Python limits recursion depth (default: 1000). You can check and raise it, but if you're hitting the limit, a loop is usually the better choice:

```python
import sys
print(sys.getrecursionlimit())  # 1000

# You CAN raise it:
sys.setrecursionlimit(5000)
```

But really, if you need 5000 levels of recursion, you're using the wrong tool.

---

## Practice: Sum a Nested List

**Your task:** Write a recursive function `nested_sum` that takes a list that may contain numbers OR other lists (nested arbitrarily deep) and returns the sum of all numbers.

```python
def nested_sum(items):
    # Your code here


print(nested_sum([1, 2, 3]))                  # 6
print(nested_sum([1, [2, [3, 4], 5], 6]))     # 21
print(nested_sum([[[[1]]], [[2]], [3], 4]))   # 10
print(nested_sum([]))                         # 0
```

Hints:
- Use `isinstance(x, list)` to check if an element is a list or a number
- Remember: you can add a number and a recursive result together

Save as `nested_sum.py` and try it!

---

## Solution

```python
def nested_sum(items):
    total = 0
    for item in items:
        if isinstance(item, list):
            total += nested_sum(item)  # Recurse into the sublist
        else:
            total += item  # It's a number — add it
    return total


print(nested_sum([1, 2, 3]))               # 6
print(nested_sum([1, [2, [3, 4], 5], 6]))  # 21
print(nested_sum([[[[1]]], [[2]], [3], 4]))  # 10
print(nested_sum([]))                      # 0
```

That's it. 8 lines. The function handles ANY depth of nesting — 2 levels, 10 levels, whatever. That's the power of recursion.

---

## What You Just Learned

- **Recursion** = a function that calls itself
- **Base case** = when to stop (without it → infinite recursion 💥)
- **Recursive case** = how to get closer to the base case
- **Call stack** = the chain of waiting recursive calls, building up and unwinding
- Some problems (trees, nested structures) are naturally recursive

---

## What's Next?

Recursion and linked lists go hand in hand — linked lists are naturally recursive data structures.

Next up: **[Lesson 18: Linked Lists](18-linked-lists.md)** — data that points to data that points to data... ⛓️

---

**One step at a time.** If recursion feels weird, that's normal — it's probably the most counterintuitive idea in programming. Give it a couple of exercises and it'll click. 💛
