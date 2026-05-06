# Python Lesson 2: Operations — Doing Things with Variables

**← Back to [Lesson 1: Variables](01-variables-explained.md)**

---

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

### Combining a List Into One String: `.join()`

When you have a list of strings and want to merge them into one string, use `.join()`:

```python
words = ["hello", "world", "from", "Sonnia"]
sentence = " ".join(words)     # join with spaces → "hello world from Sonnia"
sentence_comma = ", ".join(words)  # join with commas → "hello, world, from, Sonnia"
no_spaces = "".join(words)         # join with nothing → "helloworldfromSonnia"

print(sentence)
# Output: hello world from Sonnia
```

**Common mistake:** `.join()` goes on the *separator*, not the list:
```python
# Wrong:
" ".join("hello", "world")    # Error!

# Right:
" ".join(["hello", "world"])  # ✓
```

---

### Turning a List of Characters Into a String

A very common pattern: build a list of characters or strings piece by piece, then combine them into one final string:

```python
# Example: take every letter and make it doubled
text = "abc"
result = []

for char in text:
    result.append(char * 2)  # char * 2 repeats it (just like "A" * 3 → "AAA")

final = "".join(result)       # combine the list into a single string
print(final)  # Output: aabbcc
```

**The pattern works like this:**
```python
# Step 1: start with an empty list
output = []

# Step 2: loop through something
for item in data:
    output.append(something_built_from(item))

# Step 3: join everything into one string
final = "".join(output)
```

This is the same pattern as building a list with `append` from Lesson 4 — then adding `.join()` at the end to turn the list into a clean string.

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

## Checking What Kind of Character It Is

When you need to examine a string character by character, Python gives you useful tests:

```python
"7".isdigit()     # True  — is it a digit (0–9)?
"a".isdigit()     # False

"x".isalpha()     # True  — is it a letter (a–z or A–Z)?
"!".isalpha()     # False

"x".isalnum()     # True  — is it alphanumeric (letter OR digit)?
"7".isalnum()     # True
"!".isalnum()     # False
```

These are especially useful inside a loop over a string:

```python
def separate_letters_and_numbers(text):
    letters = []
    digits = []

    for char in text:
        if char.isdigit():
            digits.append(char)
        elif char.isalpha():
            letters.append(char)

    print(f"Letters: {letters}")
    print(f"Digits: {digits}")

separate_letters_and_numbers("Hello3World")
# Output:
# Letters: ['H', 'e', 'l', 'l', 'o', 'W', 'o', 'r', 'l', 'd']
# Digits: ['3']
```

Or to filter or transform:

```python
# Example: remove all non-letters from a string
text = "H3llo! W0rld!"
clean = []

for char in text:
    if char.isalpha():
        clean.append(char)

result = "".join(clean)
print(result)  # Output: HllWrld
```

---

## Quick Recap

- **Math operations:** `+`, `-`, `*`, `/`, `**` (exponent)
- **String concatenation:** Combine strings with `+`
- **String repetition:** Multiply string by number: `"Hi" * 3`
- **`.join(separator)`** — combine a list of strings into one string with a separator in between
- **`str.isdigit()`** — `True` if the character is a digit (0–9)
- **`str.isalpha()`** — `True` if the character is a letter
- **`str.isalnum()`** — `True` if the character is a letter or digit
- **f-strings:** Clean way to insert variables: `f"Hello {name}"`
- **Order of operations:** Parentheses first, then multiply/divide, then add/subtract

---

## What's Next?

Ready for more? Continue to **[Lesson 3: Lists Explained](03-lists-explained.md)**! 🚀

---

