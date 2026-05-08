# Python Lesson 4: Loops — Doing Things Over and Over

**← Back to [Lesson 3: Lists](03-lists-explained.md)**

---

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

## Looping With Index Numbers: `range(len())`

Sometimes you need **both** the index (position) **and** the item itself. `range(len())` gives you index numbers you can use:

```python
fruits = ["apple", "banana", "cherry"]

for i in range(len(fruits)):
    print(f"Index {i}: {fruits[i]}")

# Output:
# Index 0: apple
# Index 1: banana
# Index 2: cherry
```

**When is this useful?** When you need to look at the previous or next item, or when you need the index number for some other purpose:

```python
# Find where a target value is
names = ["Alice", "Bob", "Charlie", "Dave"]
target = "Charlie"

for i in range(len(names)):
    if names[i] == target:
        print(f"Found at index {i}")
        break

# Output: Found at index 2
```

**Tip — When to use `enumerate()` vs `range(len())`:**
- Use `enumerate()` when you want both index and value neatly together: `for i, item in enumerate(list):`
- Use `range(len())` when you only need the index, or when you need to also modify items in the list by index

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

## Controlling Loops: `break` and `continue`

Sometimes you want more control over your loops!

### `break` — Exit the loop early

Use `break` to stop the loop immediately:

```python
# Search for a number
numbers = [1, 3, 5, 7, 9, 11]

for num in numbers:
    if num == 7:
        print("Found 7!")
        break  # Stop the loop!
    print(f"Checking: {num}")

# Output:
# Checking: 1
# Checking: 3
# Checking: 5
# Found 7!
```

**Why use `break`?** Once we found 7, there's no need to check the rest!

### `continue` — Skip to the next iteration

Use `continue` to skip the rest of the current iteration and move to the next:

```python
# Print only odd numbers
numbers = [1, 2, 3, 4, 5]

for num in numbers:
    if num % 2 == 0:  # If even
        continue  # Skip this number
    print(num)

# Output:
# 1
# 3
# 5
```

**Why use `continue`?** We skip even numbers and only print odd ones!

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


## Building a New List Inside a Loop

This is one of the most useful patterns you'll use — and it comes up all the time in exams.

**The idea:** You start with an empty list, then loop through some data and add items to it as you go.

### Basic Pattern

```python
# Start with an empty list
doubled = []

numbers = [1, 2, 3, 4, 5]

for n in numbers:
    doubled.append(n * 2)  # append adds to the end of the list

print(doubled)  # [2, 4, 6, 8, 10]
```

**Why not just use a list comprehension?** You can! But a `for` loop with `append` is easier to read when the logic inside the loop is more complicated:

```python
# List comprehension — clean when the logic is simple
squares = [x**2 for x in range(1, 6)]

# For loop — easier when you have conditions
squares = []
for x in range(1, 6):
    if x % 2 == 0:  # only even numbers
        squares.append(x ** 2)
# Result: [4, 16]
```

### Example: Filter a List

```python
# Keep only the passing grades (40 or above)
all_grades = [25, 45, 10, 60, 35, 80]
passing = []

for grade in all_grades:
    if grade >= 40:
        passing.append(grade)

print(passing)  # [45, 60, 80]
```

### Example: Build a List of Strings

```python
# Turn a list of names into greetings
names = ["Arthur", "Szonja", "Mafla"]
greetings = []

for name in names:
    greetings.append(f"Hello, {name}!")

print(greetings)
# ['Hello, Arthur!', 'Hello, Szonja!', 'Hello, Mafla!']
```

### Example: Collect Matching Items

```python
# Find all words that start with a vowel
words = ["apple", "hello", "umbrella", "world", "elephant"]
vowel_words = []

vowels = "aeiouAEIOU"
for word in words:
    if word[0] in vowels:  # check the first letter
        vowel_words.append(word)

print(vowel_words)  # ['apple', 'umbrella', 'elephant']
```

### The Key Takeaway

Whenever you need to **create a new list based on an existing list**, a `for` loop with `append` is your friend. The pattern is always:

```python
new_list = []
for item in old_list:
    new_list.append(do_something_with(item))
```


## Practice Exercise

**Scenario:** You're organizing your bookshelf and want to do several things with it!

1. Create a list called `books` with 5 book titles
2. Use a `for` loop to print each book title with "I love:" in front of it
3. Use `enumerate()` to print each book with its position (Book 1, Book 2, etc.)
4. Use `range()` to print numbers 1 to 10 (inclusive — meaning 10 should be included!)
5. **Challenge:** Create a new list called `long_books` that contains only the books with more than 10 characters in the title. (Hint: use `len(title) > 10` and `append` inside your loop!)

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

# Challenge: build a list of long books (more than 10 characters)
long_books = []
for book in books:
    if len(book) > 10:
        long_books.append(book)

print(f"Long books: {long_books}")
# Long books: ['Pride and Prejudice', 'The Hobbit']
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

## Extra Practice Exercise

Want more practice with for loops? Try this!

### Exercise: Grocery Total 🛒

**Scenario:** You're at the grocery store and want to calculate your total bill!

**Your task:**
1. Create a list called `prices` with 5 item prices (numbers, like 2.50, 5.99, etc.)
2. Create a variable `total` starting at 0
3. Use a `for` loop to go through each price
4. Add each price to the total
5. After the loop, print the total with a nice message (use an f-string!)

**Hint:** To format money to 2 decimal places, use `{total:.2f}` in your f-string!

**Try it yourself first!** Solution below.

---

## Extra Practice Solution

### Grocery Total Solution

```python
prices = [2.50, 5.99, 3.49, 1.99, 7.50]
total = 0

for price in prices:
    total = total + price

print(f"Total bill: £{total:.2f}")
```

**Output:**
```
Total bill: £21.47
```

**Note:** The `:.2f` in the f-string formats the number to 2 decimal places (for pounds and pence)!

---

## Quick Recap

- **`for` loops** repeat code for each item in a list
- **Loop variable** holds the current item (name it something descriptive!)
- **`range()`** creates a sequence of numbers to loop through
- **`range(start, end)`** lets you specify start and end
- **`range(start, end, step)`** lets you skip numbers
- **`range(len())`** gives you index numbers to use with list access
- **`enumerate()`** gives you both index and value
- **Loop + append** — build a new list by adding items inside a loop

---

## What's Next?

Ready for more? Continue to **[Lesson 5: While Loops and Conditionals](05-while-loops-and-conditionals.md)**! 🚀

---

