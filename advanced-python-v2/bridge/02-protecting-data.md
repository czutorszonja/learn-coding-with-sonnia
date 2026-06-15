# Bridge Lesson 2: Protecting Your Data 🛡️

**← Back to [Lesson 1: Why Classes?](01-why-classes.md)**

---

## The Problem: Anyone Can Mess With Your Stuff

Last lesson you built a `Book` class. It works! But there's a problem lurking:

```python
book = Book("1984", "George Orwell", 328)

# Someone does this:
book.pages = -50
print(book.info())  # 1984 by George Orwell — -50 pages
```

A book with negative pages? That's nonsense. But Python lets anyone change `book.pages` to anything — a negative number, a string, even a whole list. There's no guard at the gate.

Same thing with our Student class:

```python
szonja = Student("Szonja", "szonja@example.com", [85, 92, 78])
szonja.scores = "not a list anymore!"
print(szonja.average())  # 💥 Crash!
```

The issue: **direct access to attributes means no validation.** Anyone can set anything to anything, and your object can't stop them.

---

## The Solution: Methods as Gatekeepers

Instead of letting people touch the data directly, you give them **methods** — functions that live on the object and can check things before making changes.

Here's the idea:

```python
# ❌ Direct access — no validation possible
book.pages = -50

# ✅ Through a method — validation happens here
book.set_pages(50)   # Works
book.set_pages(-50)  # "Sorry, pages can't be negative"
```

Let's rebuild our Book class with this pattern:

```python
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self._pages = None       # Start with nothing
        self.set_pages(pages)    # Use the method so validation runs!

    def set_pages(self, pages):
        """Set the page count — but only if it makes sense."""
        if pages <= 0:
            raise ValueError(f"Pages must be positive, got {pages}")
        if not isinstance(pages, int):
            raise TypeError(f"Pages must be an integer, got {type(pages).__name__}")
        self._pages = pages

    def get_pages(self):
        """Return the page count."""
        return self._pages

    def info(self):
        return f"{self.title} by {self.author} — {self._pages} pages"
```

Now let's try to break it:

```python
book = Book("1984", "George Orwell", 328)
print(book.info())  # ✅ 1984 by George Orwell — 328 pages

book.set_pages(250)
print(book.info())  # ✅ 1984 by George Orwell — 250 pages

# book.set_pages(-50)    # ❌ ValueError: Pages must be positive, got -50
# book.set_pages("lots") # ❌ TypeError: Pages must be an integer, got str
```

The validation gates are working! Nobody can create a broken book anymore.

---

## The Underscore Convention: "Please Don't Touch"

Notice I renamed the attribute from `self.pages` to `self._pages`. That leading underscore is a Python convention that means:

> "This is internal. Please use the methods instead."

It doesn't actually prevent access — you can still do `book._pages = -50` if you really want to. But the underscore says to other programmers (and to future-you): "I'm not meant to be touched directly. Use `set_pages()` and `get_pages()`."

This is called **encapsulation** — keeping the internal state of an object private, and only exposing safe ways to interact with it.

---

## Practice: A Bank Account

The classic example — and for good reason. A bank account is the perfect case for encapsulation: you really, REALLY don't want anyone changing the balance directly.

**Your task:** Create a `BankAccount` class with:

- `owner` (string) — set once, never changes
- `_balance` (number, starts at 0) — private, use the methods!
- `deposit(amount)` — add money (must be positive)
- `withdraw(amount)` — take money out (must be positive AND can't exceed balance)
- `get_balance()` — returns the current balance
- `summary()` — returns something like `"Szonja's account: £150.00"`

**Test it:**

```python
account = BankAccount("Szonja", 100)
print(account.summary())       # Szonja's account: £100.00

account.deposit(50)
print(account.get_balance())   # 150

account.withdraw(30)
print(account.summary())       # Szonja's account: £120.00

# These should all raise errors:
# account.withdraw(500)        # Not enough money
# account.deposit(-10)         # Can't deposit negative
# account.withdraw(0)          # Can't withdraw nothing
# account._balance = 1000000   # Works but DON'T — that's cheating!
```

Create `bank_account.py` and try it!

---

## Solution

```python
class BankAccount:
    def __init__(self, owner, starting_balance=0):
        self.owner = owner
        self._balance = starting_balance

    def deposit(self, amount):
        """Add money to the account. Amount must be positive."""
        if amount <= 0:
            raise ValueError(f"Deposit must be positive, got {amount}")
        self._balance += amount
        return self._balance

    def withdraw(self, amount):
        """Take money out. Must be positive and not exceed balance."""
        if amount <= 0:
            raise ValueError(f"Withdrawal must be positive, got {amount}")
        if amount > self._balance:
            raise ValueError(
                f"Cannot withdraw {amount}. Balance is only {self._balance}"
            )
        self._balance -= amount
        return self._balance

    def get_balance(self):
        """Return the current balance."""
        return self._balance

    def summary(self):
        return f"{self.owner}'s account: £{self._balance:.2f}"


# Test
account = BankAccount("Szonja", 100)
print(account.summary())       # Szonja's account: £100.00

account.deposit(50)
print(account.get_balance())   # 150

account.withdraw(30)
print(account.summary())       # Szonja's account: £120.00
```

---

## What You Just Learned

- **Direct attribute access is dangerous** — no validation, anything goes
- **Methods act as gatekeepers** — they check the data before changing it
- **`_underscore` means "internal"** — a signal to other programmers: use the methods
- **Encapsulation** — the big word for "protect your data behind methods"

---

## What's Next?

`get_balance()` and `set_pages()` work, but they're a bit... clunky. Python has a much cleaner way to write getters and setters — `@property`. That's next.

Continue to **[Bridge Lesson 3: Cleaner Access with @property](03-property-basics.md)** 🔑

---

**Your turn:** Build the bank account! Then try adding a `transfer(amount, other_account)` method that moves money from one account to another. 🛡️💛
