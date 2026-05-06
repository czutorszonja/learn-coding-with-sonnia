# Python Lesson 7: Combined Practice — Put It All Together! 🎯

**← Back to [Lesson 6: Functions](06-functions-explained.md)**

---

## Welcome to Lesson 7!

You've learned so much already:
- ✅ Variables
- ✅ Operations (math, strings, f-strings)
- ✅ Lists
- ✅ For loops
- ✅ While loops
- ✅ If/Else/Elif conditionals
- ✅ Functions

Now it's time to **combine everything** into real-world projects! This lesson has 5 practice exercises that build on each other.

**Tip:** Take your time. These are more challenging than previous exercises. That's normal!

---

## Exercise 1: Shopping List Manager 🛒

**Skills used:** Lists, for loops, functions

**Your task:**
1. Create a function called `print_shopping_list` that takes one parameter: `items` (a list)
2. Inside the function, use a for loop to print each item with a number (1., 2., 3., etc.)
3. Create a shopping list with 5 items
4. Call the function with your list

**Example output:**
```
Shopping List:
1. Milk
2. Eggs
3. Bread
4. Butter
5. Apples
```

**Try it yourself first!** Solution below.

---

## Exercise 2: Temperature Converter 🌡️

**Skills used:** Functions, if/elif/else, return statements

**Your task:**
1. Create a function called `convert_temperature` that takes two parameters: `temp` and `unit`
2. If `unit` is "C", convert to Fahrenheit and return it (formula: `F = C * 9/5 + 32`)
3. If `unit` is "F", convert to Celsius and return it (formula: `C = (F - 32) * 5/9`)
4. Test it with a few temperatures

**Try it yourself first!** Solution below.

---

## Exercise 3: Password Validator 🔐

**Skills used:** Functions, conditionals, return booleans

**Your task:**
1. Create a function called `is_valid_password` that takes one parameter: `password`
2. The password is valid if:
   - It's at least 8 characters long
   - It starts with the letter "S"
3. Return `True` if valid, `False` if not
4. Test it with different passwords

**Hint:** Think about how you access the first item in a list!

**Try it yourself first!** Solution below.

---

## Exercise 4: Number Guessing Game 🎲

**Skills used:** While loops, conditionals, functions

**Your task:**
1. Create a function called `guess_number` that takes one parameter: `secret_number`
2. Use a while loop to let the user guess until they get it right
3. Keep track of how many attempts it takes
4. When they guess correctly, print a message with the number of attempts

**Hint:** Remember how to get user input and convert it to a number!

**Try it yourself first!** Solution below.

---

## Exercise 5: Student Grade Calculator 📚

**Skills used:** ALL OF THE ABOVE! Lists, loops, functions, conditionals, return statements

**Your task:**
1. Create a function called `calculate_average` that takes one parameter: `grades` (a list of numbers)
2. Calculate and return the average of all grades
3. Create a function called `get_letter_grade` that takes one parameter: `average`
4. Return a letter grade based on the average:
   - 90-100: A
   - 80-89: B
   - 70-79: C
   - 60-69: D
   - Below 60: F
5. Create a list of grades (e.g., `[85, 92, 78, 90, 88]`)
6. Calculate the average and get the letter grade
7. Print a nice report

**Example output:**
```
Grades: [85, 92, 78, 90, 88]
Average: 86.6
Letter Grade: B
```

**Try it yourself first!** Solution below.

---

## Solutions

### Exercise 1 Solution: Shopping List Manager

```python
def print_shopping_list(items):
    print("Shopping List:")
    for index, item in enumerate(items, start=1):
        print(f"{index}. {item}")

# Create shopping list
groceries = ["Milk", "Eggs", "Bread", "Butter", "Apples"]

# Call the function
print_shopping_list(groceries)
```

**Output:**
```
Shopping List:
1. Milk
2. Eggs
3. Bread
4. Butter
5. Apples
```

---

### Exercise 2 Solution: Temperature Converter

```python
def convert_temperature(temp, unit):
    if unit == "C":
        # Convert Celsius to Fahrenheit
        fahrenheit = temp * 9/5 + 32
        return fahrenheit
    elif unit == "F":
        # Convert Fahrenheit to Celsius
        celsius = (temp - 32) * 5/9
        return celsius
    else:
        return "Invalid unit"

# Test the function
print(f"25°C = {convert_temperature(25, 'C')}°F")
print(f"77°F = {convert_temperature(77, 'F')}°C")
```

**Output:**
```
25°C = 77.0°F
77°F = 25.0°C
```

---

### Exercise 3 Solution: Password Validator

```python
def is_valid_password(password):
    # Check if password is at least 8 characters
    if len(password) < 8:
        return False
    
    # Check if password starts with "S"
    if password[0] == "S":
        return True
    else:
        return False

# Test the function
print(is_valid_password("Supersecret"))  # Output: True
print(is_valid_password("password"))      # Output: False (doesn't start with S)
print(is_valid_password("Short"))         # Output: False (too short)
```

---

### Exercise 4 Solution: Number Guessing Game

```python
def guess_number(secret_number):
    attempts = 0
    guess = None
    
    print(f"I'm thinking of a number...")
    
    while guess != secret_number:
        guess = int(input("Your guess: "))
        attempts = attempts + 1
        
        if guess < secret_number:
            print("Too low!")
        elif guess > secret_number:
            print("Too high!")
        else:
            print(f"Correct! You got it in {attempts} attempts!")

# Play the game with secret number 7
guess_number(7)
```

**Example output:**
```
I'm thinking of a number...
Your guess: 5
Too low!
Your guess: 8
Too high!
Your guess: 7
Correct! You got it in 3 attempts!
```

---

### Exercise 5 Solution: Student Grade Calculator

```python
def calculate_average(grades):
    total = sum(grades)
    count = len(grades)
    average = total / count
    return average

def get_letter_grade(average):
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"

# Create list of grades
grades = [85, 92, 78, 90, 88]

# Calculate average
avg = calculate_average(grades)

# Get letter grade
letter = get_letter_grade(avg)

# Print report
print(f"Grades: {grades}")
print(f"Average: {avg:.1f}")
print(f"Letter Grade: {letter}")
```

**Output:**
```
Grades: [85, 92, 78, 90, 88]
Average: 86.6
Letter Grade: B
```

**Note:** `sum(grades)` adds all numbers in the list, and `len(grades)` counts how many items are in the list!

---

---

## Algorithmic Thinking — How to Break Down Any Hard Problem

**This is the skill that bridges "I can follow examples" and "I can solve anything".**

When you get a question you've never seen before, don't panic. Use this step-by-step approach:

**Step 1 — Trace it by hand.** Pretend you are Python and work out what the answer should be for the given example.

**Step 2 — Identify the pattern.** What are you working with? Strings? Numbers? Lists? What operation turns the input into the output?

**Step 3 — Break it into plain English steps.** Write the logic in sentences before you write any code.

**Step 4 — Write one step at a time.** Implement and test each piece before moving to the next.

---

### Worked Example 1: `"a3b2c1" → "aaabbc"`

**Step 1 — Trace it manually:**
- See `a`, then `3` → output `aaa`
- See `b`, then `2` → output `bb`
- See `c`, then `1` → output `c`
- Combined: `aaabbc`

**Step 2 — Pattern:** The string alternates letter-digit-letter-digit. Each letter is repeated by the digit that follows it.

**Step 3 — Plain steps:**
1. Separate all letters into one list, all digits into another list
2. Pair each letter with its digit using `zip()`
3. For each pair, repeat the letter by the digit amount
4. Combine all results into one string with `.join()`

**Step 4 — Write it:**

```python
def expand_string(text):
    # Step 1: separate letters and digits into two lists
    letters = []
    digits = []

    for char in text:
        if char.isdigit():       # is this character a number?
            digits.append(char)  # put it in the digits list
        else:
            letters.append(char) # otherwise it's a letter

    # Steps 2 & 3: pair each letter with a digit, repeat the letter
    result = []
    for letter, digit in zip(letters, digits):
        repeated = letter * int(digit)  # "a" * int("3") = "aaa"
        result.append(repeated)

    # Step 4: combine everything into one string
    return "".join(result)

print(expand_string("a3b2c1"))  # aaabbc
print(expand_string("x5y2"))    # xxxxxyy
```

**Key techniques used:**
- `char.isdigit()` to categorise each character (Lesson 2)
- Two accumulator lists inside a loop (Lesson 4)
- `zip()` to pair two lists together (Lesson 3)
- `letter * int(digit)` to repeat a string (Lesson 3)
- `"".join(result)` to merge the list into one string (Lessons 2 and 3)

---

### Worked Example 2: `115 → "one hundred fifteen"`

**Step 1 — Trace it manually:**
- 115 = 100 + 10 + 5
- 100 = "one hundred", 10 = "ten", 5 = "five"
- Combined: "one hundred fifteen"

**Step 2 — Pattern:** The number breaks into hundreds, tens, and ones. Each digit maps to a word, but 11–19 have their own special names.

**Step 3 — Plain steps:**
1. Map each digit to its word using a dictionary
2. Handle the 11–19 special case first
3. Split into hundreds and remainder using `//` and `%`
4. Build the result by adding each part in order

**Step 4 — Write it:**

```python
def number_to_words(num):
    # Special teen words (they don't follow the normal pattern)
    teens = {
        11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
        15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen",
        19: "nineteen"
    }

    # Normal digit names
    ones = {
        0: "zero", 1: "one", 2: "two", 3: "three", 4: "four",
        5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"
    }

    tens_map = {
        2: "twenty", 3: "thirty", 4: "forty", 5: "fifty",
        6: "sixty", 7: "seventy", 8: "eighty", 9: "ninety"
    }

    if num == 0:
        return "zero"

    # Handle teens first (they have special names)
    if 11 <= num <= 19:
        return teens[num]

    # Break into hundreds and remainder
    hundreds = num // 100
    remainder = num % 100

    parts = []

    # Add "X hundred" if there is a hundreds component
    if hundreds > 0:
        parts.append(ones[hundreds] + " hundred")

    # Handle the remainder
    if remainder >= 11 and remainder <= 19:
        parts.append(teens[remainder])
    elif remainder >= 10:
        tens_digit = remainder // 10
        ones_digit = remainder % 10
        if ones_digit == 0:
            parts.append(tens_map[tens_digit])
        else:
            parts.append(tens_map[tens_digit] + " " + ones[ones_digit])
    elif remainder > 0:
        parts.append(ones[remainder])

    return " ".join(parts)

print(number_to_words(115))  # one hundred fifteen
print(number_to_words(7))    # seven
print(number_to_words(23))   # twenty three
print(number_to_words(99))   # ninety nine
print(number_to_words(100))  # one hundred
```

**Key techniques used:**
- Dictionary mapping to connect numbers to words (Lesson 8)
- Integer division `//` and modulo `%` to split a number into place values
- `if / elif / else` chains to handle special cases (Lessons 5 and 7)
- Building a result and `.join()`ing it into a string

---

### Your Exam Problem-Solving Checklist

When you see a new problem:

- [ ] What is the **input**? (string, list, number?)
- [ ] What is the **expected output**?
- [ ] Can I **trace the example by hand**?
- [ ] What **pattern** do I see? (repetition, pairing, mapping, filtering?)
- [ ] What **building blocks** do I need? (lists, dicts, loops, conditions?)
- [ ] What are the **steps** in plain English?
- [ ] Write it **one step at a time**

---

## Quick Recap

You've now practiced combining:
- **Variables + Lists** = Store multiple values
- **Loops + Lists** = Process each item
- **Functions + Conditionals** = Make decisions in functions
- **Functions + Return** = Send back results
- **While loops + Input** = Interactive programs
- **Algorithmic thinking** = Break down any unseen problem step by step

---

## What's Next?

You've got a solid foundation now! Before moving on to more advanced topics, try building this project to practice everything you've learned:

**📁 [Mini Project 1: Study Tracker](mini-project-1-study-tracker.md)** — Build a practical study task tracker!

When you're ready to continue, head to **[Lesson 8: Dictionaries](08-dictionaries-explained.md)**! 🚀

---

