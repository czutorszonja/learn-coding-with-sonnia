# Exam Challenge Set — LeetCode-Style Problems 🌞

**For:** CFG Python Exam  
**Based on:** Lessons 1–18 (everything you need is in your lesson files)

---

> **How to use this file:** Each challenge has three parts:
> 1. **Problem** — what to solve
> 2. **Approach** — how to think about it (the algorithmic breakdown)
> 3. **Solution** — complete working code
>
> Try the **Approach** step first without looking at the solution. If you're stuck, the approach shows you the thinking without giving away the full code. Only check the solution when you've had a proper go.

---

---

# 🔍 Part 1: Algorithmic Thinking — Your Exam Framework

Before any code, internalise this process. **Every problem on the exam follows this shape.**

## The 4-Step Decomposition Method

**Step 1 — Understand the input and output.**  
Run the example through your head manually. What goes in? What comes out? What does Python see step by step?

**Step 2 — Find the pattern.**  
What operation turns the input into the output? Look for:  
- Repetition? (loop + append)
- Mapping? (dictionary lookup)
- Pairing? (`zip()`)
- Filtering? (loop + condition)
- Arithmetic breakdown? (`//` and `%`)

**Step 3 — Write the steps in plain English.**  
Before touching Python, write the algorithm as bullet points. This is your proof you've thought it through.

**Step 4 — Translate to Python, one step at a time.**  
Implement step by step. Test each piece before adding the next.

---

## Your Problem-Solving Checklist

Copy this into your exam paper or write it before you start each question:

```
[ ] What is the INPUT?  (string / list / number / dict?)
[ ] What is the OUTPUT?
[ ] Can I trace the example by hand?
[ ] Pattern: repetition / mapping / pairing / filtering / arithmetic?
[ ] What building blocks do I need?
[ ] Steps in plain English first?
```

---

## Worked Example: `"a3b2c1" → "aaabbc"` (Medium)

This is the exam-style problem you shared. Let's break it down properly.

**Step 1 — Trace it:**
- See `a`, then `3` → output `aaa`
- See `b`, then `2` → output `bb`
- See `c`, then `1` → output `c`
- Combined: `aaabbc`

**Step 2 — Pattern:** The string alternates between letters and digits. Each letter is repeated by the digit that follows it.

**Step 3 — Plain English steps:**
1. Walk through the string, separate letters into one list, digits into another
2. Pair each letter with its digit using `zip()`
3. For each pair, repeat the letter `int(digit)` times
4. Join all the pieces together

**Step 4 — Code (see Solution to Challenge 5)**

---

## Worked Example: `115 → "one hundred fifteen"` (Medium)

**Step 1 — Trace it:** 115 = 100 + 10 + 5 → "one" + "hundred" + "fifteen"

**Step 2 — Pattern:** The number breaks into hundreds, tens, and ones. Each digit maps to a word. But 11–19 are special.

**Step 3 — Plain English steps:**
1. Check for special teen cases (11–19)
2. Extract hundreds with `num // 100`, remainder with `num % 100`
3. Map each digit to its word using a dictionary
4. Build the result piece by piece and join with spaces

**Step 4 — Code (see Solution to Challenge 10)**

---

---

# 🔥 Part 2: The Challenges

---

## Challenge 1: Count Vowels
**Difficulty:** Easy | **Topics:** strings, loops, conditionals

### Problem
Write a function `count_vowels(text)` that returns the number of vowel letters (a, e, i, o, u) in the input string. The search should be **case-insensitive**.

```
count_vowels("Hello World")  → 3  (e, o, o)
count_vowels("rhythm")       →  0
count_vowels("AEIOU")        →  5
```

### Approach
1. What is input? A string. Output? A number.
2. Walk through each character. If it's a vowel, count it.
3. A loop goes through every character. A condition checks if it's in `"aeiouAEIOU"`.

### Solution
```python
def count_vowels(text):
    count = 0
    vowels = "aeiouAEIOU"
    for char in text:
        if char in vowels:
            count += 1
    return count
```

---

## Challenge 2: Reverse a String
**Difficulty:** Easy | **Topics:** strings, loops

### Problem
Write a function `reverse_string(text)` that returns the string reversed.

```
reverse_string("hello")   → "olleh"
reverse_string("Szonja")  → "ajnzoS"
reverse_string("racecar") → "racecar"
```

### Approach
1. Build a new string by walking through the input from back to front.
2. Use `range(len(text))` to get index numbers.
3. Append each character to a list, then `.join()` it at the end.

### Solution
```python
def reverse_string(text):
    result = []
    for i in range(len(text)):
        result.append(text[i])
    return "".join(reversed(result))

# Or even cleaner:
def reverse_string(text):
    return "".join(char for char in reversed(text))

# Or build forward:
def reverse_string(text):
    result = []
    for i in range(len(text) - 1, -1, -1):  # count backwards
        result.append(text[i])
    return "".join(result)
```

---

## Challenge 3: Is It a Palindrome?
**Difficulty:** Easy | **Topics:** strings, functions

### Problem
Write a function `is_palindrome(text)` that returns `True` if the word reads the same forwards and backwards. Ignore case.

```
is_palindrome("racecar")  → True
is_palindrome("hello")    → False
is_palindrome("Madam")    → True
is_palindrome("")         → True
```

### Approach
1. Reverse the string and compare it to the original.
2. Use Challenge 2's trick, or slice backwards: `text[::-1]`.
3. Compare: `text == reversed_text`.

### Solution
```python
def is_palindrome(text):
    # Slice backwards: start at end, go to start, step -1
    reversed_text = text[::-1]
    return text.lower() == reversed_text.lower()

# Or use the reverse_string function from Challenge 2:
def is_palindrome(text):
    return reverse_string(text) == text
```

---

## Challenge 4: Sum and Max in One Pass
**Difficulty:** Easy | **Topics:** lists, loops

### Problem
Write a function `sum_and_max(numbers)` that returns **both** the sum and the maximum value of a list, without using `sum()` or `max()`.

```
sum_and_max([1, 2, 3, 4, 5]) → (15, 5)
sum_and_max([10, 20])         → (30, 20)
sum_and_max([42])             → (42, 42)
```

### Approach
1. Start with `total = 0` and `largest = numbers[0]`.
2. Loop through every number.
3. For each number, add it to the total and check if it's larger than the current largest.
4. Return both at the end.

### Solution
```python
def sum_and_max(numbers):
    total = 0
    largest = numbers[0]
    for num in numbers:
        total += num
        if num > largest:
            largest = num
    return (total, largest)
```

---

## Challenge 5: Expand String — `"a3b2c1" → "aaabbc"`
**Difficulty:** Medium | **Topics:** strings, lists, zip, join

### Problem
Write a function `expand_string(text)` that takes a string of alternating letters and digits (like `"a3b2c1"`) and expands it so each digit tells you how many times to repeat the preceding letter.

```
expand_string("a3b2c1")  → "aaabbc"
expand_string("x5y2")    → "xxxxxyy"
expand_string("z1")      → "z"
```

### Approach
1. Separate letters and digits into two lists using a `for` loop and `isdigit()`.
2. Pair them up with `zip()`.
3. For each pair, repeat the letter `int(digit)` times and append to a results list.
4. Join the results into one string.

### Solution
```python
def expand_string(text):
    letters = []
    digits = []

    # Step 1: separate
    for char in text:
        if char.isdigit():
            digits.append(char)
        else:
            letters.append(char)

    # Steps 2 & 3: pair and expand
    result = []
    for letter, digit in zip(letters, digits):
        result.append(letter * int(digit))

    # Step 4: combine into one string
    return "".join(result)
```

---

## Challenge 6: Find the Second Largest
**Difficulty:** Easy | **Topics:** lists, sorting, sets

### Problem
Write a function `second_largest(numbers)` that returns the second largest **distinct** number. The list will always have at least 2 distinct numbers.

```
second_largest([1, 2, 3, 4, 5])      → 4
second_largest([10, 20, 20, 30])     → 20  (duplicates ignored)
second_largest([1, 3, 3, 7, 9, 9])  → 7
```

### Approach
1. Remove duplicates by converting to a `set()`.
2. Sort the unique numbers in descending order.
3. Return the second element.

### Solution
```python
def second_largest(numbers):
    unique = set(numbers)       # remove duplicates
    sorted_nums = sorted(unique, reverse=True)
    return sorted_nums[1]       # second largest
```

---

## Challenge 7: Two Sum
**Difficulty:** Medium | **Topics:** lists, dictionaries, loops

### Problem
Write a function `two_sum(numbers, target)` that takes a list of numbers and a target value. Return `True` if any two numbers in the list add up to the target.

```
two_sum([1, 2, 3, 4, 5], 9)   → True   (4 + 5 = 9)
two_sum([1, 2, 3, 4, 5], 10)  → False
two_sum([3, 3], 6)             → True   (3 + 3 = 6)
```

### Approach
1. Walk through the list. For each number, figure out what you need to add to it to reach the target: `needed = target - current`.
2. Keep a dictionary tracking numbers you've already seen (`{number: index}`).
3. If `needed` is already in the dictionary, you found your pair — return `True`.
4. If you finish the loop, no pair exists.

### Solution
```python
def two_sum(numbers, target):
    seen = {}  # maps number → index of where we've seen it

    for i, num in enumerate(numbers):
        needed = target - num
        if needed in seen:
            return True
        seen[num] = i

    return False
```

---

## Challenge 8: Count Word Frequency
**Difficulty:** Medium | **Topics:** strings, dictionaries, loops

### Problem
Write a function `word_frequency(sentence)` that counts how many times each word appears. Return a dictionary. Ignore punctuation (.,!?) and work case-insensitively.

```
word_frequency("The cat sat on the mat.")
→ {'the': 2, 'cat': 1, 'sat': 1, 'on': 1, 'mat': 1}
word_frequency("hello HELLO Hello")
→ {'hello': 3}
```

### Approach
1. Strip punctuation from the sentence.
2. Split it into words.
3. For each word (lowercased), count it in a dictionary using `.get()` or by checking `if word in counts`.
4. Return the dictionary.

### Solution
```python
def word_frequency(sentence):
    # Remove punctuation
    for punct in ".,!?":
        sentence = sentence.replace(punct, "")

    words = sentence.lower().split()
    counts = {}

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts

    # Or using .get() (more compact):
    # counts = {}
    # for word in words:
    #     counts[word] = counts.get(word, 0) + 1
    # return counts
```

---

## Challenge 9: Is It an Anagram?
**Difficulty:** Medium | **Topics:** strings, dictionaries

### Problem
Write a function `is_anagram(word1, word2)` that returns `True` if the two words are anagrams of each other (same letters, same count, ignore case).

```
is_anagram("listen", "silent")   → True
is_anagram("hello", "world")     → False
is_anagram("Dormitory", "Dirty room") → True (after cleaning)
```

### Approach
1. Normalise both strings: lower case, remove spaces.
2. Build a frequency dictionary for each word.
3. Compare the two dictionaries — they're anagrams if the counts match.
4. Alternative: sort both strings and compare — if they contain the same letters, the sorted versions will be identical.

### Solution
```python
def is_anagram(word1, word2):
    # Normalise
    w1 = word1.lower().replace(" ", "")
    w2 = word2.lower().replace(" ", "")

    # Count letters
    def count_letters(word):
        counts = {}
        for char in word:
            counts[char] = counts.get(char, 0) + 1
        return counts

    return count_letters(w1) == count_letters(w2)

    # Or the cleaner approach: sort and compare
    # return sorted(w1) == sorted(w2)
```

---

## Challenge 10: Number to Words — `115 → "one hundred fifteen"`
**Difficulty:** Medium | **Topics:** dictionaries, arithmetic, conditionals

### Problem
Write a function `number_to_words(num)` that converts an integer into its English word equivalent. Handle hundreds and teens specially. Numbers will be between 0 and 999.

```
number_to_words(115)  → "one hundred fifteen"
number_to_words(7)    → "seven"
number_to_words(23)   → "twenty three"
number_to_words(99)   → "ninety nine"
number_to_words(100)  → "one hundred"
number_to_words(0)    → "zero"
```

### Approach
1. Handle `0` and the teen special cases (11–19) first.
2. Break the number: `hundreds = num // 100`, `remainder = num % 100`.
3. Map digits to words using dictionaries.
4. Build the result piece by piece and join with spaces.

### Solution
```python
def number_to_words(num):
    ones = {
        0: "zero", 1: "one", 2: "two", 3: "three", 4: "four",
        5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"
    }
    teens = {
        11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
        15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen",
        19: "nineteen"
    }
    tens = {
        2: "twenty", 3: "thirty", 4: "forty", 5: "fifty",
        6: "sixty", 7: "seventy", 8: "eighty", 9: "ninety"
    }

    if num == 0:
        return "zero"
    if 11 <= num <= 19:
        return teens[num]

    hundreds = num // 100
    remainder = num % 100

    parts = []

    if hundreds > 0:
        parts.append(ones[hundreds] + " hundred")

    if 11 <= remainder <= 19:
        parts.append(teens[remainder])
    elif remainder >= 10:
        tens_digit = remainder // 10
        ones_digit = remainder % 10
        if ones_digit == 0:
            parts.append(tens[tens_digit])
        else:
            parts.append(tens[tens_digit] + " " + ones[ones_digit])
    elif remainder > 0:
        parts.append(ones[remainder])

    return " ".join(parts)
```

---

## Challenge 11: Group Items by First Letter
**Difficulty:** Medium | **Topics:** dictionaries, lists, loops

### Problem
Write a function `group_by_letter(names)` that takes a list of names and returns a dictionary where each key is a letter (A–Z) and the value is a list of names starting with that letter.

```
group_by_letter(["Alice", "Bob", "Anna", "Brian", "Claire"])
→ {'A': ['Alice', 'Anna'], 'B': ['Bob', 'Brian'], 'C': ['Claire']}
```

### Approach
1. Start with an empty dictionary.
2. For each name, take its first letter (`name[0]`).
3. If that letter is not yet a key in the dictionary, add it with an empty list.
4. Append the name to the list for that letter.

### Solution
```python
def group_by_letter(names):
    groups = {}
    for name in names:
        first_letter = name[0].upper()
        if first_letter not in groups:
            groups[first_letter] = []
        groups[first_letter].append(name)
    return groups
```

---

## Challenge 12: Student Grade Statistics (From a File)
**Difficulty:** Medium | **Topics:** files, strings, dictionaries, lists

### Problem
Write two functions — one to **save** student grades to a file, and one to **read** them back and produce a summary dictionary showing: the class average, the highest grade, who got it, the lowest grade, and who got it.

```python
# Usage:
save_student_grades("students.csv", [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 92},
    {"name": "Charlie", "grade": 78},
])

stats = read_grade_stats("students.csv")
print(stats)
# {
#   'average': 85.0,
#   'highest': 92, 'top_student': 'Bob',
#   'lowest': 78, 'low_student': 'Charlie'
# }
```

### Approach for `save_student_grades`:
1. Open the file in write mode.
2. Write each student as a comma-separated line: `name,grade\n`.

### Approach for `read_grade_stats`:
1. Open the file in read mode.
2. Loop through each line, split by comma, parse the grade.
3. Track running totals, highest, and lowest.
4. Return the summary dictionary.

### Solution
```python
def save_student_grades(filepath, students):
    with open(filepath, "w") as f:
        for student in students:
            line = f"{student['name']},{student['grade']}\n"
            f.write(line)

def read_grade_stats(filepath):
    total = 0
    count = 0
    highest = None
    lowest = None
    top_student = ""
    low_student = ""

    with open(filepath, "r") as f:
        for line in f:
            name, grade_str = line.strip().split(",")
            grade = int(grade_str)
            total += grade
            count += 1
            if highest is None or grade > highest:
                highest = grade
                top_student = name
            if lowest is None or grade < lowest:
                lowest = grade
                low_student = name

    return {
        "average": round(total / count, 1),
        "highest": highest,
        "top_student": top_student,
        "lowest": lowest,
        "low_student": low_student
    }
```

---

---

# 📊 Quick Reference — What to Look Up

| Challenge | Key Technique | Lesson |
|-----------|--------------|--------|
| 1. Count Vowels | `for` loop + `in` condition | L2, L4 |
| 2. Reverse String | `range(len())` + list building | L2, L3, L4 |
| 3. Is Palindrome | string slicing `[::-1]` or reverse | L2 |
| 4. Sum & Max | single loop, track two values | L3, L4 |
| 5. Expand String | `isdigit()`, `zip()`, repeat | L2, L3 |
| 6. Second Largest | `set()` + `sorted()` | L3 |
| 7. Two Sum | dictionary tracking seen values | L3, L8 |
| 8. Word Frequency | `dict.get()` pattern | L4, L8 |
| 9. Is Anagram | dict frequency or `sorted()` comparison | L2, L8 |
| 10. Number to Words | `//`, `%`, dict mapping, special cases | L5, L8 |
| 11. Group by Letter | dict of lists, `append` to each key | L8 |
| 12. Grade Stats | file `open()`, `split()`, dict | L9 |

---

# ✅ All Solutions in One Place

<details>
<summary>Click to reveal all solutions (try the problems first!)</summary>

```python
# Challenge 1
def count_vowels(text):
    count = 0
    for char in text:
        if char in "aeiouAEIOU":
            count += 1
    return count

# Challenge 2
def reverse_string(text):
    result = []
    for i in range(len(text)):
        result.append(text[i])
    return "".join(reversed(result))

# Challenge 3
def is_palindrome(text):
    return text[::-1].lower() == text.lower()

# Challenge 4
def sum_and_max(numbers):
    total = 0
    largest = numbers[0]
    for num in numbers:
        total += num
        if num > largest:
            largest = num
    return (total, largest)

# Challenge 5
def expand_string(text):
    letters, digits = [], []
    for char in text:
        if char.isdigit():
            digits.append(char)
        else:
            letters.append(char)
    result = []
    for letter, digit in zip(letters, digits):
        result.append(letter * int(digit))
    return "".join(result)

# Challenge 6
def second_largest(numbers):
    unique = set(numbers)
    return sorted(unique, reverse=True)[1]

# Challenge 7
def two_sum(numbers, target):
    seen = {}
    for i, num in enumerate(numbers):
        needed = target - num
        if needed in seen:
            return True
        seen[num] = i
    return False

# Challenge 8
def word_frequency(sentence):
    for punct in ".,!?":
        sentence = sentence.replace(punct, "")
    words = sentence.lower().split()
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts

# Challenge 9
def is_anagram(word1, word2):
    w1 = word1.lower().replace(" ", "")
    w2 = word2.lower().replace(" ", "")
    return sorted(w1) == sorted(w2)

# Challenge 10
def number_to_words(num):
    ones = {0:"zero",1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight",9:"nine"}
    teens = {11:"eleven",12:"twelve",13:"thirteen",14:"fourteen",15:"fifteen",16:"sixteen",17:"seventeen",18:"eighteen",19:"nineteen"}
    tens = {2:"twenty",3:"thirty",4:"forty",5:"fifty",6:"sixty",7:"seventy",8:"eighty",9:"ninety"}
    if num == 0: return "zero"
    if 11 <= num <= 19: return teens[num]
    hundreds = num // 100
    remainder = num % 100
    parts = []
    if hundreds > 0: parts.append(ones[hundreds] + " hundred")
    if 11 <= remainder <= 19: parts.append(teens[remainder])
    elif remainder >= 10:
        td, od = remainder // 10, remainder % 10
        parts.append(tens[td] + ("" if od == 0 else " " + ones[od]))
    elif remainder > 0: parts.append(ones[remainder])
    return " ".join(parts)

# Challenge 11
def group_by_letter(names):
    groups = {}
    for name in names:
        letter = name[0].upper()
        if letter not in groups: groups[letter] = []
        groups[letter].append(name)
    return groups

# Challenge 12
def save_student_grades(filepath, students):
    with open(filepath, "w") as f:
        for s in students:
            f.write(f"{s['name']},{s['grade']}\n")

def read_grade_stats(filepath):
    total = count = highest = lowest = None
    top_student = low_student = ""
    with open(filepath) as f:
        for line in f:
            name, g = line.strip().split(",")
            grade = int(g)
            total = (total or 0) + grade
            count += 1
            if highest is None or grade > highest:
                highest, top_student = grade, name
            if lowest is None or grade < lowest:
                lowest, low_student = grade, name
    return {"average": round(total / count, 1), "highest": highest,
            "top_student": top_student, "lowest": lowest, "low_student": low_student}
```

</details>

---

Good luck, Szonja! Every tool you need is in your lesson files — go find them when you need them. 💛