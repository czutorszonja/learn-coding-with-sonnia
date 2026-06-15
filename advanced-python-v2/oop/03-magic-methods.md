# OOP Lesson 3: Making Your Objects Feel Pythonic ✨

**← Back to [Lesson 2: Polymorphism](02-polymorphism.md)**

---

## The Problem: Your Objects Feel Foreign

You've built some great classes. But they don't quite feel like Python objects yet:

```python
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

book = Book("1984", "George Orwell", 328)

print(book)
# <__main__.Book object at 0x7f8a1c0b3d90>  ← useless!

# book + book   ← TypeError
# len(book)     ← TypeError
# if book: ...  ← Always True, even if empty
```

Python doesn't know how to print your book, add two books, or check if a book is "empty." But you can teach it.

---

## The Idea: Fill In the Blanks

Python already knows what `+` means for numbers, what `print()` means, what `len()` means. The question is: what should those things mean for YOUR class?

You answer that with **magic methods** — special methods with double underscores that Python calls automatically.

| When you write… | Python calls… | Your job |
|----------------|---------------|----------|
| `print(book)` | `book.__str__()` | Return a readable string |
| `len(thing)` | `thing.__len__()` | Return the size |
| `a + b` | `a.__add__(b)` | Return the sum |
| `a == b` | `a.__eq__(b)` | Return True or False |
| `if thing:` | `thing.__bool__()` | Return True or False |
| `thing[0]` | `thing.__getitem__(0)` | Return the item at index 0 |

You're not inventing new operators. You're just telling Python: "When someone does X to my object, here's what it means."

---

## Starting Simple: `__str__` and `__repr__`

These two control what your object looks like when printed:

```python
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):
        """Called by print() and str() — for humans."""
        return f"{self.title} by {self.author}"

    def __repr__(self):
        """Called by repr() and the interactive prompt — for developers."""
        return f"Book(title={self.title!r}, author={self.author!r}, pages={self.pages})"


book = Book("1984", "George Orwell", 328)

print(book)       # 1984 by George Orwell    ← clean!
print(repr(book))  # Book(title='1984', author='George Orwell', pages=328)
```

**Rule of thumb:** `__str__` is for users. `__repr__` is for debugging. If you only write one, write `__repr__` — Python falls back to it when `__str__` is missing.

---

## Arithmetic: `__add__`, `__sub__`, `__mul__`

Let's make a Vector class that supports math:

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        """v1 + v2 — add two vectors."""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """v1 - v2 — subtract."""
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        """v * 3 — multiply by a number."""
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        """v1 == v2 — are they the same?"""
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y


v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(v1 + v2)     # Vector(4, 6)
print(v1 - v2)     # Vector(2, 2)
print(v1 * 3)      # Vector(9, 12)
print(v1 == Vector(3, 4))  # True
print(v1 == v2)    # False
```

It feels like Python. No `.add()` or `.multiply()` — just `+`, `-`, `*`.

---

## Comparisons: `__eq__`, `__lt__`, `__gt__`

```python
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __eq__(self, other):
        """Two books are equal if they have the same title and author."""
        if not isinstance(other, Book):
            return False
        return self.title == other.title and self.author == other.author

    def __lt__(self, other):
        """Book < other — compare by page count."""
        return self.pages < other.pages

    def __str__(self):
        return f"{self.title} ({self.pages}pp)"


book1 = Book("1984", "George Orwell", 328)
book2 = Book("1984", "George Orwell", 250)  # Same book, different edition
book3 = Book("Dune", "Frank Herbert", 412)

print(book1 == book2)  # True — same book!
print(book1 < book3)   # True — 328 < 412 pages

# Now sorting works automatically:
books = [book3, book1, book2]
books.sort()
for b in books:
    print(b)
# 1984 (250pp)
# 1984 (328pp)
# Dune (412pp)
```

---

## Container-Like: `__len__`, `__getitem__`, `__contains__`

```python
class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []

    def add(self, song):
        self.songs.append(song)

    def __len__(self):
        """len(playlist) — how many songs?"""
        return len(self.songs)

    def __getitem__(self, index):
        """playlist[0] — get a song by index."""
        return self.songs[index]

    def __contains__(self, song):
        """'song' in playlist — is this song here?"""
        return song in self.songs

    def __str__(self):
        return f"Playlist '{self.name}' ({len(self)} songs)"


playlist = Playlist("Chill Vibes")
playlist.add("Bohemian Rhapsody")
playlist.add("Stairway to Heaven")
playlist.add("Hotel California")

print(playlist)             # Playlist 'Chill Vibes' (3 songs)
print(len(playlist))        # 3
print(playlist[0])          # Bohemian Rhapsody

# Iteration works because of __getitem__!
for song in playlist:
    print(f"  - {song}")

print("Hotel California" in playlist)  # True
print("Despacito" in playlist)         # False
```

---

## Truthiness: `__bool__`

```python
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def __bool__(self):
        """Is this cart empty? Used by 'if cart:'"""
        return len(self.items) > 0

    def __len__(self):
        return len(self.items)


cart = ShoppingCart()
print(bool(cart))  # False

if not cart:
    print("Your cart is empty!")

cart.add("Python Book")
if cart:
    print(f"You have {len(cart)} item(s) in your cart.")
# You have 1 item(s) in your cart.
```

---

## Practice: A 2D Point

**Your task:** Create a `Point` class for 2D coordinates, and make it feel like a real Python object.

Requirements:
- `__init__(self, x, y)` — constructor
- `__str__` — returns `"Point(3, 4)"`
- `__repr__` — returns `"Point(x=3, y=4)"`
- `__add__` — `Point(1, 2) + Point(3, 4)` → `Point(4, 6)`
- `__eq__` — two points are equal if their coordinates match
- `__abs__` — `abs(point)` returns the distance from the origin `(0, 0)` → `sqrt(x² + y²)`
- `__bool__` — `bool(point)` is `True` unless the point is `(0, 0)`

**Test it:**

```python
p1 = Point(3, 4)
p2 = Point(1, 2)

print(p1)               # Point(3, 4)
print(p1 + p2)          # Point(4, 6)
print(p1 == Point(3, 4))  # True
print(abs(p1))          # 5.0
print(bool(Point(0, 0)))  # False
print(bool(p1))         # True
```

Create `point.py` and try it!

---

## Solution

```python
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    def __add__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __abs__(self):
        """Distance from origin — sqrt(x² + y²)."""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __bool__(self):
        """A point is 'truthy' unless it's at the origin."""
        return self.x != 0 or self.y != 0


# Test
p1 = Point(3, 4)
p2 = Point(1, 2)

print(p1)                   # Point(3, 4)
print(repr(p1))             # Point(x=3, y=4)
print(p1 + p2)              # Point(4, 6)
print(p1 == Point(3, 4))    # True
print(p1 == p2)             # False
print(abs(p1))              # 5.0
print(bool(Point(0, 0)))    # False
print(bool(p1))             # True
```

---

## What You Just Learned

- **Magic methods** let your objects work with Python's built-in operations
- **`__str__`** — for `print()`, human-readable
- **`__repr__`** — for debugging, developer-readable
- **`__add__` / `__sub__` / `__mul__`** — arithmetic
- **`__eq__` / `__lt__`** — comparisons, enable sorting
- **`__len__` / `__getitem__`** — make objects act like containers
- **`__bool__`** — control truthiness for `if object:`

---

## What's Next?

You can now create classes that feel like they belong in Python. The last OOP concept: **composition** — when "has-a" is better than "is-a."

Continue to **[OOP Lesson 4: Composition](04-composition.md)** 🧩

---

**Your turn:** Build the Point class! Then add `__sub__` (subtraction) and `__mul__` (multiply both coordinates by a number). Try `p1 * 2` → `Point(6, 8)`. ✨💛
