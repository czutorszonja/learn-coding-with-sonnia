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

---

## What's Next?

Lesson 9 will cover **more dictionary practice** — combining dictionaries with lists, nested dictionaries, and real-world projects!

---

**Your turn:** Try the contact book exercise! Use your own contact info or make up a fictional character! 📇💛
