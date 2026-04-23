# Python Lesson 9: Advanced Dictionaries Practice 🎯

**← Back to [Lesson 8: Dictionaries Explained](08-dictionaries-explained.md)**

---

## Welcome to Dictionary Deep-Dive!

Now you know the basics of dictionaries. Let's level up with more advanced operations and real-world patterns! 💪

---

## Part 1: More Dictionary Methods

### `.pop()` — Remove and Return a Value

The `.pop()` method removes a key and **returns its value**:

```python
person = {"name": "Szonja", "age": 30, "city": "London"}

# Remove 'age' and store the value
removed_age = person.pop("age")

print(removed_age)  # Output: 30
print(person)       # Output: {'name': 'Szonja', 'city': 'London'}
```

**Why use `.pop()` instead of `del`?**
- `del` just removes the item
- `.pop()` removes it AND gives you the value back
- Useful when you need to use the value before removing it

```python
# Real-world example: processing orders
orders = {
    "order_001": "Pizza",
    "order_002": "Pasta",
    "order_003": "Salad"
}

# Process and remove first order
next_order = orders.pop("order_001")
print(f"Now preparing: {next_order}")  # Output: Now preparing: Pizza
print(f"Remaining orders: {orders}")    # Output: {'order_002': 'Pasta', 'order_003': 'Salad'}
```

### `.pop()` with a Default Value

If the key doesn't exist, `.pop()` can return a default instead of crashing:

```python
person = {"name": "Szonja"}

# Key doesn't exist, but we provide a default
age = person.pop("age", "Unknown")
print(age)  # Output: Unknown
print(person)  # Output: {'name': 'Szonja'}
```

---

### `.update()` — Add Multiple Items at Once

Instead of adding keys one by one, use `.update()`:

```python
person = {"name": "Szonja", "age": 30}

# Add multiple key-value pairs
person.update({"city": "London", "job": "Developer", "is_student": True})

print(person)
# Output: {'name': 'Szonja', 'age': 30, 'city': 'London', 'job': 'Developer', 'is_student': True}
```

You can also update existing values:

```python
person = {"name": "Szonja", "age": 30}

# Update age and add city
person.update({"age": 31, "city": "London"})

print(person)  # Output: {'name': 'Szonja', 'age': 31, 'city': 'London'}
```

---

### `.clear()` — Empty the Dictionary

Remove all items at once:

```python
person = {"name": "Szonja", "age": 30, "city": "London"}

person.clear()
print(person)  # Output: {}
```

---

## Part 2: Combining Dictionaries with Lists

Dictionaries become even more powerful when combined with lists!

### List of Dictionaries

Store multiple items (each item is a dictionary):

```python
# A list of students
students = [
    {"name": "Szonja", "age": 30, "city": "London"},
    {"name": "Arthur", "age": 35, "city": "Paris"},
    {"name": "Emma", "age": 28, "city": "Berlin"}
]

# Access the first student
print(students[0])  # Output: {'name': 'Szonja', 'age': 30, 'city': 'London'}

# Access a specific value
print(students[0]["name"])  # Output: Szonja

# Loop through all students
for student in students:
    print(f"{student['name']} lives in {student['city']}")

# Output:
# Szonja lives in London
# Arthur lives in Paris
# Emma lives in Berlin
```

### Dictionary with List Values

Store lists as values inside a dictionary:

```python
# Student with multiple courses
student = {
    "name": "Szonja",
    "courses": ["Python", "SQL", "Data Science"],
    "grades": [85, 90, 78]
}

print(student["name"])      # Output: Szonja
print(student["courses"])   # Output: ['Python', 'SQL', 'Data Science']
print(student["courses"][0])  # Output: Python

# Loop through courses
for course in student["courses"]:
    print(f"Course: {course}")
```

---

## Part 3: Nested Dictionaries

A dictionary inside a dictionary! This is super useful for complex data:

```python
# A company with multiple departments
company = {
    "engineering": {
        "head": "Arthur",
        "budget": 500000,
        "employees": ["Szonja", "Emma", "David"]
    },
    "marketing": {
        "head": "Sarah",
        "budget": 300000,
        "employees": ["John", "Lisa"]
    },
    "sales": {
        "head": "Mike",
        "budget": 400000,
        "employees": ["Tom", "Anna", "Chris"]
    }
}

# Access nested values
print(company["engineering"]["head"])  # Output: Arthur
print(company["marketing"]["budget"])  # Output: 300000

# Loop through departments
for dept, info in company.items():
    print(f"\n{dept}:")
    print(f"  Head: {info['head']}")
    print(f"  Budget: £{info['budget']:,}")
    print(f"  Employees: {', '.join(info['employees'])}")
```

**Output:**
```
engineering:
  Head: Arthur
  Budget: £500,000
  Employees: Szonja, Emma, David

marketing:
  Head: Sarah
  Budget: £300,000
  Employees: John, Lisa

sales:
  Head: Mike
  Budget: £400,000
  Employees: Tom, Anna, Chris
```

---

## Part 4: Real-World Projects

### Project 1: Shopping Cart

Build a simple shopping cart system:

```python
# Shopping cart with items and quantities
cart = {
    "apples": 5,
    "bananas": 3,
    "oranges": 2,
    "milk": 1
}

# Prices for each item
prices = {
    "apples": 0.50,
    "bananas": 0.30,
    "oranges": 0.40,
    "milk": 1.20
}

# Calculate total
total = 0
for item, quantity in cart.items():
    item_total = prices[item] * quantity
    print(f"{item}: {quantity} x £{prices[item]:.2f} = £{item_total:.2f}")
    total += item_total

print(f"\nTotal: £{total:.2f}")
```

**Output:**
```
apples: 5 x £0.50 = £2.50
bananas: 3 x £0.30 = £0.90
oranges: 2 x £0.40 = £0.80
milk: 1 x £1.20 = £1.20

Total: £5.40
```

---

### Project 2: Student Grade Tracker

Track student grades and calculate averages:

```python
# Student grades (nested dictionary)
students = {
    "Szonja": {"math": 85, "science": 90, "english": 78},
    "Arthur": {"math": 92, "science": 88, "english": 95},
    "Emma": {"math": 76, "science": 82, "english": 89}
}

# Calculate average for each student
for student, grades in students.items():
    total = sum(grades.values())
    num_subjects = len(grades)
    average = total / num_subjects
    print(f"{student}'s average: {average:.1f}%")
```

**Output:**
```
Szonja's average: 84.3%
Arthur's average: 91.7%
Emma's average: 82.3%
```

---

### Project 3: Contact Book with Search

A contact book where you can search by name:

```python
# Contact database
contacts = {
    "Szonja": {"phone": "07123456789", "email": "szonja@example.com", "city": "London"},
    "Arthur": {"phone": "07987654321", "email": "arthur@example.com", "city": "Paris"},
    "Emma": {"phone": "07555123456", "email": "emma@example.com", "city": "Berlin"}
}

# Search for a contact
search_name = "Arthur"

if search_name in contacts:
    contact = contacts[search_name]
    print(f"Found {search_name}!")
    print(f"  Phone: {contact['phone']}")
    print(f"  Email: {contact['email']}")
    print(f"  City: {contact['city']}")
else:
    print(f"{search_name} not found!")
```

---

## Part 5: Practice Exercises

### Exercise 1: Using `.pop()`

```python
# You have a to-do list dictionary
tasks = {
    "task_1": "Buy groceries",
    "task_2": "Write report",
    "task_3": "Call mum"
}

# Complete and remove task_1
completed = tasks.pop("task_1")
print(f"Completed: {completed}")
print(f"Remaining tasks: {tasks}")
```

---

### Exercise 2: List of Dictionaries

```python
# Create a list of 3 books
# Each book should have: title, author, year, genre
books = [
    # Add your books here
]

# Print all book titles
for book in books:
    print(f"Title: {book['title']} by {book['author']}")
```

---

### Exercise 3: Nested Dictionary

```python
# Create a nested dictionary for a restaurant menu
# Structure: category -> dish name -> price
menu = {
    "starters": {
        "bruschetta": 6.50,
        "calamari": 8.00
    },
    "mains": {
        "pizza": 12.00,
        "pasta": 10.50
    },
    "desserts": {
        "tiramisu": 5.50,
        "gelato": 4.00
    }
}

# Print all main courses and their prices
for dish, price in menu["mains"].items():
    print(f"{dish}: £{price:.2f}")
```

---

### Exercise 4: Build Your Own Project

Create a dictionary-based project of your choice! Ideas:
- Movie collection (title, director, year, rating)
- Recipe book (recipe name, ingredients, cooking time)
- Travel log (country, cities visited, dates)
- Music playlist (song, artist, duration)

---

## Quick Recap

- **`.pop()`** — remove and return a value
- **`.update()`** — add multiple items at once
- **`.clear()`** — empty the dictionary
- **List of dictionaries** — store multiple similar items
- **Dictionary with list values** — store multiple values per key
- **Nested dictionaries** — complex, hierarchical data
- **Real-world patterns** — shopping carts, grade trackers, contact books

---

## What's Next?

Ready for more? Continue to **[Lesson 10: Sets Explained](10-sets-explained.md)**! 🎯

---

**Your turn:** Try the exercises above! Start with Exercise 1 and work your way up. Ask if you get stuck! 💛🌞
