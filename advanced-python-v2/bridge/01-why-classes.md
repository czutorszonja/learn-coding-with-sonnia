# Bridge Lesson 1: Why Classes? 🤔

---

## The Mess We're Trying to Fix

You've been writing Python for a while now. You've built things with lists, dictionaries, and functions. That's powerful! But let me show you a problem that starts to hurt once your programs grow.

Imagine you're building a program to track students:

```python
# Student 1
student1_name = "Szonja"
student1_email = "szonja@example.com"
student1_scores = [85, 92, 78]

# Student 2
student2_name = "Arthur"
student2_email = "arthur@example.com"
student2_scores = [90, 88, 95]

# Calculate Szonja's average
total = 0
for score in student1_scores:
    total += score
average = total / len(student1_scores)
print(f"{student1_name}: {average}")

# Now do the same for Arthur... copy-paste the same code?
```

This works for 2 students. What about 50? What about 500?

You might think: "I'll use a dictionary!"

```python
szonja = {
    "name": "Szonja",
    "email": "szonja@example.com",
    "scores": [85, 92, 78]
}

def get_average(student):
    scores = student["scores"]
    return sum(scores) / len(scores)

print(get_average(szonja))  # 85.0
```

Better! But there's still a problem lurking...

What happens when someone creates a student but forgets the `"scores"` key?

```python
bad_student = {"name": "Oops", "email": "oops@test.com"}
print(get_average(bad_student))  # 💥 KeyError: 'scores'
```

Or what if someone types `"scors"` instead of `"scores"`?

```python
typo_student = {"name": "Typos", "email": "t@test.com", "scors": [1, 2, 3]}
print(get_average(typo_student))  # 💥 KeyError: 'scores'
```

The problem: **dictionaries don't enforce any structure.** They'll happily accept whatever keys you give them, and you only find out something's wrong when your code crashes.

---

## The Idea: Data That Knows Its Own Shape

What if we could create a "student" that:
- Always has a name, email, and scores — no missing fields, no typos
- Knows how to calculate its own average — no separate function needed
- Can't accidentally be created in a broken state

This is exactly what **classes** give you.

A class is like a **blueprint**. It defines:
- What data every student MUST have (name, email, scores)
- What every student CAN do (calculate their average)

Once you have the blueprint, you create individual students from it — each with their own name and scores, but all guaranteed to have the same structure.

---

## Your First Class

Here's the simplest possible class. Read it once slowly — I'll explain every line:

```python
class Student:
    def __init__(self, name, email, scores):
        self.name = name
        self.email = email
        self.scores = scores

    def average(self):
        return sum(self.scores) / len(self.scores)
```

That's it. Now let's use it:

```python
szonja = Student("Szonja", "szonja@example.com", [85, 92, 78])
arthur = Student("Arthur", "arthur@example.com", [90, 88, 95])

print(szonja.name)       # Szonja
print(szonja.average())  # 85.0
print(arthur.average())  # 91.0
```

Notice:
- Creating a student REQUIRES a name, email, AND scores. You can't accidentally leave one out — Python won't let you.
- Each student knows how to calculate its own average. You don't need a separate function.
- The data and the behaviour live together — everything about a student is in one place.

---

## What's Actually Happening? Let's Demystify It

### `class Student:`

This line says "I'm creating a new blueprint called Student." Nothing happens yet — no students exist. It's just the design.

### `def __init__(self, name, email, scores):`

This is a special function that runs when you CREATE a student. It's called the **constructor** or **initialiser**.

The double underscores (`__`) are Python's way of saying "this is built-in magic, not something you made up." You'll see this pattern a lot: `__init__`, `__str__`, `__len__` — all built-in hooks.

### `self.name = name`

OK, this is the one line that confuses almost everyone at first. Let me break it down with a concrete example.

When you write:

```python
szonja = Student("Szonja", "szonja@example.com", [85, 92, 78])
```

Python secretly does this:

```
1. Create a blank Student object
2. Call Student.__init__(that_blank_object, "Szonja", "szonja@example.com", [85, 92, 78])
3. Inside __init__, 'self' IS that blank object
4. self.name = "Szonja"  →  stamps the name onto this specific student
5. self.email = "szonja@example.com"  →  stamps the email
6. self.scores = [85, 92, 78]  →  stamps the scores
7. Return the now-filled-in student
```

**`self` means "this specific instance."** It's how the student knows "my name is Szonja, not Arthur."

Think of it like filling out a form:
- The blank form = the class
- Filling in YOUR details = `__init__`
- The filled form with YOUR name on it = an instance, where `self` refers to YOU

---

## A Small Practice: The Book Class

Before we move on, try this one yourself. It's the same pattern as Student — just different data.

**Your task:** Create a `Book` class with:
- `title` (string)
- `author` (string)
- `pages` (integer)
- A method called `info()` that returns something like: `"1984 by George Orwell — 328 pages"`

**Test it:**

```python
book = Book("1984", "George Orwell", 328)
print(book.info())  # 1984 by George Orwell — 328 pages
```

Try writing it in a file called `book.py`. The solution is below, but really try it first — it's the same pattern you just learned!

---

## Solution

```python
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def info(self):
        return f"{self.title} by {self.author} — {self.pages} pages"


# Test it
book = Book("1984", "George Orwell", 328)
print(book.info())
```

If your solution looks different but works — that's great! There's no single right way. If it doesn't work, compare yours to this one and spot the difference.

---

## What You Just Learned

- **A class is a blueprint** — it defines what data something has and what it can do
- **`__init__` is the constructor** — it runs when you create a new object, setting up its data
- **`self` means "this specific one"** — it's how each object keeps track of its own stuff
- **Classes prevent broken data** — you can't create a Book without a title, and you can't accidentally use the wrong key name

---

## What's Next?

Now that you can create a basic class, the next question is: **how do you protect the data inside it?**

Right now, anyone can do `book.pages = "banana"` and break everything. Next lesson: **encapsulation** — how to keep your objects' data safe.

Continue to **[Bridge Lesson 2: Protecting Your Data](02-protecting-data.md)** 🛡️

---

**No rush.** Sit with this one until `self` feels natural. It's the foundation everything else builds on. 💛
