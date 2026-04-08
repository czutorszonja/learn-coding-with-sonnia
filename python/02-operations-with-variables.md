# Python Lesson 2: Operations — Doing Things with Variables

## What are Operations?

**Plain English:** Operations are actions you can perform on variables — like math, combining text, or comparing values.

You already did one operation in Lesson 1: combining two strings with `+`. Now let's go deeper!

---

## Math Operations

Python can do all the basic math you'd expect:

```python
# Addition
apples = 5
oranges = 3
total_fruit = apples + oranges
print(total_fruit)  # Output: 8

# Subtraction
money = 100
spent = 35
remaining = money - spent
print(remaining)  # Output: 65

# Multiplication
price = 10
quantity = 4
total = price * quantity
print(total)  # Output: 40

# Division
cookies = 20
people = 4
cookies_each = cookies / people
print(cookies_each)  # Output: 5.0

# Exponents (power)
base = 2
squared = base ** 2
print(squared)  # Output: 4
```

**Note:** Division in Python always returns a decimal (float), even if the result is a whole number. That's why `20 / 4` gives `5.0` not `5`.

---

## String Operations

You already know you can combine strings with `+`. This is called **concatenation**:

```python
first_name = "Szonja"
last_name = "Doe"
full_name = first_name + " " + last_name
print(full_name)  # Output: Szonja Doe
```

**Important:** You need to add the space manually! `"Szonja" + "Doe"` would give `"SzonjaDoe"` (no space).

### Repeating Strings

You can also multiply a string by a number to repeat it:

```python
cheer = "Yay "
excited = cheer * 3
print(excited)  # Output: Yay Yay Yay 
```

---

## The Clean Way: f-strings

Remember how you had to combine `nickname + city` and it felt a bit clunky? Python has a better way!

**f-strings** let you insert variables directly into text:

```python
nickname = "Szonja"
city = "London"

# Old way (concatenation)
location = nickname + " from " + city
print(location)  # Output: Szonja from London

# New way (f-string) - cleaner!
location = f"{nickname} from {city}"
print(location)  # Output: Szonja from London
```

See the `f` before the quotes? That tells Python: "Hey, there are variables inside these curly braces — replace them with their values!"

### f-strings with numbers

```python
name = "Arthur"
age = 30

# Using concatenation (old way)
message = "My name is " + name + " and I am " + str(age) + " years old"

# Using f-string (clean way)
message = f"My name is {name} and I am {age} years old"
print(message)  # Output: My name is Arthur and I am 30 years old
```

**Why is the old way annoying?** You have to convert numbers to strings with `str()` and add `+` everywhere. f-strings are much cleaner!

---

## Order of Operations

Just like in math, Python follows a specific order:

```python
# What does this equal?
result = 2 + 3 * 4
print(result)  # Output: 14, NOT 20!

# Why? Multiplication happens BEFORE addition
# So it's: 2 + (3 * 4) = 2 + 12 = 14

# Use parentheses to control order
result = (2 + 3) * 4
print(result)  # Output: 20
```

**Rule:** Parentheses first, then multiplication/division, then addition/subtraction.

---

## Practice Exercise

**Scenario:** You're running a small bakery. Create variables for:
- Price per cupcake: £3.50
- Number of cupcakes sold: 12
- Price per cookie: £2.00
- Number of cookies sold: 8

Then calculate:
1. Total revenue from cupcakes
2. Total revenue from cookies
3. Grand total (cupcakes + cookies)
4. Print a nice summary message using an f-string

**Try it yourself first!** Scroll down when ready.

---

## Solution

```python
# Create variables
price_cupcake = 3.50
cupcakes_sold = 12
price_cookie = 2.00
cookies_sold = 8

# Calculate revenues
cupcake_revenue = price_cupcake * cupcakes_sold
cookie_revenue = price_cookie * cookies_sold
total_revenue = cupcake_revenue + cookie_revenue

# Print summary with f-string
print(f"Cupcakes: £{cupcake_revenue}")
print(f"Cookies: £{cookie_revenue}")
print(f"Total: £{total_revenue}")

# Output:
# Cupcakes: £42.0
# Cookies: £16.0
# Total: £58.0
```

---

## Quick Recap

- **Math operations:** `+`, `-`, `*`, `/`, `**` (exponent)
- **String concatenation:** Combine strings with `+`
- **String repetition:** Multiply string by number: `"Hi" * 3`
- **f-strings:** Clean way to insert variables: `f"Hello {name}"`
- **Order of operations:** Parentheses first, then multiply/divide, then add/subtract

---

## What's Next?

Lesson 3 will cover **working with lists** — how to store multiple items in one variable (like a shopping list!).

---

**Your turn:** Try the bakery exercise! If you get stuck, just ask. 💛
