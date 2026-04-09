# Python Lesson 6: Functions — Reusable Code Blocks

**← Back to [Lesson 5: While Loops](05-while-loops-and-conditionals.md)**

---

## What is a Function?

**Plain English:** A function is a named block of code that does one specific thing. You can use (call) it whenever you need it, without rewriting the code.

**Real-world analogy:** Imagine you have a recipe for making coffee:
- You don't explain the whole process every time
- You just say "make coffee" and everyone knows what to do
- You can "call" this recipe whenever you want coffee

Functions work the same way!

---

## Why Use Functions?

**Without functions:**
```python
# Make coffee
print("Boil water")
print("Add coffee")
print("Pour into cup")
print("Add milk")

# Make tea
print("Boil water")
print("Add tea")
print("Pour into cup")
print("Add milk")

# Make hot chocolate
print("Boil water")
print("Add hot chocolate")
print("Pour into cup")
print("Add milk")
```

**With functions:**
```python
def make_hot_drink(drink_name):
    print("Boil water")
    print(f"Add {drink_name}")
    print("Pour into cup")
    print("Add milk")

make_hot_drink("coffee")
make_hot_drink("tea")
make_hot_drink("hot chocolate")
```

Much cleaner! And if you want to change something (like use almond milk), you only change it in ONE place!

---

## Defining a Function

Use the `def` keyword (short for "define"):

```python
def greet():
    print("Hello!")
    print("Welcome to Python!")

# Call the function
greet()

# Output:
# Hello!
# Welcome to Python!
```

**Key parts:**
- `def` — tells Python you're defining a function
- `greet` — the function name (you choose!)
- `()` — parentheses (we'll add stuff here soon)
- `:` — colon (required!)
- Indented code — what the function does

---

## Calling a Function

To use a function, you **call** it by name:

```python
def say_goodbye():
    print("Goodbye!")
    print("See you later!")

# Call the function
say_goodbye()

# Output:
# Goodbye!
# See you later!
```

**Important:** You must use parentheses `()` when calling a function!

---

## Functions with Parameters

Parameters let you pass information INTO the function:

```python
def greet_person(name):
    print(f"Hello, {name}!")
    print("Welcome to Python!")

greet_person("Szonja")
greet_person("Arthur")

# Output:
# Hello, Szonja!
# Welcome to Python!
# Hello, Arthur!
# Welcome to Python!
```

**Key terms:**
- **Parameter:** The variable inside the function definition (`name`)
- **Argument:** The actual value you pass when calling (`"Szonja"`)

---

## Multiple Parameters

You can have as many parameters as you need:

```python
def introduce(name, age, city):
    print(f"Hi, I'm {name}")
    print(f"I'm {age} years old")
    print(f"I live in {city}")

introduce("Szonja", 30, "London")

# Output:
# Hi, I'm Szonja
# I'm 30 years old
# I live in London
```

**Important:** Arguments must match the order of parameters!

---

## The `return` Statement

Functions can **return** a value (send something back):

```python
def add(a, b):
    result = a + b
    return result

total = add(5, 3)
print(total)  # Output: 8
```

**How it works:**
1. Call `add(5, 3)`
2. Function calculates `5 + 3 = 8`
3. `return` sends 8 back
4. `total` receives the value 8

---

## What Can You Return?

**You can return ANY type of data!** Not just numbers!

### Return a string:
```python
def get_greeting():
    return "Hello, World!"

message = get_greeting()
print(message)  # Output: Hello, World!
```

### Return a boolean:
```python
def is_adult(age):
    return age >= 18

result = is_adult(20)
print(result)  # Output: True
```

### Return a list:
```python
def get_colors():
    return ["red", "green", "blue"]

colors = get_colors()
print(colors)  # Output: ['red', 'green', 'blue']
```

### Return nothing (using `return` without a value):
```python
def say_goodbye():
    print("Goodbye!")
    return  # Optional - function ends here anyway

say_goodbye()  # Output: Goodbye!
```

---

## Return vs Print

**Big difference:**
- `print()` — shows output on screen (for humans to see)
- `return` — sends a value back to the code (for the program to use)

```python
def add_and_print(a, b):
    print(a + b)

def add_and_return(a, b):
    return a + b

# Using print
add_and_print(3, 5)  # Shows: 8
# But you can't use the result!

# Using return
result = add_and_return(3, 5)
print(result * 2)  # Output: 16 (you can use the result!)
```

---

## Practice Exercise

**Scenario:** You're building a calculator for a coffee shop!

**Your task:**
1. Create a function called `calculate_coffee_price` that takes one parameter: `size`
2. Inside the function:
   - If size is "small", return 2.50
   - If size is "medium", return 3.50
   - If size is "large", return 4.50
3. Call the function three times (once for each size)
4. Print the results with nice messages

**Hint:** Use `if/elif/else` inside the function!

**Try it yourself first!** Solution below.

---

## Solution

```python
def calculate_coffee_price(size):
    if size == "small":
        return 2.50
    elif size == "medium":
        return 3.50
    else:
        return 4.50

# Call the function for different sizes
small_price = calculate_coffee_price("small")
medium_price = calculate_coffee_price("medium")
large_price = calculate_coffee_price("large")

# Print results
print(f"Small coffee: £{small_price:.2f}")
print(f"Medium coffee: £{medium_price:.2f}")
print(f"Large coffee: £{large_price:.2f}")
```

**Output:**
```
Small coffee: £2.50
Medium coffee: £3.50
Large coffee: £4.50
```

---

## Quick Recap

- **Functions** are reusable blocks of code
- **`def`** defines a function
- **Parameters** let you pass data into functions
- **`return`** sends a value back — can be ANY type (number, string, boolean, list, etc.)
- **Call functions** by name with parentheses
- **Return vs Print:** Return for calculations, print for display

---

## What's Next?

Ready for more? Continue to **[Lesson 7: Combined Practice](07-combined-practice.md)**! 🚀

---

**Your turn:** Try the coffee shop exercise! Maybe add more sizes or drinks! ☕💛
