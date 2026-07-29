# Lesson 3: Cleaner Access with @property

**← Back to [Lesson 2: Protecting Your Data](02-protecting-data.md)**

---

## The Annoyance: get_this(), set_that()

Last lesson you built a `BankAccount` with `get_balance()`, `deposit()`, and `withdraw()`. It works! But using it looks like this:

```python
account = BankAccount("Szonja", 100)

# Reading the balance — looks like a function call
print(account.get_balance())  # 100

# But I can't just write:
# print(account.balance)  # AttributeError — no such attribute
```

Wouldn't it be nicer if we could write `account.balance` instead of `account.get_balance()`? Cleaner. More natural. Like reading any other attribute.

But we still need the validation! If someone writes `account.balance = -500`, we need that to fail.

Python's `@property` gives us exactly this: **attribute-like access with method-like protection.**

---

## Your First @property

Let's rewrite the bank account's balance using `@property`:

```python
class BankAccount:
    def __init__(self, owner, starting_balance=0):
        self.owner = owner
        self._balance = starting_balance    # Internal storage — still private

    @property
    def balance(self):
        """The balance, as a read-only property."""
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError(f"Deposit must be positive, got {amount}")
        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError(f"Withdrawal must be positive, got {amount}")
        if amount > self._balance:
            raise ValueError(f"Insufficient funds. Balance: {self._balance}")
        self._balance -= amount
```

Now look at the difference:

```python
account = BankAccount("Szonja", 100)

# Before: account.get_balance()
# After:
print(account.balance)  # 100 — clean, natural, no parentheses!

# Before: no way to block direct writing
# After:
# account.balance = 5000  # ❌ AttributeError — can't set, no setter defined!
```

The balance is **read-only**. The only way to change it is through `deposit()` and `withdraw()`. Perfect.

---

## How @property Actually Works

This is the part that clicked for me. `@property` is just a decorator (we'll learn more about those later). For now, think of it like this:

```python
# What you write:
@property
def balance(self):
    return self._balance

# What Python secretly does:
# balance = property(balance)
# It turns the METHOD into a PROPERTY.
# Now account.balance calls the method automatically.
```

That's it. `@property` makes a method look like an attribute. No parentheses needed when you read it.

---

## Adding a Setter

What if you WANT people to be able to write `account.balance = 100` — but with validation?

You add a **setter**:

```python
class BankAccount:
    def __init__(self, owner, starting_balance=0):
        self.owner = owner
        self._balance = starting_balance

    @property
    def balance(self):
        """Getter — runs when you READ account.balance."""
        return self._balance

    @balance.setter
    def balance(self, amount):
        """Setter — runs when you WRITE account.balance = X."""
        if amount < 0:
            raise ValueError(f"Balance cannot be negative, got {amount}")
        self._balance = amount

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError(f"Deposit must be positive")
        self._balance += amount
```

Now both reading and writing use the clean attribute syntax:

```python
account = BankAccount("Szonja", 100)

print(account.balance)    # 100 — calls the getter
account.balance = 200     # Calls the setter — validation runs!
print(account.balance)    # 200

# account.balance = -50   # ❌ ValueError: Balance cannot be negative
```

Notice the pattern:
- `@property` → the **getter** (reading)
- `@balance.setter` → the **setter** (writing)
- The name after `@` and `.setter` must match — `@balance.setter` goes with `def balance`

---

## Why This Matters

Without `@property`:
- `get_balance()` — works, but ugly
- `set_balance(x)` — works, but even uglier  
- Can't stop people from doing `account._balance = 999999`

With `@property`:
- `account.balance` — clean, natural
- `account.balance = 200` — clean, validated
- `account._balance` still accessible but clearly marked as internal

The outside of your class looks simple. The inside handles the complexity. That's good design.

---

## Practice: A Temperature Class

**Your task:** Create a `Temperature` class that stores temperature in Celsius internally, but lets you read and write in BOTH Celsius and Fahrenheit.

Requirements:
- Internal storage is `_celsius` (private)
- `celsius` property with getter and setter (the setter rejects values below -273.15)
- `fahrenheit` property — getter only (converts on the fly, no separate variable)
- `fahrenheit` setter — converts to Celsius and stores it (reuses the celsius setter's validation!)
- `kelvin` property — getter only, read-only

**Test it:**

```python
temp = Temperature(25)
print(temp.celsius)      # 25
print(temp.fahrenheit)   # 77.0
print(temp.kelvin)       # 298.15

temp.fahrenheit = 32     # Set in Fahrenheit
print(temp.celsius)      # 0.0 — converted automatically!

# temp.celsius = -300    # ❌ ValueError — below absolute zero
# temp.kelvin = 300      # ❌ AttributeError — read-only
```

Create `temperature.py` and try it!

---

## Solution

```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    # ── Celsius: getter + setter ──────────────────────

    @property
    def celsius(self):
        """Read the temperature in Celsius."""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """Set temperature in Celsius. Rejects values below absolute zero."""
        if value < -273.15:
            raise ValueError(
                f"Temperature below absolute zero! Got {value}°C"
            )
        self._celsius = value

    # ── Fahrenheit: getter + setter ───────────────────

    @property
    def fahrenheit(self):
        """Read the temperature in Fahrenheit (calculated from Celsius)."""
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        """Set temperature in Fahrenheit. Converts to Celsius (validation runs!)."""
        self.celsius = (value - 32) * 5/9   # Uses the celsius setter!

    # ── Kelvin: getter only (read-only) ──────────────

    @property
    def kelvin(self):
        """Read the temperature in Kelvin (calculated from Celsius)."""
        return self._celsius + 273.15


# Test
temp = Temperature(25)
print(f"{temp.celsius}°C = {temp.fahrenheit}°F = {temp.kelvin}K")
# 25°C = 77.0°F = 298.15K

temp.fahrenheit = 32
print(f"{temp.celsius}°C")  # 0.0°C — converted and validated!
```

---

## What You Just Learned

- **`@property` turns a method into an attribute** — read it without `()`
- **`@name.setter` adds write access** — with validation
- **No setter = read-only** — users can read but not write
- **The internal variable uses `_underscore`** — `_celsius` is the real storage
- **Setters can reuse other setters** — `fahrenheit.setter` calls `self.celsius = ...` which triggers the celsius setter's validation

---

## What's Next?

You now know how to:
- Create classes (`__init__`, `self`)
- Protect data (methods as gatekeepers, `_private`)
- Use `@property` for clean attribute access

Continue to **[Lesson 4: Sharing Behaviour with Inheritance](04-inheritance.md)** 🧬

---

**Your turn:** Build the temperature converter! Then add a `description` property that returns a human-readable string like `"Mild"` (0-15°C), `"Warm"` (15-30°C), `"Hot"` (30+°C), `"Cold"` (below 0). 🔑💛
