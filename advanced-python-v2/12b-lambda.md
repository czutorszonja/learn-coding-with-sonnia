# Lesson 12b: Lambda Functions ⚡

**Companion to [Lesson 12: Functions as First-Class Citizens](12-functions-first-class.md)** — do that one first.

---

## The Problem: A Whole `def` for One Line?

You've written functions like this:

```python
def add_one(x):
    return x + 1

def by_length(word):
    return len(word)

def is_even(n):
    return n % 2 == 0
```

Three lines each — `def`, the body, `return`. And half the time, you only use them once, right where you pass them:

```python
sorted(words, key=by_length)   # by_length only exists for this one line
```

It works. But it feels heavy. You named something, gave it a docstring spot, indented a block… for `return len(word)`.

What if you just wanted to say "here's a tiny function, use it now, forget it after"?

That's exactly what `lambda` is for.

---

## The Idea: A Function Without a Name

`lambda` creates a function in a single expression. No `def`, no name, no indented block, no `return` keyword.

```python
# Traditional function:
def add_one(x):
    return x + 1

# Lambda — same thing:
lambda x: x + 1
```

That's it. `lambda` → parameters → colon → expression. The expression IS the return value — you don't write `return`.

The word "lambda" is borrowed from maths (λ-calculus, 1930s), but you don't need the history — just think "quick function."

---

## Lambda Syntax, Piece by Piece

```
lambda  parameters  :  expression
  ↑         ↑       ↑       ↑
keyword   what     colon   the result
          goes in           (no 'return' needed)
```

The expression can only be **one line**. No `if` blocks, no loops, no multiple statements. If your logic needs more than one line, use `def`.

```python
# These three are EXACTLY equivalent:

# Version 1: Traditional
def double(x):
    return x * 2

# Version 2: Lambda, assigned to a variable
double = lambda x: x * 2

# Version 3: Using it anonymously (more common)
result = (lambda x: x * 2)(5)  # 10 — called immediately
```

Version 2 works but is considered bad style — if you're naming it anyway, use `def`. Lambda's superpower is **anonymity** — using it without ever giving it a name.

---

## Step by Step: Where Lambda Shines

### Part 1: As a `key` for `sorted()`

The most common place you'll see lambda. You need to tell `sorted()` HOW to sort — what value to compare:

```python
students = [
    {"name": "Szonja", "score": 92},
    {"name": "Arthur", "score": 87},
    {"name": "Cece",   "score": 95},
]

# Sort by score (ascending):
by_score = sorted(students, key=lambda student: student["score"])
print([s["name"] for s in by_score])
# ['Arthur', 'Szonja', 'Cece']

# Sort by name length:
by_name_len = sorted(students, key=lambda student: len(student["name"]))
print([s["name"] for s in by_name_len])
# ['Cece', 'Szonja', 'Arthur']
```

Without lambda, you'd write three-line `def` functions for each key. With lambda, the sorting rule lives right next to the data — you can read it in one glance.

### Part 2: With `map()` — Transform Every Item

`map(func, iterable)` applies `func` to every element. Lambda makes it clean:

```python
numbers = [1, 2, 3, 4, 5]

squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

halved = list(map(lambda x: x / 2, numbers))
print(halved)   # [0.5, 1.0, 1.5, 2.0, 2.5]
```

### Part 3: With `filter()` — Keep Only What Matches

`filter(func, iterable)` keeps items where `func` returns `True`:

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6, 8, 10]

big = list(filter(lambda x: x > 5, numbers))
print(big)    # [6, 7, 8, 9, 10]
```

### Part 4: Multiple Parameters

Lambda can take as many parameters as you need:

```python
# Two parameters:
add = lambda a, b: a + b
print(add(3, 4))  # 7

# Three parameters:
average = lambda a, b, c: (a + b + c) / 3
print(average(10, 20, 30))  # 20.0

# No parameters (rare but valid):
get_pi = lambda: 3.14159
print(get_pi())  # 3.14159
```

### Part 5: Conditional Expressions Inside Lambda

You CAN have a one-line `if/else` — the ternary expression:

```python
# "positive" if x > 0 else "not positive"
label = lambda x: "positive" if x > 0 else "not positive"

print(label(10))   # positive
print(label(-5))   # not positive
print(label(0))    # not positive

# More practical: grade classifier
grade = lambda score: "pass" if score >= 50 else "fail"
print(grade(72))   # pass
print(grade(33))   # fail
```

The syntax is: `value_if_true if condition else value_if_false`

This is different from a normal `if` statement — it's an **expression** that evaluates to a value. That's why lambda can use it.

---

## Lambda vs `def`: The Rule

| Situation | Use |
|-----------|-----|
| One expression, passed to another function | `lambda` ✅ |
| Logic fits in one line, only used once | `lambda` ✅ |
| Multiple lines of logic | `def` ✅ |
| You're assigning it to a variable | `def` ✅ |
| Needs a docstring or clear name | `def` ✅ |
| Nested inside another function as a quick helper | Either — taste |

A good smell test: **if you're typing `=` after a lambda, use `def` instead.** The whole point of lambda is that you DON'T name it:

```python
# ❌ Bad — just use def
double = lambda x: x * 2

# ✅ Good — lambda used anonymously
sorted(words, key=lambda w: len(w))

# ✅ Also good — def when naming
def double(x):
    return x * 2
```

---

## Common Beginner Confusions

### "Where's the `return`?"

Lambda expressions **automatically return** their result. You never write `return`:

```python
lambda x: x * 2        # Implicitly returns x * 2
# NOT: lambda x: return x * 2   ← ERROR
```

### "Can I use `print()` inside lambda?"

Technically yes, but don't. Lambda is for computing a value, not for side effects:

```python
# ❌ Weird — lambda calls print() which returns None
weird = lambda x: print(x)

# ✅ Just use the print function directly if that's what you want
```

### "Why does my lambda with `if` fail?"

You probably used a statement instead of an expression:

```python
# ❌ WRONG — if/elif/else blocks are statements, not expressions
lambda x: if x > 0: "positive" else: "negative"

# ✅ RIGHT — the ternary conditional expression
lambda x: "positive" if x > 0 else "negative"
```

---

## Practice: Quick Data Transformations

**Your task:** You're cleaning up a list of product prices. Write lambda-powered transformations for each step. No `def` allowed — use `map()`, `filter()`, and `sorted()` with lambdas.

```python
prices = [4.99, 19.99, 0.50, 24.95, 9.99, 100.00, 14.99]

# Step 1: Round every price to the nearest whole number
#         (use map + lambda)
# Your code:
rounded = ...

# Step 2: Keep only prices that are £10 and above
#          (use filter + lambda)
# Your code:
affordable = ...

# Step 3: Sort the remaining prices from cheapest to most expensive
#         (use sorted + lambda)
# Your code:
sorted_prices = ...

# Step 4: Add 20% VAT to every price
#         (use map + lambda)
# Your code:
with_vat = ...

print("Step 1 - Rounded:", rounded)
print("Step 2 - £10+:", affordable)
print("Step 3 - Sorted:", sorted_prices)
print("Step 4 - +VAT:", with_vat)
```

**Expected output:**
```
Step 1 - Rounded: [5, 20, 0, 25, 10, 100, 15]
Step 2 - £10+: [20, 25, 100, 15]
Step 3 - Sorted: [15, 20, 25, 100]
Step 4 - +VAT: [18.0, 24.0, 30.0, 120.0]
```

**Think about it:**
- `map()` transforms each item: `map(transformation, list)`
- `filter()` keeps items: `filter(condition, list)`
- `sorted()` orders items: `sorted(list, key=sort_rule)`
- Each lambda should be ONE expression — the transformation, condition, or sort key

Save as `lambda_shop.py` and try it!

---

## Solution

```python
prices = [4.99, 19.99, 0.50, 24.95, 9.99, 100.00, 14.99]

# Step 1: Round to whole numbers
rounded = list(map(lambda p: round(p), prices))

# Step 2: Keep £10 and above
affordable = list(filter(lambda p: p >= 10, rounded))

# Step 3: Sort cheapest first
sorted_prices = sorted(affordable, key=lambda p: p)

# Step 4: Add 20% VAT
with_vat = list(map(lambda p: p * 1.2, sorted_prices))

print("Step 1 - Rounded:", rounded)
print("Step 2 - £10+:", affordable)
print("Step 3 - Sorted:", sorted_prices)
print("Step 4 - +VAT:", with_vat)
```

Notice how each step reads almost like English: "map round to prices," "filter prices >= 10," "sorted by the price itself," "map multiply by 1.2." Lambda keeps the intent visible without burying it in named helper functions.

**One gotcha:** `round(4.99)` returns `5` in Python. `round(0.50)` returns `0` (banker's rounding — .5 rounds to the nearest even number). If you expected `1`, use `lambda p: int(p + 0.5)` instead.

---

## Bonus: Lambda in the Real World

Here are patterns you'll actually encounter:

```python
# GUI programming — button callbacks
button.on_click(lambda: print("Clicked!"))

# Web frameworks — route handlers
app.route("/hello")(lambda: "Hello, world!")

# Data analysis — pandas transformations
df["name_length"] = df["name"].apply(lambda x: len(x))

# Game programming — sorting game objects by distance
enemies.sort(key=lambda e: distance(player, e))

# API responses — extracting a field from every item
usernames = list(map(lambda u: u["login"], api_response["users"]))
```

Each of these is a one-line idea. Lambda lets you express it without ceremony.

---

## What You Just Learned

- **Lambda** = anonymous one-expression function: `lambda x: x * 2`
- **No `return`** — the expression IS the return value
- **Use it** for `sorted(key=...)`, `map()`, `filter()` — one-liners passed to other functions
- **Don't name it** — `f = lambda x: ...` defeats the purpose; use `def` instead
- **Conditional inside lambda** uses the ternary expression: `x if condition else y`
- **Can take any number of parameters:** `lambda a, b: a + b`
- **Rule of thumb:** if it fits in one expression and you're passing it somewhere, lambda. Otherwise, `def`.

---

## What's Next?

Lambda is a tool, not a topic on its own — it's the punctuation of higher-order functions. Now that you have it:

- Continue to **[Lesson 13: Linked Lists](13-linked-lists.md)**
- Or practice with **[Lesson 20: Sorting](20-sorting.md)** — every custom sort key is a lambda waiting to happen

---

**Your turn:** Run the price transformations! Then try this: given `names = ["Szonja", "Arthur", "Cece", "Alex", "Zoe"]`, use `sorted()` with a lambda to sort them by the LAST letter of each name. (Hint: `name[-1]`.) ⚡💛
