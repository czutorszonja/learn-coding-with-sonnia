# Python Lesson 5: While Loops + Conditionals — Making Decisions

**← Back to [Lesson 4: Loops](04-loops-explained.md)**

---

## Part 1: Conditionals (If/Else)

### What are Conditionals?

**Plain English:** Conditionals let your code make decisions based on whether something is true or false.

**Real-world analogy:** Imagine you're deciding what to wear:
- **IF** it's raining → take an umbrella
- **ELSE** (if it's not raining) → wear sunglasses

---

### The `if` Statement

```python
weather = "raining"

if weather == "raining":
    print("Take an umbrella!")

# Output: Take an umbrella!
```

**Important:** Notice the `==` (two equals signs)? That's for **comparing** values. One `=` assigns a value, two `==` compares values!

---

### Comparison Operators

You can compare values in different ways:

| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Equal to | `5 == 5` → `True` |
| `!=` | Not equal to | `5 != 3` → `True` |
| `>` | Greater than | `5 > 3` → `True` |
| `<` | Less than | `3 < 5` → `True` |
| `>=` | Greater than or equal | `5 >= 5` → `True` |
| `<=` | Less than or equal | `3 <= 5` → `True` |

**Tip:** Think of `<` and `>` like a crocodile mouth 🐊 — it always opens toward the bigger number!

---

### The `else` Statement

Use `else` to do something different when the condition is false:

```python
weather = "sunny"

if weather == "raining":
    print("Take an umbrella!")
else:
    print("Wear sunglasses!")

# Output: Wear sunglasses!
```

---

### The `elif` Statement

Use `elif` (else-if) for multiple conditions:

```python
temperature = 25

if temperature < 15:
    print("Wear a jacket!")
elif temperature < 25:
    print("Wear a light sweater!")
else:
    print("It's warm! Wear a t-shirt!")

# Output: It's warm! Wear a t-shirt!
```

**How it works:** Python checks each condition from top to bottom. When it finds a `True` condition, it runs that code and skips the rest!

---

## Part 2: While Loops

### What is a While Loop?

**Plain English:** A `while` loop keeps running **as long as** a condition is true.

**Real-world analogy:** Keep eating **while** you're hungry. When you're not hungry anymore, stop!

---

### Basic While Loop

```python
count = 1

while count <= 5:
    print(f"Count: {count}")
    count = count + 1  # Don't forget this!

# Output:
# Count: 1
# Count: 2
# Count: 3
# Count: 4
# Count: 5
```

**Important:** The `count = count + 1` line is crucial! Without it, the loop would run forever (infinite loop)!

---

### While vs For Loops

- **`for` loops**: Loop through a list or range (you know how many times it will run)
- **`while` loops**: Loop while a condition is true (might run any number of times)

Example with `for`:
```python
# Print 1-5 using for loop
for i in range(1, 6):
    print(i)
```

Same thing with `while`:
```python
# Print 1-5 using while loop
count = 1
while count <= 5:
    print(count)
    count = count + 1
```

---

### Real-World While Loop Example

```python
# Simulate a login attempt
password = "secret123"
user_input = ""
attempts = 0

while user_input != password:
    user_input = input("Enter password: ")
    attempts = attempts + 1
    print(f"Attempt {attempts}")

print("Login successful!")
```

This keeps asking for the password **while** the user gets it wrong. When they get it right, the loop stops!

---

## Practice Exercise

**Scenario:** You're building a simple countdown timer!

1. Create a variable called `countdown` and set it to 10
2. Use a `while` loop to print the countdown value
3. Decrease the countdown by 1 each time through the loop
4. When the countdown reaches 0, print "Blast off! 🚀"

**Hint:** You'll need an `if` statement inside your `while` loop to check when countdown reaches 0!

**Try it yourself first!** Scroll down when ready.

---

## Solution

```python
# Create countdown variable
countdown = 10

# Loop while countdown is greater than 0
while countdown > 0:
    print(f"T-minus {countdown}...")
    countdown = countdown - 1

# Print final message
print("Blast off! 🚀")
```

**Output:**
```
T-minus 10...
T-minus 9...
T-minus 8...
T-minus 7...
T-minus 6...
T-minus 5...
T-minus 4...
T-minus 3...
T-minus 2...
T-minus 1...
Blast off! 🚀
```

---

## Extra Practice Exercises

Want more practice? Try these! Solutions are below.

### Exercise 1: While Loop — Savings Goal 💰

**Scenario:** You're saving money for a new laptop that costs £1000. You save £100 each week.

**Your task:**
1. Create a variable `savings` starting at 0
2. Create a variable `goal` set to 1000
3. Use a `while` loop that runs while `savings` is less than `goal`
4. Each week, add £100 to savings
5. Print your current savings after each week
6. When you reach the goal, print "I bought the laptop! 🎉"

**Try it yourself first!** Solution below.

---

### Exercise 2: If/Elif/Else — Cinema Tickets 🎬

**Scenario:** You're working at a cinema and need to calculate ticket prices based on age!

**Your task:**
1. Create a variable `age` and set it to any number you want
2. Use `if/elif/else` to determine the ticket price:
   - Under 12: Child ticket = £8
   - 12 to 17: Teenager ticket = £12
   - 18 to 64: Adult ticket = £15
   - 65 and older: Senior ticket = £10
3. Print the ticket price based on the age

**Try it yourself first!** Solution below.

---

## Extra Practice Solutions

### Savings Goal Solution

```python
savings = 0
goal = 1000
week = 0

while savings < goal:
    week = week + 1
    savings = savings + 100
    print(f"Week {week}: £{savings} saved")

print("I bought the laptop! 🎉")
```

**Output:**
```
Week 1: £100 saved
Week 2: £200 saved
Week 3: £300 saved
...
Week 10: £1000 saved
I bought the laptop! 🎉
```

---

### Cinema Tickets Solution

```python
age = 25

if age < 12:
    print("Child ticket: £8")
elif age < 18:
    print("Teenager ticket: £12")
elif age < 65:
    print("Adult ticket: £15")
else:
    print("Senior ticket: £10")
```

**Output (for age 25):**
```
Adult ticket: £15
```

**Tip:** Since we check conditions in order, we don't need to check both bounds! If `age < 12` is false, we already know age is at least 12!

---

## Quick Recap

- **`if` statements** make decisions based on conditions
- **`==`** compares values (don't confuse with `=` which assigns!)
- **`else`** runs when the `if` condition is false
- **`elif`** lets you check multiple conditions
- **`while` loops** run while a condition is true
- **Don't forget to update your loop variable** or you'll have an infinite loop!

---

## What's Next?

Ready for more? Continue to **[Lesson 6: Functions Explained](06-functions-explained.md)**! 🚀

---

**Your turn:** Try the countdown exercise! Make it your own — maybe countdown from 5, or add a custom message! 🚀💛
