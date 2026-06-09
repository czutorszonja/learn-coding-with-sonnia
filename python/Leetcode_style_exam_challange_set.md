# Algorithmic Thinking

**Topic:** Patterns for solving problems systematically — sliding window, two-pointer, stack, frequency maps

---

# Python Exam Challenge Set — LeetCode Style 🌞

**For:** Python Exam | **Open-book** — all lesson files are available to you

---

> **How each problem is structured:**
> - **Description** — what to solve
> - **Function signature** — exact code to write
> - **Examples** — test your answer by hand first
> - **Constraints** — what the input will look like (use these to think about edge cases)
> - **Follow-up** — optional harder version
> - **Approach** — how to think about it step by step
> - **Solution** — complete, working code
>
> Always trace the examples by hand before looking at the solution. That's the habit that wins exams.

---

---

# 🔥 Easy — 4 Problems

---

## Problem 1: Count Vowels

**Difficulty:** Easy | **Topic:** Strings, Loops, Conditionals

### Description
Given a string `s`, return the **number of vowels** in it. Vowels are: `a`, `e`, `i`, `o`, `u` (both upper and lowercase).

### Function Signature
```python
def count_vowels(s: str) -> int:
```

### Examples

**Example 1:**
```
Input:  s = "Hello World"
Output: 3
```

**Example 2:**
```
Input:  s = "rhythm"
Output: 0
```

**Example 3:**
```
Input:  s = "AEIOU"
Output: 5
```

### Constraints
- `1 <= len(s) <= 1000`

### Approach
1. Walk through every character in the string using a `for` loop.
2. Check if the character is in the vowel set `"aeiouAEIOU"`.
3. Increment the counter each time you find one.


## Problem 2: Reverse String

**Difficulty:** Easy | **Topic:** Strings, Loops, List Building

### Description
Given a string `s`, reverse it and return the reversed string. Do not use the built-in `reversed()` or string slicing in your logic — build the result step by step.

### Function Signature
```python
def reverse_string(s: str) -> str:
```

### Examples

**Example 1:**
```
Input:  s = "hello"
Output: "olleh"
```

**Example 2:**
```
Input:  s = "Szonja"
Output: "ajnzoS"
```

**Example 3:**
```
Input:  s = "racecar"
Output: "racecar"
```

### Constraints
- `1 <= len(s) <= 1000`

### Approach
1. Start with an empty list.
2. Loop through the string **from the last character to the first** using `range(len(s)-1, -1, -1)`.
3. Append each character to the list.
4. Join the list into a single string with `"".join()`.


## Problem 3: Valid Anagram

**Difficulty:** Easy | **Topic:** Strings, Dictionaries, Frequency Counting

### Description
Given two strings `s` and `t`, return `True` if `t` is an anagram of `s` (i.e. it contains exactly the same characters with the same frequencies, ignoring case).

### Function Signature
```python
def is_anagram(s: str, t: str) -> bool:
```

### Examples

**Example 1:**
```
Input:  s = "listen", t = "silent"
Output: True
```

**Example 2:**
```
Input:  s = "hello", t = "world"
Output: False
```

**Example 3:**
```
Input:  s = "Dormitory", t = "Dirty room"
Output: True   (after normalising: \"dormitory\" == \"dirtyroom\")
```

### Constraints
- `1 <= len(s) <= 1000`
- `s` and `t` consist only of lowercase letters and spaces

### Follow-up
Can you solve it without using a dictionary? (Hint: `sorted(string)` sorts a string's characters into a list — two anagrams produce identical sorted lists.)

### Approach
1. Normalise both strings: lower case and remove spaces.
2. Build a frequency map for `s`: for each character, count how many times it appears using `freq.get(char, 0) + 1`.
3. Build the same frequency map for `t`.
4. Return `True` if the two dictionaries are identical.


## Problem 4: Check if String Can Be a Palindrome

**Difficulty:** Easy | **Topic:** Strings, Dictionaries, Frequency Counting

### Description
Given a string `s`, return `True` if it can be rearranged to form a palindrome. Ignore case and ignore spaces. A palindrome reads the same forwards and backwards (e.g. `"racecar"`, `"ababa"`).

### Function Signature
```python
def can_form_palindrome(s: str) -> bool:
```

### Examples

**Example 1:**
```
Input:  s = "racecar"
Output: True
```

**Example 2:**
```
Input:  s = "hello"
Output: False    (h,l,o — three odds)
```

**Example 3:**
```
Input:  s = "aabbcc"
Output: True
```

**Example 4:**
```
Input:  s = "ab"
Output: True    (can be \"ba\" — one odd count is fine)
```

### Constraints
- `1 <= len(s) <= 1000`

### Approach
1. Build a frequency map of all characters (lower case, ignore spaces).
2. Count how many characters have an **odd** frequency.
3. A string can form a palindrome if it has **at most one** character with an odd count.


---

# ⚡ Medium — 4 Problems

---

## Problem 5: Longest Substring Without Repeating Characters

**Difficulty:** Medium | **Topic:** Strings, Sliding Window

### Description
Given a string `s`, find the length of the **longest substring** that does not contain any repeating characters.

### Function Signature
```python
def longest_unique_substring(s: str) -> int:
```

### Examples

**Example 1:**
```
Input:  s = "abcabcbb"
Output: 3    (substring "abc" has length 3)
```

**Example 2:**
```
Input:  s = "bbbbb"
Output: 1    (only "b" on its own)
```

**Example 3:**
```
Input:  s = "pwwkew"
Output: 3    (substring "wke" has length 3)
```

### Constraints
- `0 <= len(s) <= 1000`

### Follow-up
Can you return the substring itself, not just its length?

### Approach
1. Use a **sliding window**: a start index `left` and a current index `right` that defines the window.
2. As you expand `right`, check if the new character is already inside the window.
3. If it is, move `left` forward until the duplicate is out.
4. Track the maximum window size seen.


## Problem 6: Group Anagrams Together

**Difficulty:** Medium | **Topic:** Strings, Dictionaries, Sorting

### Description
Given a list of strings `strs`, group all anagrams together and return them as a list of lists.

### Function Signature
```python
def group_anagrams(strs: list[str]) -> list[list[str]]:
```

### Examples

**Example 1:**
```
Input:  strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
Output: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```

**Example 2:**
```
Input:  strs = [""]
Output: [[""]]
```

**Example 3:**
```
Input:  strs = ["a"]
Output: [["a"]]
```

### Constraints
- `1 <= len(strs) <= 1000`
- Each `strs[i]` consists of lowercase letters

### Approach
1. The key insight: **all anagrams of a word sort to the same string**. `"eat"`, `"tea"`, and `"ate"` all sort to `"aet"`.
2. For each word, compute its sorted form as a key.
3. Use a dictionary: key = sorted word, value = list of all words with that key.
4. Return all the dictionary values.


## Problem 7: Two Sum

**Difficulty:** Medium | **Topic:** Arrays, Dictionaries

### Description
Given a list of integers `nums` and an integer `target`, return `True` if any two numbers in `nums` add up to `target`.

### Function Signature
```python
def two_sum(nums: list[int], target: int) -> bool:
```

### Examples

**Example 1:**
```
Input:  nums = [2, 7, 11, 15], target = 9
Output: True   (2 + 7 = 9)
```

**Example 2:**
```
Input:  nums = [3, 7, 2, 15], target = 100
Output: False
```

**Example 3:**
```
Input:  nums = [3, 3], target = 6
Output: True   (3 + 3 = 6)
```

### Constraints
- `2 <= len(nums) <= 1000`

### Approach
1. For each number, figure out what you need to reach the target: `needed = target - num`.
2. Keep a dictionary of numbers you've already seen: `{number: True}`.
3. If `needed` is already in the dictionary, you found your pair — return `True`.
4. If you finish the loop, no pair exists — return `False`.


## Problem 8: Find the Missing Positive Integer

**Difficulty:** Medium | **Topic:** Arrays, Sets

### Description
Given an unsorted list of integers `nums`, find the smallest missing positive integer. (Positive means greater than 0.)

### Function Signature
```python
def first_missing_positive(nums: list[int]) -> int:
```

### Examples

**Example 1:**
```
Input:  nums = [1, 2, 0]
Output: 3
```

**Example 2:**
```
Input:  nums = [3, 4, -1, 1]
Output: 2
```

**Example 3:**
```
Input:  nums = [7, 8, 9, 11, 12]
Output: 1    (1 is missing)
```

### Constraints
- `1 <= len(nums) <= 1000`
- The numbers may be negative or zero

### Approach
1. Put all positive numbers in a set (a set automatically removes duplicates).
2. Start from `1` and keep checking `i + 1` — the first number not in the set is the answer.


---

# 🔥 Hard — 2 Problems

---

## Problem 9: Longest Palindromic Substring

**Difficulty:** Hard | **Topic:** Strings, Two-Pointer (Expand Around Centre)

### Description
Given a string `s`, find the longest substring that is a palindrome.

### Function Signature
```python
def longest_palindrome(s: str) -> str:
```

### Examples

**Example 1:**
```
Input:  s = "babad"
Output: "bab"    (also valid: "aba")
```

**Example 2:**
```
Input:  s = "cbbd"
Output: "bb"
```

### Constraints
- `1 <= len(s) <= 1000`

### Follow-up
Return its length instead of the substring itself. (Then the approach simplifies to just tracking `max_len`.)

### Approach (Two-Pointer: Expand Around Centre)

**The key insight:** Every palindrome has a centre. For odd-length palindromes the centre is a single character ("bab" — centre is `b`). For even-length palindromes the centre is between two characters ("baab" — centre is between the two `a`s).

**Algorithm:**
1. For each possible centre position in the string, try to expand outward while the characters match.
2. Keep track of the longest palindrome found.
3. The trick: for position `i` in the string, check two cases:
   - Odd palindrome: centre at `i` (check `s[i-left]` vs `s[i+right]`)
   - Even palindrome: centre between `i` and `i+1` (check `s[i-1-left]` vs `s[i+right]`)


## Problem 10: Valid Parentheses

**Difficulty:** Hard | **Topic:** Strings, Stack

### Description
Given a string `s` containing only the characters `(`, `[`, `{`, `)`, `]`, `}`, determine if the brackets are **balanced**. Every opening bracket must have a matching closing bracket of the same type, and no bracket may be closed before its matching opener is closed.

### Function Signature
```python
def is_valid_parentheses(s: str) -> bool:
```

### Examples

**Example 1:**
```
Input:  s = "()"
Output: True
```

**Example 2:**
```
Input:  s = "()[]{}"
Output: True
```

**Example 3:**
```
Input:  s = "(]"
Output: False
```

**Example 4:**
```
Input:  s = "([{}])"
Output: True
```

**Example 5:**
```
Input:  s = "([)]"
Output: False
```

### Constraints
- `1 <= len(s) <= 1000`
- The string contains only `(`, `)`, `[`, `]`, `{`, `}`

### Approach (Stack)

**The key insight:** A stack is a **LIFO** structure — last item in is the first item out. This perfectly matches bracket matching:
- When you see an **opening** bracket, **push** it onto the stack.
- When you see a **closing** bracket, **pop** from the stack and check the popped value is the matching opener.

**Algorithm:**
1. Map each closing bracket to its opener: `')': '(', ']': '[', '}': '{'`.
2. Create an empty stack.
3. For each character in the string:
   - If it's an opening bracket (`(`, `[`, `{`): push it onto the stack.
   - If it's a closing bracket: try to pop from the stack. If the stack is empty or the popped item isn't the matching opener → return `False`.
4. Return `True` only if the stack is **empty** at the end (no unmatched openers left).


---

# 📊 Quick Reference — Lesson Lookup

| Problem | Key Technique | Lesson |
|---------|--------------|--------|
| 1. Count Vowels | `for` loop + `in` condition | L2, L4 |
| 2. Reverse String | `range(len())` + list building + `"".join()` | L2, L3, L4 |
| 3. Valid Anagram | frequency map with `dict.get()` | L8 |
| 4. Palindrome Form | frequency map — count of odd chars ≤ 1 | L8 |
| 5. Longest Unique Substring | sliding window + dictionary | L8 |
| 6. Group Anagrams | `sorted(strings, key=...)` as dict key | L3, L8 |
| 7. Two Sum | dictionary of seen numbers | L8 |
| 8. Missing Positive | `set()` for positive numbers | L3 |
| 9. Longest Palindrome | two-pointer expand-around-centre | L7 (algorithmic thinking) |
| 10. Valid Parentheses | **stack** — push openers, pop and match | L5, L8 |

---

---

# ✅ Solutions with Explanations

<details>
<summary>Click to reveal solutions (try the problems first!)</summary>

```python
# Problem 1: Count Vowels
def count_vowels(s: str) -> int:
    count = 0                        # Start at zero
    for char in s:                   # Walk through each character
        if char in "aeiouAEIOU":     # Check if it's a vowel (both cases)
            count += 1               # Increment when we find one
    return count                     # Return the total


# Problem 2: Reverse String
def reverse_string(s: str) -> str:
    result = []                      # Build the answer in a list
    # Loop backwards: from last index down to 0, stepping -1
    for i in range(len(s) - 1, -1, -1):
        result.append(s[i])          # Add each character in reverse order
    return "".join(result)           # Join list into a single string


# Problem 3: Valid Anagram
def is_anagram(s: str, t: str) -> bool:
    # Normalise both strings: lowercase, remove spaces
    s = s.lower().replace(" ", "")
    t = t.lower().replace(" ", "")

    # Build a frequency map for s
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1  # Count each character

    # Subtract characters of t from the frequency map
    for c in t:
        if c not in freq:              # Character wasn't in s at all
            return False
        freq[c] -= 1                   # Use up one occurrence
        if freq[c] == 0:
            del freq[c]                # Clean up empty entries

    # If the map is empty, both strings had the same characters
    return len(freq) == 0


# Problem 4: Can Form a Palindrome
def can_form_palindrome(s: str) -> bool:
    s = s.lower().replace(" ", "")    # Normalise

    # Count how many times each character appears
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1

    # Count how many characters appear an odd number of times
    odd_count = 0
    for count in freq.values():
        if count % 2 == 1:
            odd_count += 1

    # A palindrome can have at most one character with odd frequency
    return odd_count <= 1


# Problem 5: Longest Substring Without Repeating Characters
def longest_unique_substring(s: str) -> int:
    char_index = {}                    # Store the most recent index of each char
    left = 0                           # Left edge of our sliding window
    max_len = 0                        # Track the longest valid window seen

    for right in range(len(s)):        # Right edge expands one step at a time
        char = s[right]
        # If this char was already inside our window, move left edge past it
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1

        char_index[char] = right       # Update char's most recent position

        # Check if current window is the longest we've seen
        current_len = right - left + 1
        if current_len > max_len:
            max_len = current_len

    return max_len


# Problem 6: Group Anagrams Together
def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups = {}                        # sorted word -> list of anagram words

    for word in strs:
        # All anagrams of a word sort to the same string!
        # "eat", "tea", "ate" all become "aet" when sorted
        sorted_key = "".join(sorted(word))

        # Add this word to its anagram group
        if sorted_key not in groups:
            groups[sorted_key] = []
        groups[sorted_key].append(word)

    # Return just the groups (the keys themselves are just helpers)
    return list(groups.values())


# Problem 7: Two Sum (check if any pair adds to target)
def two_sum(nums: list[int], target: int) -> bool:
    seen = {}                          # Numbers we've already visited

    for num in nums:
        needed = target - num          # What would complete this pair?
        if needed in seen:             # We already saw the complement!
            return True
        seen[num] = True               # Remember this number for future checks

    return False                       # No pair found


# Problem 8: First Missing Positive Integer
def first_missing_positive(nums: list[int]) -> int:
    # Keep only positive numbers — negatives and zeros don't matter
    positives = set(n for n in nums if n > 0)

    # Start from 1 and find the first missing one
    i = 1
    while True:
        if i not in positives:
            return i                   # This positive integer is missing!
        i += 1                         # Check the next one


# Problem 9: Longest Palindromic Substring
def longest_palindrome(s: str) -> str:
    longest = ""                        # Store the longest palindrome found

    for i in range(len(s)):            # Try every position as potential centre
        # --- ODD-length palindrome (centre is a single character) ---
        left, right = i, i
        # Expand outward while characters match
        while left >= 0 and right < len(s) and s[left] == s[right]:
            # Check if this palindrome beats our current record
            if right - left + 1 > len(longest):
                longest = s[left:right + 1]
            left -= 1                  # Expand leftwards
            right += 1                 # Expand rightwards

        # --- EVEN-length palindrome (centre is between two characters) ---
        left, right = i, i + 1
        while left >= 0 and right < len(s) and s[left] == s[right]:
            if right - left + 1 > len(longest):
                longest = s[left:right + 1]
            left -= 1
            right += 1

    return longest


# Problem 10: Valid Parentheses
def is_valid_parentheses(s: str) -> bool:
    # Map each closing bracket to its matching opening bracket
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []                         # LIFO stack for open brackets

    for char in s:
        if char in "([{":             # Opening bracket — push onto stack
            stack.append(char)
        else:                          # Closing bracket — must match top of stack
            if not stack:              # Nothing to match — invalid
                return False
            top = stack.pop()          # Get the most recent opener
            if pairs[char] != top:      # Wrong type of bracket
                return False

    # All brackets matched only if the stack is empty at the end
    return len(stack) == 0
```

</details>

---

Good luck, Szonja! Every technique is in your lesson files — go find it before you start each problem. 💛