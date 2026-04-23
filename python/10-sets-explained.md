# Python Lesson 10: Sets — Unique Items Only 🎯

**← Back to [Lesson 9: Advanced Dictionaries Practice](09-dictionaries-practice.md)**

---

## What is a Set?

**Plain English:** A set is like a bag of **unique** items. The golden rule: **no duplicates allowed!**

**Real-world analogy:** Think of a collection of different coloured marbles — you can't have two identical marbles in the same bag. If you try to add a duplicate, it's simply ignored!

Or a deck of cards — you only have one Ace of Spades in a standard deck.

---

## Why Use Sets?

**Main use cases:**
1. **Remove duplicates** from a list
2. **Check membership** quickly (is this item in the set?)
3. **Mathematical operations** (union, intersection, difference)

---

## Creating a Set

### Method 1: Using Curly Braces

```python
# Create a set with some fruits
fruits = {'apple', 'banana', 'orange', 'apple'}
print(fruits)
# Output: {'apple', 'banana', 'orange'}
# Notice: 'apple' appears only once!
```

### Method 2: Using the `set()` Constructor

```python
# Convert a list to a set (removes duplicates!)
numbers = set([1, 2, 3, 3, 4, 4, 5])
print(numbers)
# Output: {1, 2, 3, 4, 5}
# Duplicates removed automatically!
```

### Creating an Empty Set

```python
# WRONG! This creates an empty dictionary, not a set!
empty = {}
print(type(empty))  # Output: <class 'dict'>

# CORRECT! Use set() for empty sets
empty = set()
print(type(empty))  # Output: <class 'set'>
```

**Important:** `{}` creates an empty dictionary, not a set! Use `set()` for empty sets.

---

## Basic Set Operations

### Adding Items

```python
# Create a set of colours
colours = {'red', 'blue', 'green'}

# Add a single item
colours.add('yellow')
print(colours)  # Output: {'red', 'blue', 'green', 'yellow'}

# Try adding the same item again (nothing happens!)
colours.add('red')
print(colours)  # Still {'red', 'blue', 'green', 'yellow'}
# No error, just ignored!
```

### Removing Items

```python
colours = {'red', 'blue', 'green', 'yellow'}

# Method 1: .remove() - removes the item
colours.remove('blue')
print(colours)  # Output: {'red', 'green', 'yellow'}

# But what if the item doesn't exist?
# colours.remove('purple')  # ERROR! KeyError: 'purple'

# Method 2: .discard() - removes if exists, no error if not
colours.discard('green')
print(colours)  # Output: {'red', 'yellow'}

# Safe to call even if item doesn't exist
colours.discard('purple')  # No error!
print(colours)  # Still {'red', 'yellow'}
```

**Key difference:**
- `.remove()` — crashes if item doesn't exist
- `.discard()` — safe, no error if item doesn't exist

### `.pop()` — Remove a Random Item

```python
colours = {'red', 'blue', 'green', 'yellow'}

# Remove and return a random item
removed = colours.pop()
print(f"Removed: {removed}")
print(f"Remaining: {colours}")
```

**Note:** Sets are unordered, so you can't predict which item `.pop()` will remove!

### `.clear()` — Empty the Set

```python
colours = {'red', 'blue', 'green'}
colours.clear()
print(colours)  # Output: set()
```

---

## Checking Membership

Use the `in` keyword:

```python
fruits = {'apple', 'banana', 'orange'}

print('apple' in fruits)    # Output: True
print('grape' in fruits)    # Output: False

# Useful in if statements
if 'banana' in fruits:
    print("Yes, we have bananas!")
```

---

## Set Length

```python
fruits = {'apple', 'banana', 'orange'}
print(len(fruits))  # Output: 3
```

---

## Set Mathematics (The Cool Part! 🎨)

Sets can do mathematical operations like union, intersection, and difference!

### Union — All Items from Both Sets

```python
set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}

# Method 1: Using | operator
union = set_a | set_b
print(union)  # Output: {1, 2, 3, 4, 5, 6, 7, 8}

# Method 2: Using .union() method
union = set_a.union(set_b)
print(union)  # Output: {1, 2, 3, 4, 5, 6, 7, 8}
```

**Visual:** Everything from both sets combined (no duplicates).

---

### Intersection — Items in BOTH Sets

```python
set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}

# Method 1: Using & operator
intersection = set_a & set_b
print(intersection)  # Output: {4, 5}

# Method 2: Using .intersection() method
intersection = set_a.intersection(set_b)
print(intersection)  # Output: {4, 5}
```

**Visual:** Only the overlapping part (items that appear in both sets).

---

### Difference — Items in One Set But NOT the Other

```python
set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}

# Method 1: Using - operator
difference = set_a - set_b
print(difference)  # Output: {1, 2, 3}

# Method 2: Using .difference() method
difference = set_a.difference(set_b)
print(difference)  # Output: {1, 2, 3}

# Reverse: items in set_b but NOT in set_a
difference_reverse = set_b - set_a
print(difference_reverse)  # Output: {6, 7, 8}
```

**Visual:** What's left after removing the overlapping part.

---

### Symmetric Difference — Items in EITHER Set, But NOT BOTH

```python
set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}

# Method 1: Using ^ operator
sym_diff = set_a ^ set_b
print(sym_diff)  # Output: {1, 2, 3, 6, 7, 8}

# Method 2: Using .symmetric_difference() method
sym_diff = set_a.symmetric_difference(set_b)
print(sym_diff)  # Output: {1, 2, 3, 6, 7, 8}
```

**Visual:** Everything except the overlapping part.

---

## Real-World Examples

### Example 1: Remove Duplicates from a List

```python
# List of email addresses with duplicates
emails = [
    'alice@example.com',
    'bob@example.com',
    'alice@example.com',
    'charlie@example.com',
    'bob@example.com'
]

# Convert to set to remove duplicates
unique_emails = set(emails)
print(unique_emails)
# Output: {'alice@example.com', 'bob@example.com', 'charlie@example.com'}

# Convert back to list if needed
unique_list = list(unique_emails)
print(unique_list)
```

---

### Example 2: Find Common Friends

```python
# Two people's friend lists
friends_alice = {'Bob', 'Charlie', 'David', 'Eve'}
friends_bob = {'Charlie', 'Eve', 'Frank', 'Grace'}

# Find common friends (intersection)
common_friends = friends_alice & friends_bob
print(f"Common friends: {common_friends}")
# Output: Common friends: {'Charlie', 'Eve'}
```

---

### Example 3: Combine Collections Without Duplicates

```python
# Two stamp collections
collection_1 = {'UK', 'USA', 'France', 'Germany'}
collection_2 = {'France', 'Italy', 'Spain', 'UK'}

# Combine both collections (union)
full_collection = collection_1 | collection_2
print(f"Complete collection: {full_collection}")
# Output: Complete collection: {'UK', 'USA', 'France', 'Germany', 'Italy', 'Spain'}
```

---

### Example 4: Find What's Missing

```python
# Complete set of required skills
required = {'Python', 'SQL', 'JavaScript', 'HTML', 'CSS'}

# Your current skills
your_skills = {'Python', 'HTML', 'CSS'}

# Find missing skills (difference)
missing = required - your_skills
print(f"Skills to learn: {missing}")
# Output: Skills to learn: {'SQL', 'JavaScript'}
```

---

## Practice Exercises

### Exercise 1: Remove Duplicates

You have a list of email addresses with some duplicates. Use a set to remove them!

```python
emails = ['alice@example.com', 'bob@example.com', 'alice@example.com', 'charlie@example.com', 'bob@example.com']

# Your code here: convert to set and back to list
unique_emails = ...
print(unique_emails)
```

---

### Exercise 2: Find Common Friends

Two people have friend lists. Find who they have in common!

```python
friends_alice = {'Bob', 'Charlie', 'David', 'Eve'}
friends_bob = {'Charlie', 'Eve', 'Frank', 'Grace'}

# Your code here: find intersection
common_friends = ...
print(common_friends)
```

---

### Exercise 3: Combine Collections

You have two stamp collections. Combine them without duplicates!

```python
collection_1 = {'UK', 'USA', 'France', 'Germany'}
collection_2 = {'France', 'Italy', 'Spain', 'UK'}

# Your code here: find union
full_collection = ...
print(full_collection)
```

---

### Exercise 4: Find Missing Items

```python
# All required ingredients for a recipe
required = {'flour', 'sugar', 'eggs', 'butter', 'milk'}

# What you have in the kitchen
have = {'flour', 'eggs', 'milk'}

# Find what's missing
missing = ...
print(f"Need to buy: {missing}")
```

---

### Exercise 5: Create Your Own Set

Create a set of your favourite movies, books, or songs. Then:
1. Add a new item
2. Remove an item
3. Check if a specific item exists
4. Print the final set

---

## Quick Recap

- **Sets** store **unique items** only (no duplicates!)
- Create with `{item1, item2, ...}` or `set()`
- **Empty set:** `set()` (NOT `{}` which is a dict!)
- **`.add()`** — add an item
- **`.remove()`** — remove an item (errors if not found)
- **`.discard()`** — remove an item (safe, no error)
- **`.pop()`** — remove a random item
- **`.clear()`** — empty the set
- **`in`** — check if item exists
- **`|`** or **`.union()`** — combine both sets
- **`&`** or **`.intersection()`** — items in both sets
- **`-`** or **`.difference()`** — items in one set but not the other
- **`^`** or **`.symmetric_difference()`** — items in either set but not both

---

## What's Next?

Lesson 11 will cover **File Handling** — how to read from and write to files on your computer! This is essential for working with real data. 📁

---

**Your turn:** Try the exercises above! Sets are super useful for data cleaning and comparison tasks. Ask if you get stuck! 💛🌞
