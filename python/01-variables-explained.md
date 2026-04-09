# Python Lesson 1: Variables — Your Memory Boxes

**← Back to [Python Setup Guide](README.md)**

---

## What is a Variable?

**Plain English:** A variable is like a labeled box where you can store something to use later.

**Real-world analogy:** Imagine you're cooking and you have containers in your kitchen:
- A jar labeled "sugar" 
- A bottle labeled "olive oil"
- A container labeled "flour"

You don't need to remember what's inside — the label tells you. Variables work the same way in Python.

## How to Create a Variable

In Python, you create a variable by giving it a name and putting something inside:

```python
# Creating variables
name = "Szonja"
age = 30
height = 1.65
is_learning = True
```

**What's happening:**
- `name` is the label (variable name)
- `=` means "put this inside the box"
- `"Szonja"` is what's inside (the value)

## Different Types of Data

Variables can hold different kinds of information:

| Type | Example | What it is |
|------|---------|------------|
| String | `"hello"` | Text (in quotes) |
| Integer | `42` | Whole numbers |
| Float | `3.14` | Decimal numbers |
| Boolean | `True` or `False` | Yes/No values |

## Using Variables

Once you've stored something, you can use it:

```python
# Create variables
first_name = "Szonja"
last_name = "Doe"

# Use them
print(first_name)  # Output: Szonja
print(last_name)   # Output: Doe

# Combine them
full_name = first_name + " " + last_name
print(full_name)   # Output: Szonja Doe
```

## Important Rules

1. **Variable names can't have spaces** — use underscores: `my_variable` ✅ not `my variable` ❌
2. **Names are case-sensitive** — `Age` and `age` are different variables
3. **Start with a letter or underscore** — not a number
4. **Make names descriptive** — `customer_name` is better than `x`

## Practice Exercise

**Scenario:** You're creating a profile for a dating app. Create variables to store:
- Your nickname
- Your age
- Your city
- Whether you like dogs (True/False)

Then print each variable, and create one more variable that combines your nickname and city.

**Try it yourself first!** Then scroll down to check your answer.

---

## Solution

```python
# Create your profile variables
nickname = "Szoni"
age = 30
city = "Budapest"
likes_dogs = True

# Print each variable
print(nickname)
print(age)
print(city)
print(likes_dogs)

# Combine nickname and city
location = nickname + " from " + city
print(location)  # Output: Szoni from Budapest
```

## Quick Recap

- Variables = labeled boxes for storing data
- Use `=` to put data in a variable
- Different types: strings, numbers, booleans
- Use descriptive names
- No spaces in variable names

---

## What's Next?

Ready for more? Continue to **[Lesson 2: Operations with Variables](02-operations-with-variables.md)**! 🚀

---

**Your turn:** Try the exercise above. If you get stuck or have questions, just ask! 💛
