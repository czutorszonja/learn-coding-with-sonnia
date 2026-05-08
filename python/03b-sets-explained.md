# Python Lesson 3b: Sets — When Order Doesn't Matter

**← Back to [Lesson 3: Lists](03-lists-explained.md)**

---

## What is a Set?

**Plain English:** A set is like a list, but it **automatically removes duplicates** and items have **no fixed order**.

**Real-world analogy:** Think of a guest list for a party. You only care about *who* is coming, not *how many times* they said they'd attend. If Arthur says he'll come twice, he's still just one person on the list.

```python
# List — keeps duplicates, remembers order
names_list = ["Szonja", "Arthur", "Emma", "Szonja", "Arthur"]
print(names_list)  # ['Szonja', 'Arthur', 'Emma', 'Szonja', 'Arthur']

# Set — removes duplicates automatically
names_set = {"Szonja", "Arthur", "Emma", "Szonja", "Arthur"}
print(names_set)  # {'Szonja', 'Arthur', 'Emma'}
```

The moment `"Szonja"` appeared twice in the set, Python silently dropped the duplicate. Useful, right?

---

## Creating a Set

Sets use **curly braces** `{ }` (like dictionaries — but without the key:value pairs):

```python
# A set of strings
languages = {"Python", "JavaScript", "Rust"}

# A set of numbers
scores = {95, 87, 92, 95}   # 95 appears twice — set keeps only one
print(scores)  # {87, 92, 95}

# An empty set — careful!
empty_list = []           # easy, obvious
empty_set = set()         # {} makes an empty DICT, not a set!
print(empty_set)          # set()
```

---

## The Three Key Differences from Lists

### 1. No duplicates
```python
votes = ["yes", "no", "yes", "yes", "abstain"]
unique_votes = set(votes)
print(unique_votes)  # {'yes', 'no', 'abstain'}
```
Great for: counting unique items, removing duplicates from a list.

### 2. No specific order
```python
fruits = {"apple", "banana", "cherry"}
print(fruits)  # Could output in any order — {'apple', 'banana', 'cherry'}
```
Sets are **unordered** — you can't rely on `fruits[0]` returning `"apple"`. If you need order, use a list!

### 3. Membership testing is much faster
```python
allowed_users = {"alice", "bob", "carol"}   # 1,000,000 users? Still fast!
# Checking if "alice" is in allowed_users is instant.

if "alice" in allowed_users:
    print("Access granted")
```
This is called **O(1) lookup** — the time it takes doesn't increase as the set gets bigger. With a list, Python has to check every single item one by one (O(n)). For large datasets, this is a huge difference.

---

## Set Operations — The Really Useful Part

Sets shine when you need to compare groups. Think of it like Venn diagrams.

### Union — Everything in either set (OR)
```python
python_class = {"Szonja", "Arthur", "Emma", "David"}
javascript_class = {"Arthur", "Emma", "Fiona", "George"}

# Union — everyone in at least one class
both = python_class | javascript_class
# OR: python_class.union(javascript_class)
print(both)  # {'Szonja', 'Arthur', 'Emma', 'David', 'Fiona', 'George'}
```

### Intersection — In BOTH sets (AND)
```python
# Students taking BOTH classes
both_classes = python_class & javascript_class
# OR: python_class.intersection(javascript_class)
print(both_classes)  # {'Arthur', 'Emma'}
```

### Difference — In one set but NOT the other
```python
# Students in Python but NOT in JavaScript
python_only = python_class - javascript_class
# OR: python_class.difference(javascript_class)
print(python_only)  # {'Szonja', 'David'}

# Students in JavaScript but NOT in Python
javascript_only = javascript_class - python_class
print(javascript_only)  # {'Fiona', 'George'}
```

### Symmetric Difference — In one OR the other, but NOT both
```python
# Students in exactly one class (not both)
one_class = python_class ^ javascript_class
# OR: python_class.symmetric_difference(javascript_class)
print(one_class)  # {'Szonja', 'David', 'Fiona', 'George'}
```

---

## Checking Relationships

### `issubset` — Is every item in A also in B?
```python
small = {1, 2, 3}
medium = {1, 2, 3, 4, 5}

print(small.issubset(medium))  # True — all of small is in medium
print(medium.issubset(small))  # False — medium has more items
```

### `issuperset` — Does A contain every item in B?
```python
print(medium.issuperset(small))  # True — medium has everything in small
print(small.issuperset(medium))  # False
```

### `isdisjoint` — Do they share NO items?
```python
even = {2, 4, 6, 8}
odd = {1, 3, 5, 7}
print(odd.isdisjoint(even))  # True — no overlap!
```

---

## When to Use Sets (and When Not To)

**Use a set when:**
- You need **unique values** and don't care about order
- You're comparing groups (union, intersection, difference)
- You're checking if something exists in a large collection — it's much faster than a list
- You want to **de-duplicate** a list quickly

**Stick with a list when:**
- You need things in a **specific order**
- You need to **access by index** (`mylist[0]`)
- You need **duplicates to be preserved**
- You're doing simple membership checks on small collections where speed doesn't matter

---

## Converting Between Lists and Sets

```python
# List → Set (remove duplicates, lose order)
names_list = ["Szonja", "Arthur", "Emma", "Szonja"]
unique_names = set(names_list)
print(unique_names)  # {'Szonja', 'Arthur', 'Emma'}

# Set → List (preserve items, lose order, lose duplicates)
back_to_list = list(unique_names)
print(back_to_list)  # ['Szonja', 'Arthur', 'Emma']

# Common pattern: get unique items from a list
grades = [85, 92, 85, 90, 92, 88, 85]
unique_grades = set(grades)
print(unique_grades)  # {85, 92, 90, 88}
print(f"There are {len(unique_grades)} unique grades: {unique_grades}")
```

---

## Adding and Removing Items

```python
team = set()

# Add one item
team.add("Alice")
print(team)  # {'Alice'}

# Add multiple items
team.update(["Bob", "Carol"])   # Note: update(), not .add() for a list
print(team)  # {'Alice', 'Bob', 'Carol'}

# Remove an item
team.remove("Bob")              # Raises an error if "Bob" isn't there
print(team)  # {'Alice', 'Carol'}

# Remove safely (won't error if missing)
team.discard("Dave")            # Does nothing if "Dave" not in set
print(team)  # {'Alice', 'Carol'}

# Copy a set
team_copy = team.copy()
print(team_copy)  # {'Alice', 'Carol'}
```

---

## Practice Exercise

**Scenario:** You've just finished a Python course with two classes.

Class A: `"Alice", "Bob", "Carol", "David", "Emma"`
Class B: `"Carol", "David", "Emma", "Fiona", "George"`

1. Create two sets, `class_a` and `class_b`
2. Print the names of all students who took **either** class (union)
3. Print the names of students who took **both** classes (intersection)
4. Print the names of students who were in **Class A only** (difference)
5. Print how many **unique** students there were across both classes (len of union)
6. **Challenge:** A third class, `class_c`, had these students: `"Emma", "Fiona", "George", "Helen"`. Find all students who took exactly ONE of the three classes (symmetric difference of A and B, then remove any who are also in C).
7. **Challenge 2 (exam style!):** Write a function `has_unique_letters(word1, word2)` that returns `True` if the two words share **no letters at all**. Hint: `set(word1)` gives you the set of its letters.

**Try it yourself first!** Scroll down when ready.

---

## Solution

```python
# Create the two class sets
class_a = {"Alice", "Bob", "Carol", "David", "Emma"}
class_b = {"Carol", "David", "Emma", "Fiona", "George"}

# All students in either class (union)
print("Union:", class_a | class_b)
# Output: {'Alice', 'Bob', 'Carol', 'David', 'Emma', 'Fiona', 'George'}

# Students in both classes (intersection)
print("Both classes:", class_a & class_b)
# Output: {'Carol', 'David', 'Emma'}

# Students in Class A only (difference)
print("Class A only:", class_a - class_b)
# Output: {'Alice', 'Bob'}

# Total unique students
print(f"Unique students: {len(class_a | class_b)}")
# Output: 7

# Challenge: exactly one of three classes
class_c = {"Emma", "Fiona", "George", "Helen"}
ab_only = class_a ^ class_b            # in A or B, but not both
exactly_one = ab_only - class_c        # remove those also in C
print("Exactly one of three:", exactly_one)
# Output: {'Alice', 'Bob', 'Helen'}

# Challenge 2: no shared letters
def has_unique_letters(word1, word2):
    set1 = set(word1.lower())
    set2 = set(word2.lower())
    return len(set1 & set2) == 0       # intersection should be empty

print(has_unique_letters("hello", "world"))  # True  — no shared letters
print(has_unique_letters("hello", "oliver")) # False — 'o', 'l' overlap
```

---

## Quick Recap

| Symbol | Method | Meaning |
|--------|--------|---------|
| `{ }` | `set()` | Create a set — `{}` makes a dict, `set()` makes an empty set |
| `a \| b` | `a.union(b)` | All items in A **or** B |
| `a & b` | `a.intersection(b)` | All items in A **and** B |
| `a - b` | `a.difference(b)` | Items in A **but not** in B |
| `a ^ b` | `a.symmetric_difference(b)` | Items in A **or** B, **but not** both |
| `.add(x)` | — | Add one item |
| `.update([x, y])` | — | Add multiple items from a list |
| `.remove(x)` | — | Remove item (errors if not there) |
| `.discard(x)` | — | Remove item (silent if not there) |
| `a.issubset(b)` | — | `True` if all of A is in B |
| `a.issuperset(b)` | — | `True` if A contains all of B |
| `a.isdisjoint(b)` | — | `True` if A and B share nothing |

- Sets **automatically remove duplicates**
- Sets have **no guaranteed order** (don't use indexes on sets!)
- Checking `x in myset` is **much faster** than `x in mylist` for large collections
- Convert to/from a list with `set(mylist)` and `list(myset)`

---

## What's Next?

Sets are the perfect data structure when you need to compare groups or find unique items. Now let's learn how to repeat actions automatically — **[Lesson 4: Loops Explained](04-loops-explained.md)**! 🚀

---