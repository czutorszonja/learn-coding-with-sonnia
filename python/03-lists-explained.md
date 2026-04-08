# Python Lesson 3: Lists — Storing Multiple Items

## What is a List?

**Plain English:** A list is like a shopping list — one variable that holds multiple items in order.

**Real-world analogy:** Instead of having separate variables for each item you need to buy:
```python
# The hard way (don't do this!)
item1 = "milk"
item2 = "eggs"
item3 = "bread"
item4 = "butter"
```

You can put them all in one list:
```python
# The easy way!
shopping_list = ["milk", "eggs", "bread", "butter"]
```

---

## Creating a List

Lists use **square brackets** `[ ]` and items are separated by **commas**:

```python
# List of strings
names = ["Szonja", "Arthur", "Emma", "David"]

# List of numbers
ages = [25, 30, 35, 40]

# List of booleans
answers = [True, False, True, True]

# Mixed types (you can mix, but usually keep it simple)
mixed = ["hello", 42, True, 3.14]
```

---

## Accessing Items in a List

Each item has a **position number** called an **index**. Here's the tricky part: **Python starts counting at 0, not 1!**

```python
fruits = ["apple", "banana", "cherry", "date"]

# Access items by index
print(fruits[0])  # Output: apple (first item!)
print(fruits[1])  # Output: banana
print(fruits[2])  # Output: cherry
print(fruits[3])  # Output: date
```

**Visual:**
```
Index:    0        1        2        3
        ["apple", "banana", "cherry", "date"]
```

### Negative Indexes

You can also count from the **end** using negative numbers:

```python
fruits = ["apple", "banana", "cherry", "date"]

print(fruits[-1])  # Output: date (last item)
print(fruits[-2])  # Output: cherry (second from last)
```

---

## Changing Items in a List

Lists are **mutable** — you can change them after creating them:

```python
colors = ["red", "blue", "green"]

# Change an item
colors[1] = "yellow"
print(colors)  # Output: ["red", "yellow", "green"]

# The blue became yellow!
```

---

## Adding Items to a List

### Add to the end with `.append()`:

```python
fruits = ["apple", "banana"]
fruits.append("cherry")
print(fruits)  # Output: ["apple", "banana", "cherry"]
```

### Add anywhere with `.insert()`:

```python
fruits = ["apple", "cherry"]
fruits.insert(1, "banana")  # Insert at index 1
print(fruits)  # Output: ["apple", "banana", "cherry"]
```

---

## Removing Items from a List

### Remove by value with `.remove()`:

```python
colors = ["red", "blue", "green"]
colors.remove("blue")
print(colors)  # Output: ["red", "green"]
```

### Remove by index with `del`:

```python
colors = ["red", "blue", "green"]
del colors[0]  # Remove first item
print(colors)  # Output: ["blue", "green"]
```

### Remove and get the item with `.pop()`:

```python
fruits = ["apple", "banana", "cherry"]
last_fruit = fruits.pop()  # Removes and returns last item
print(last_fruit)  # Output: cherry
print(fruits)      # Output: ["apple", "banana"]
```

---

## Useful List Functions

```python
numbers = [5, 2, 8, 1, 9]

# Length of list
print(len(numbers))  # Output: 5

# Sort the list
numbers.sort()
print(numbers)  # Output: [1, 2, 5, 8, 9]

# Reverse the list
numbers.reverse()
print(numbers)  # Output: [9, 8, 5, 2, 1]

# Find minimum and maximum
print(min(numbers))  # Output: 1
print(max(numbers))  # Output: 9
```

---

## Practice Exercise

**Scenario:** You're making a playlist for a road trip!

1. Create a list called `playlist` with 5 songs (just use song titles as strings)
2. Print the first song in the list using an f-string (e.g., `print(f"First song: {playlist[0]}")`)
3. Print the last song in the list using an f-string and negative index (e.g., `print(f"Last song: {playlist[-1]}")`)
4. Add a new song to the end of the list
5. Change the second song to something else
6. Print the final playlist in two ways:
   - First, print it directly (to see the brackets and quotes)
   - Then, print it nicely using `.join()` (e.g., `print(", ".join(playlist))`) using an f-string (e.g., `print(f"Final playlist: {playlist}")`)

**Try it yourself first!** Scroll down when ready.

---

## Solution

```python
# Create playlist with 5 songs
playlist = ["Bohemian Rhapsody", "Hotel California", "Imagine", "Hey Jude", "Like a Rolling Stone"]

# Print first song
print(f"First song: {playlist[0]}")

# Print last song (using negative index)
print(f"Last song: {playlist[-1]}")

# Add a new song to the end
playlist.append("Stairway to Heaven")

# Change the second song
playlist[1] = "Sweet Child O' Mine"

# Print final playlist directly (with brackets)
print(f"Final playlist (raw): {playlist}")

# Print final playlist nicely (comma-separated)
print(f"Final playlist: {', '.join(playlist)}")
```

**Output:**
```
First song: Bohemian Rhapsody
Last song: Like a Rolling Stone
Final playlist (raw): ['Bohemian Rhapsody', 'Sweet Child O' Mine', 'Imagine', 'Hey Jude', 'Like a Rolling Stone', 'Stairway to Heaven']
Final playlist: Bohemian Rhapsody, Hotel California, Imagine, Hey Jude, Like a Rolling Stone, Stairway to Heaven
```

---

## Printing Lists Nicely

When you print a list directly, Python shows it with brackets and quotes:

```python
playlist = ["Yesterday", "Girl", "Bohemian Rhapsody"]
print(playlist)
# Output: ['Yesterday', 'Girl', 'Bohemian Rhapsody']
```

That's not very pretty! Here are two ways to make it look nicer:

### Option 1: Join items with commas

Use `.join()` to combine list items into a single string with a separator:

```python
playlist = ["Yesterday", "Girl", "Bohemian Rhapsody"]
formatted = ", ".join(playlist)
print(formatted)
# Output: Yesterday, Girl, Bohemian Rhapsody
```

**How it works:**
- `", "` is the separator (comma + space)
- `.join(playlist)` combines all items into one string
- You can use any separator: `" - ".join(playlist)` → `Yesterday - Girl - Bohemian Rhapsody`

### Option 2: Print each item on its own line (using a loop)

You can also print each item separately using a **loop** (Lesson 4 covers this):

```python
playlist = ["Yesterday", "Girl", "Bohemian Rhapsody"]

for song in playlist:
    print(song)

# Output:
# Yesterday
# Girl
# Bohemian Rhapsody
```

---

## Quick Recap

- **Lists** store multiple items in one variable
- Use **square brackets**: `[item1, item2, item3]`
- **Index starts at 0** (not 1!)
- **Negative indexes** count from the end: `[-1]` is last item
- **`.append()`** adds to the end
- **`.insert()`** adds at a specific position
- **`.remove()`** removes by value
- **`.pop()`** removes and returns an item
- **`.sort()`** sorts the list
- **`.reverse()`** reverses the list

---

## What's Next?

Lesson 4 will cover **loops** — how to do something for every item in a list (like printing all songs in your playlist without writing 10 print statements!).

---

**Your turn:** Try the playlist exercise! Make it fun — use your actual favorite songs if you want! 🎵💛
