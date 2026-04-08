# Python Lesson 4: Loops — Doing Things Over and Over

## What is a Loop?

**Plain English:** A loop lets you repeat the same code multiple times without writing it over and over.

**Real-world analogy:** Imagine you're handing out flyers to 50 people. You could write:
```python
hand_flyer(person1)
hand_flyer(person2)
hand_flyer(person3)
# ... 47 more times! 😫
```

Or you could use a loop:
```python
for person in people:
    hand_flyer(person)
# Much better! ✨
```

---

## The `for` Loop

A `for` loop goes through each item in a list, one by one:

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)

# Output:
# apple
# banana
# cherry
```

**How it works:**
1. `for fruit in fruits:` — "For each item in the fruits list..."
2. `fruit` is a temporary variable that holds the current item
3. The indented code runs once for each item
4. Python automatically moves to the next item

---

## Loop Variables

You can name the loop variable anything you want:

```python
fruits = ["apple", "banana", "cherry"]

# These all do the same thing:
for fruit in fruits:
    print(fruit)

for item in fruits:
    print(item)

for x in fruits:
    print(x)
```

**Tip:** Use descriptive names like `fruit`, `song`, or `name` — not just `x`. It makes your code easier to understand!

---

## Using f-strings in Loops

You can use f-strings to make nice output:

```python
playlist = ["Yesterday", "Girl", "Bohemian Rhapsody"]

for song in playlist:
    print(f"Now playing: {song}")

# Output:
# Now playing: Yesterday
# Now playing: Girl
# Now playing: Bohemian Rhapsody
```

---

## The `range()` Function

`range()` creates a sequence of numbers for you to loop through:

```python
# Loop 5 times
for i in range(5):
    print(f"Count: {i}")

# Output:
# Count: 0
# Count: 1
# Count: 2
# Count: 3
# Count: 4
```

**Important:** `range(5)` gives you 0, 1, 2, 3, 4 — it starts at 0 and stops *before* 5!

### Custom Range

You can specify start and end:

```python
# Start at 1, end before 6
for i in range(1, 6):
    print(f"Number: {i}")

# Output:
# Number: 1
# Number: 2
# Number: 3
# Number: 4
# Number: 5
```

**Important:** The end number is *exclusive* — `range(1, 6)` gives you 1, 2, 3, 4, 5 (stops BEFORE 6). If you want to include 10, use `range(1, 11)`!

### Range with Steps

You can also skip numbers:

```python
# Start at 0, end before 10, skip by 2
for i in range(0, 10, 2):
    print(f"Even number: {i}")

# Output:
# Even number: 0
# Even number: 2
# Even number: 4
# Even number: 6
# Even number: 8
```

---

## Getting Both Index and Value

Sometimes you need both the position AND the item. Use `enumerate()`:

```python
playlist = ["Yesterday", "Girl", "Bohemian Rhapsody"]

for index, song in enumerate(playlist):
    print(f"Track {index + 1}: {song}")

# Output:
# Track 1: Yesterday
# Track 2: Girl
# Track 3: Bohemian Rhapsody
```

**Why `index + 1`?** Because Python starts counting at 0, but humans usually start at 1!

---

## Practice Exercise

**Scenario:** You're organizing your bookshelf and want to print a catalog!

1. Create a list called `books` with 5 book titles
2. Use a `for` loop to print each book title with "I love:" in front of it
3. Use `enumerate()` to print each book with its position (Book 1, Book 2, etc.)
4. Use `range()` to print numbers 1 to 10 (inclusive — meaning 10 should be included!)

**Try it yourself first!** Scroll down when ready.

---

## Solution

```python
# Create list of books
books = ["1984", "Pride and Prejudice", "The Hobbit", "Dune", "Emma"]

# Print each book with "I love:"
print("My favorite books:")
for book in books:
    print(f"I love: {book}")

# Print with position using enumerate
print("Bookshelf order:")
for index, book in enumerate(books):
    print(f"Book {index + 1}: {book}")

# Print numbers 1-10
print("Counting:")
for i in range(1, 11):  # Remember: end is exclusive, so use 11 to include 10!
    print(i)
```

**Output:**
```
My favorite books:
I love: 1984
I love: Pride and Prejudice
I love: The Hobbit
I love: Dune
I love: Emma

Bookshelf order:
Book 1: 1984
Book 2: Pride and Prejudice
Book 3: The Hobbit
Book 4: Dune
Book 5: Emma

Counting:
1
2
3
4
5
6
7
8
9
10
```

---

## Quick Recap

- **`for` loops** repeat code for each item in a list
- **Loop variable** holds the current item (name it something descriptive!)
- **`range()`** creates a sequence of numbers to loop through
- **`range(start, end)`** lets you specify start and end
- **`range(start, end, step)`** lets you skip numbers
- **`enumerate()`** gives you both index and value

---

## What's Next?

Lesson 5 will cover **`while` loops and conditionals** — looping while a condition is true, and making decisions in your code!

---

**Your turn:** Try the bookshelf exercise! Use your actual favorite books if you want! 📚💛
