# Python Lesson 8: Dictionaries — Key-Value Pairs 📖

**← Back to [Lesson 7: Combined Practice](07-combined-practice.md)**

---

## What is a Dictionary?

**Plain English:** A dictionary stores data as **key-value pairs**. Each key maps to a value.

**Real-world analogy:** Think of a real dictionary (book):
- You look up a **word** (the key)
- You find its **definition** (the value)

Or a contact list on your phone:
- You search for a **name** (the key)
- You get their **phone number** (the value)

---

## Why Use Dictionaries?

**With lists:**
```python
# Storing student info in separate lists
names = ["Szonja", "Arthur", "Emma"]
ages = [30, 35, 28]
cities = ["London", "Paris", "Berlin"]

# Hard to keep track of which index matches which!
print(f"{names[0]} is {ages[0]} and lives in {cities[0]}")
```

**With dictionaries:**
```python
# All info together, clearly labeled!
student = {
    "name": "Szonja",
    "age": 30,
    "city": "London"
}

print(f"{student['name']} is {student['age']} and lives in {student['city']}")
```

Much clearer! 🎯

---

## Creating a Dictionary

Dictionaries use **curly braces** `{ }` with `key: value` pairs:

```python
# Empty dictionary
empty = {}

# Dictionary with data
person = {
    "name": "Szonja",
    "age": 30,
    "city": "London",
    "is_student": True
}
```

**Key rules:**
- Keys must be **unique** (can't have two "name" keys)
- Keys are usually **strings** (but can be numbers or other types)
- Values can be **any type** (strings, numbers, booleans, lists, even other dictionaries!)

---

## Accessing Values

Use square brackets with the **key** (not an index!):

```python
person = {
    "name": "Szonja",
    "age": 30,
    "city": "London"
}

print(person["name"])  # Output: Szonja
print(person["age"])   # Output: 30
print(person["city"])  # Output: London
```

**Important:** You use the **key** to access the value, not a number!

---

## What Happens if the Key Doesn't Exist?

```python
person = {"name": "Szonja", "age": 30}

print(person["city"])  # ERROR! KeyError: 'city'
```

Python will crash with a `KeyError`!

**Solution:** Use the `.get()` method instead:

```python
print(person.get("city"))  # Output: None (no error!)
print(person.get("name"))  # Output: Szonja
```

You can also provide a **default value**:

```python
print(person.get("city", "Unknown"))  # Output: Unknown
```

---

## Adding or Modifying Values

```python
person = {"name": "Szonja", "age": 30}

# Add a new key-value pair
person["city"] = "London"
print(person)  # Output: {'name': 'Szonja', 'age': 30, 'city': 'London'}

# Modify an existing value
person["age"] = 31
print(person)  # Output: {'name': 'Szonja', 'age': 31, 'city': 'London'}
```

---

## Removing Items

Use `del` to remove a key-value pair:

```python
person = {"name": "Szonja", "age": 30, "city": "London"}

del person["city"]
print(person)  # Output: {'name': 'Szonja', 'age': 30}
```

---

## Dictionary Methods

### `.keys()` — Get all keys

```python
person = {"name": "Szonja", "age": 30, "city": "London"}

keys = person.keys()
print(keys)  # Output: dict_keys(['name', 'age', 'city'])

# Loop through keys
for key in person.keys():
    print(key)
# Output:
# name
# age
# city
```

### `.values()` — Get all values

```python
person = {"name": "Szonja", "age": 30, "city": "London"}

values = person.values()
print(values)  # Output: dict_values(['Szonja', 30, 'London'])

# Loop through values
for value in person.values():
    print(value)
# Output:
# Szonja
# 30
# London
```

### `.items()` — Get both keys and values

```python
person = {"name": "Szonja", "age": 30, "city": "London"}

# Loop through both keys and values
for key, value in person.items():
    print(f"{key}: {value}")

# Output:
# name: Szonja
# age: 30
# city: London
```

---

## Checking if a Key Exists

Use the `in` keyword:

```python
person = {"name": "Szonja", "age": 30}

print("name" in person)  # Output: True
print("city" in person)  # Output: False
```

---

## Counting Things: Frequency Maps

A very common pattern: **how many times does each thing appear?** Use a dictionary to count:

```python
# Count how many times each letter appears
text = "hello world"
freq = {}

for char in text:
    if char in freq:
        freq[char] += 1
    else:
        freq[char] = 1

print(freq)  # {'h': 1, 'e': 1, 'l': 3, 'o': 2, ' ': 1, 'w': 1, 'r': 1, 'd': 1}
```

### The `.get()` Shortcut

The `if/else` pattern above can be written more cleanly with `.get()`:

```python
text = "hello world"
freq = {}

for char in text:
    freq[char] = freq.get(char, 0) + 1
    # If char is not in dict yet, .get() returns 0. Then +1 sets it to 1.
    # If char is already there, it adds 1 to the current count.

print(freq)  # {'h': 1, 'e': 1, 'l': 3, 'o': 2, ' ': 1, 'w': 1, 'r': 1, 'd': 1}
```

### Using This to Compare Two Strings (Anagrams)

If two strings are anagrams, they have the same letters with the same counts:

```python
def is_anagram(word1, word2):
    # Build a frequency map for word1
    freq1 = {}
    for char in word1.lower():
        freq1[char] = freq1.get(char, 0) + 1

    # Build a frequency map for word2
    freq2 = {}
    for char in word2.lower():
        freq2[char] = freq2.get(char, 0) + 1

    return freq1 == freq2

print(is_anagram("listen", "silent"))  # True
print(is_anagram("hello", "world"))    # False
```

### Can a String Be Rearranged Into a Palindrome?

A string can form a palindrome if at most **one** character has an odd count (for odd-length strings) or **no** odd counts (for even-length strings):

```python
def can_be_palindrome(text):
    freq = {}
    for char in text.lower():
        freq[char] = freq.get(char, 0) + 1

    odd_count = sum(1 for count in freq.values() if count % 2 == 1)
    return odd_count <= 1

print(can_be_palindrome("racecar"))  # True
print(can_be_palindrome("hello"))    # False (l and o both odd)
```

---

## Merging Two Dictionaries

What if you want to combine two dictionaries? Use `.update() or the `|` operator:

```python
a = {"x": 1, "y": 2}
b = {"y": 3, "z": 4}

# .update() — b's values overwrite a's on conflict
merged = a.copy()
merged.update(b)
print(merged)  # {'x': 1, 'y': 3, 'z': 4}

# | operator (Python 3.9+) — newer, cleaner
# merged = a | b
```

---

## Practice Exercise

**Scenario:** You're building a simple contact book!

**Your task:**
1. Create a dictionary called `contact` with these keys: `name`, `phone`, `email`
2. Add some values (use your own or make some up)
3. Print the contact's name
4. Print the contact's phone number
5. Add a new key `address` with a value
6. Print all keys and values using `.items()`

**Try it yourself first!** Solution below.

---

## Solution

```python
# Create contact dictionary
contact = {
    "name": "Arthur Drozdov",
    "phone": "07123456789",
    "email": "arthur@example.com"
}

# Print name and phone
print(f"Name: {contact['name']}")
print(f"Phone: {contact['phone']}")

# Add address
contact["address"] = "123 Main Street, London"

# Print all keys and values
print("\nFull Contact:")
for key, value in contact.items():
    print(f"{key}: {value}")
```

**Output:**
```
Name: Arthur Drozdov
Phone: 07123456789

Full Contact:
name: Arthur Drozdov
phone: 07123456789
email: arthur@example.com
address: 123 Main Street, London
```

---

## Quick Recap

- **Dictionaries** store data as **key-value pairs**
- Use **curly braces**: `{"key": "value"}`
- Access values with **keys**: `dict["key"]`
- Use **`.get()`** to avoid errors if key doesn't exist
- **Add/modify**: `dict["key"] = value`
- **Remove**: `del dict["key"]`
- **`.keys()`** — get all keys
- **`.values()`** — get all values
- **`.items()`** — get both keys and values
- **`in`** — check if key exists
- **`dict.get(key, default)`** — get a value, return default if key is missing (also a building block for frequency counting)
- **Frequency map** — `freq[char] = freq.get(char, 0) + 1` counts how many times each item appears
- **`sorted(strings, key=len)`** — sort strings by length (Lesson 3)
- **`sorted(string)`** — sort characters in a string: `sorted("cab")` → `['a','b','c']`

---

## What's Next?

Ready for more? Continue to **[Lesson 9: Advanced Dictionaries Practice](09-dictionaries-practice.md)**! 🎯

---

