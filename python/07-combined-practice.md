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
   - It contains at least one digit (hint: use `any(char.isdigit() for char in password)`)
3. Return `True` if valid, `False` if not
4. Test it with different passwords

**Try it yourself first!** Solution below.

---

## Exercise 4: Number Guessing Game 🎲

**Skills used:** While loops, conditionals, functions

**Your task:**
1. Create a function called `guess_number` that takes one parameter: `secret_number`
2. Use a while loop to let the user guess until they get it right
3. Keep track of how many attempts it takes
4. When they guess correctly, print a message with the number of attempts

**Hint:** Use `input()` to get the user's guess, and `int()` to convert it to a number.

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
    
    # Check if password contains at least one digit
    has_digit = any(char.isdigit() for char in password)
    if not has_digit:
        return False
    
    # If both checks pass, password is valid
    return True

# Test the function
print(is_valid_password("password123"))  # Output: True
print(is_valid_password("short"))         # Output: False
print(is_valid_password("nodigits"))      # Output: False
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

## Quick Recap

You've now practiced combining:
- **Variables + Lists** = Store multiple values
- **Loops + Lists** = Process each item
- **Functions + Conditionals** = Make decisions in functions
- **Functions + Return** = Send back results
- **While loops + Input** = Interactive programs

---

## What's Next?

Ready for more? Continue to **[Lesson 8: Dictionaries](08-dictionaries-explained.md)** (coming soon)! 🚀

Or go back to **[Lesson 6: Functions Explained](06-functions-explained.md)** to review!

---

**Your turn:** Try all 5 exercises! Don't worry if they take time — that's how you learn! 💛
