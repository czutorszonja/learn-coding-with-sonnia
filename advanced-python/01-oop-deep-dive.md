# Advanced Python Lesson 1: Object-Oriented Programming Deep Dive 🏛️

---

## What is OOP Really About?

**Plain English:** OOP is a way of organising code by bundling _data_ and the _behaviour that works on that data_ into objects. Instead of separate lists and functions floating around, you have objects that know their own state and what they can do.

**Real-world analogy:** Think of a coffee machine:
- It has _state_ (water level, bean count, temperature)
- It has _behaviour_ (brew, steam milk, clean)
- You don't need to know how the pump works internally — you just press "espresso"
- The machine _encapsulates_ all that complexity behind a simple interface

---

## The Four Pillars

### 1. Encapsulation — Hiding the Mess

Keep internal state _private_ and expose only what's needed.

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance        # Protected — "please don't touch directly"
        self.__transaction_log = []    # Private — name-mangled to _BankAccount__transaction_log

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount
        self.__transaction_log.append(f"DEPOSIT: +{amount}")
        return self._balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self.__transaction_log.append(f"WITHDRAW: -{amount}")
        return self._balance

    # @property turns a method into a GETTER — you call it without ():
    #   account.balance   (instead of account.get_balance())
    # @name.setter turns a method into a SETTER — you assign without ():
    #   account.balance = 100   (instead of account.set_balance(100))
    #
    # (Note: @property is a decorator — Lesson 6 covers how they work.
    #  For now, just know: @property = getter, @name.setter = setter.)
    #
    # Here we only define GETTERS — no setters — so these are READ-ONLY.
    # The only way to change the balance is through deposit()/withdraw().

    @property
    def balance(self):
        """Getter — read access. No setter → can't do account.balance = X."""
        return self._balance

    @property
    def last_transaction(self):
        """Getter — returns the most recent transaction, or None."""
        # Ternary: <value_if_true> if <condition> else <value_if_false>
        #
        # "the last element if the log has entries, otherwise None"
        #
        # Empty list [] is "falsy" → evaluates to False → returns None.
        # Non-empty list is "truthy" → evaluates to True → returns [-1].
        # Without this guard, indexing an empty list raises IndexError.
        return self.__transaction_log[-1] if self.__transaction_log else None


# ✅ Only way to change balance is through deposit/withdraw
account = BankAccount("Szonja", 100)
account.deposit(50)
account.withdraw(30)
print(account.balance)   # 120 — property getter, no () needed

# account.balance = 5000  # ❌ AttributeError — no setter, read-only!
# account._balance = 1000000  # ⚠️ Possible but breaks encapsulation
# account.__transaction_log  # ❌ AttributeError — truly private
```

### 2. Inheritance — "Is-a" Relationships

"Is-a" is a quick test for when inheritance makes sense. If you can say "X IS a Y" naturally, use inheritance:

  - An **ElectricCar** *is-a* **Vehicle** → inheritance ✅
  - A **Dog** *is-an* **Animal** → inheritance ✅

The companion concept is **"Has-a"** — when something *contains* another thing (composition):

  - A **Car** *has-an* **Engine** → composition, not inheritance
  - A **BankAccount** *has-a* **transaction log** → composition

A child class _inherits_ everything from its parent and can extend or override.

```python
class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self._odometer = 0

    def drive(self, distance):
        self._odometer += distance
        return f"Drove {distance}km. Total: {self._odometer}km"

    def info(self):
        return f"{self.year} {self.make} {self.model}"


class ElectricCar(Vehicle):
    def __init__(self, make, model, year, battery_kwh):
        super().__init__(make, model, year)  # Call parent's __init__
        self.battery_kwh = battery_kwh
        self._charge = 100

    def drive(self, distance):
        """Override — electric cars consume charge."""
        consumption = distance * 0.2  # 0.2 kWh per km
        if consumption > self._charge:
            return "Not enough charge!"
        self._charge -= consumption
        return super().drive(distance)  # Still update odometer

    def charge(self):
        self._charge = 100
        return "Fully charged! 🔋"

    def info(self):
        return f"{super().info()} — {self.battery_kwh}kWh EV"


class Motorcycle(Vehicle):
    def drive(self, distance):
        return f"🏍️ {super().drive(distance)}"


# Polymorphism — same interface, different behaviour
vehicles = [
    ElectricCar("Tesla", "Model 3", 2024, 75),
    Motorcycle("Ducati", "Monster", 2023),
]

for v in vehicles:
    print(v.info())
    print(v.drive(50))
    print()
```

### 3. Polymorphism — Same Interface, Different Behaviour

```python
class Animal:
    def speak(self):
        raise NotImplementedError("Subclass must implement speak()")


class Dog(Animal):
    def speak(self):
        return "Woof! 🐕"


class Cat(Animal):
    def speak(self):
        return "Meow! 🐱"


class Duck(Animal):
    def speak(self):
        return "Quack! 🦆"


def animal_chorus(animals):
    """Works with ANY Animal subclass — polymorphism!"""
    for animal in animals:
        print(f"{animal.__class__.__name__}: {animal.speak()}")


animal_chorus([Dog(), Cat(), Duck(), Dog()])
# Dog: Woof! 🐕
# Cat: Meow! 🐱
# Duck: Quack! 🦆
# Dog: Woof! 🐕
```

### 4. Abstraction — Hiding Complexity

```python
from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """Abstract base class — defines the interface."""

    @abstractmethod
    def validate_payment(self, amount):
        pass

    @abstractmethod
    def process_payment(self, amount):
        pass

    def pay(self, amount):
        """Template method — the workflow is fixed."""
        if not self.validate_payment(amount):
            return "Payment validation failed"
        result = self.process_payment(amount)
        self.log_transaction(amount, result)
        return result

    def log_transaction(self, amount, result):
        print(f"[LOG] Payment of {amount} — {result}")


class CreditCardProcessor(PaymentProcessor):
    def __init__(self, card_number):
        self.card_number = card_number
        self._limit = 5000

    def validate_payment(self, amount):
        return amount <= self._limit

    def process_payment(self, amount):
        last_four = self.card_number[-4:]
        return f"Charged {amount} to card ****{last_four}"


class PayPalProcessor(PaymentProcessor):
    def __init__(self, email):
        self.email = email

    def validate_payment(self, amount):
        return amount > 0

    def process_payment(self, amount):
        return f"Sent {amount} via PayPal to {self.email}"


# Same interface, completely different internals
cc = CreditCardProcessor("4111111111111111")
pp = PayPalProcessor("szonja@example.com")

print(cc.pay(100))   # Charged 100 to card ****1111
print(pp.pay(100))   # Sent 100 via PayPal to szonja@example.com
print(pp.pay(6000))  # Payment validation failed (for CC — limit exceeded)
```

---

## Magic Methods — Making Your Objects Pythonic

Python already knows what `+` means for numbers, what `print()` means, what `==` means.
**Dunder methods (double underscore methods like `__add__`) are how you teach Python what those things mean for YOUR class.**

You're not inventing anything new. You're just filling in the blank:

| When someone writes… | Python calls… |
|---|---|
| `v1 + v2` | `__add__` |
| `v1 - v2` | `__sub__` |
| `v1 * 3` | `__mul__` |
| `3 * v1` | `__rmul__` (reversed) |
| `v1 == v2` | `__eq__` |
| `abs(v1)` | `__abs__` |
| `if v1:` | `__bool__` |
| `len(v1)` | `__len__` |
| `print(v1)` | `__str__` |
| `v1[0]` | `__getitem__` |
| `for coord in v1:` | `__iter__` |

If you never define `__add__` and try `v1 + v2`, Python crashes with `TypeError: unsupported operand type(s) for +`. You're just telling Python what to do when it sees those operators on your objects.

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        """Human-readable — print() and str()"""
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):
        """Unambiguous — repr() and debug output"""
        return f"Vector({self.x!r}, {self.y!r})"

    def __add__(self, other):
        """v1 + v2"""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        """v1 - v2"""
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        """v * 3 — scalar multiplication"""
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        """3 * v — reflected multiplication"""
        return self.__mul__(scalar)

    def __eq__(self, other):
        """v1 == v2"""
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y

    def __abs__(self):
        """abs(v) — magnitude"""
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __bool__(self):
        """bool(v) — truthiness"""
        return self.x != 0 or self.y != 0

    def __len__(self):
        """len(v) — number of dimensions"""
        return 2

    def __getitem__(self, index):
        """v[0], v[1]"""
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError("Vector index out of range")

    def __iter__(self):
        """for coord in v:"""
        yield self.x
        yield self.y


v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(v1)               # Vector(3, 4)
print(v1 + v2)          # Vector(4, 6)
print(v1 * 3)           # Vector(9, 12)
print(3 * v1)           # Vector(9, 12)  — thanks to __rmul__
print(abs(v1))          # 5.0
print(bool(Vector(0, 0)))  # False
print(v1 == Vector(3, 4))  # True

for coord in v1:
    print(coord)        # 3, then 4
```

---

## Composition vs Inheritance

**Inheritance:** "A Car _is a_ Vehicle"
**Composition:** "A Car _has an_ Engine"

```python
class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower
        self._running = False

    def start(self):
        self._running = True
        return "Vroom! 🔥"

    def stop(self):
        self._running = False
        return "...silence"

    @property
    def is_running(self):
        return self._running


class Wheels:
    def __init__(self, count=4):
        self.count = count
        self._pressure = [32] * count  # PSI

    def inflate(self, wheel_index, psi):
        self._pressure[wheel_index] = psi

    @property
    def all_ok(self):
        return all(28 <= p <= 36 for p in self._pressure)


class Car:
    """Composition: Car HAS an Engine, HAS Wheels."""
    def __init__(self, make, model, horsepower):
        self.make = make
        self.model = model
        self.engine = Engine(horsepower)  # Composition!
        self.wheels = Wheels(4)           # Composition!

    def start(self):
        if not self.wheels.all_ok:
            return "⚠️ Check tyre pressure!"
        return self.engine.start()

    def stop(self):
        return self.engine.stop()


my_car = Car("Mini", "Cooper", 134)
print(my_car.start())  # Vroom! 🔥
print(my_car.engine.horsepower)  # 134
```

**Rule of thumb:** Prefer composition over inheritance. Only use inheritance when there's a genuine "is-a" relationship.

---

## Class Methods and Static Methods

```python
class Pizza:
    # Class-level constant
    BASE_PRICE = 8.00
    TOPPING_PRICE = 1.50

    def __init__(self, size, toppings=None):
        self.size = size          # "small", "medium", "large"
        self.toppings = toppings or []

    def price(self):
        """Instance method — uses self."""
        size_multiplier = {"small": 0.8, "medium": 1.0, "large": 1.3}
        topping_cost = len(self.toppings) * self.TOPPING_PRICE
        return self.BASE_PRICE * size_multiplier[self.size] + topping_cost

    @classmethod
    def margherita(cls, size="medium"):
        """Class method — factory for a common pizza type."""
        return cls(size, ["mozzarella", "basil"])

    @classmethod
    def pepperoni(cls, size="medium"):
        return cls(size, ["mozzarella", "pepperoni"])

    @staticmethod
    def is_valid_size(size):
        """Static method — no self or cls needed."""
        return size in ("small", "medium", "large")

    def __str__(self):
        toppings_str = ", ".join(self.toppings) if self.toppings else "plain"
        return f"{self.size} pizza with {toppings_str} — £{self.price():.2f}"


# Use class methods as factories
marg = Pizza.margherita("large")
pep = Pizza.pepperoni()

print(marg)  # large pizza with mozzarella, basil — £10.90
print(pep)   # medium pizza with mozzarella, pepperoni — £10.00

# Use static method for validation
print(Pizza.is_valid_size("medium"))  # True
print(Pizza.is_valid_size("extra large"))  # False
```

---

## Property Decorators — Controlled Attribute Access

Now that you've seen read-only getters, here's the full pattern: **getters AND setters**.

| Role | What it does | Without @property | With @property |
|------|-------------|-------------------|----------------|
| **Getter** | Read a value | `get_balance()` | `balance` (no `()`) |
| **Setter** | Write a value | `set_balance(x)` | `balance = x` |

(`@property` is a decorator — more on those in Lesson 6.)

```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius  # Internal storage — use the properties instead

    # ─── celsius: getter + setter ─────────────────────────────

    @property
    def celsius(self):
        """Getter — temp.celsius (no parentheses)"""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """Setter — temp.celsius = 25"""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value

    # ─── fahrenheit: computed from celsius ────────────────────

    @property
    def fahrenheit(self):
        """Getter — calculated on the fly, no separate variable."""
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        """Setter — converts to celsius, reuses the celsius setter's validation."""
        self.celsius = (value - 32) * 5/9

    # ─── kelvin: getter only (read-only) ──────────────────────

    @property
    def kelvin(self):
        """Getter only — no setter, so kelvin is read-only."""
        return self._celsius + 273.15


temp = Temperature(25)
print(f"{temp.celsius}°C = {temp.fahrenheit}°F = {temp.kelvin}K")
# 25°C = 77.0°F = 298.15K

temp.fahrenheit = 32    # Triggers the setter → converts and validates
print(f"{temp.celsius}°C")  # 0.0°C

# temp.kelvin = 300     # ❌ AttributeError — read-only, no setter
# temp.celsius = -300   # ❌ ValueError — blocked by validation
```

### Why @property Is Useful

1. **Validation at the gate.** The absolute-zero check runs no matter how you set the temperature — directly via `celsius` or indirectly via `fahrenheit`.
2. **Clean outside, smart inside.** Users write `temp.celsius = 25` — simple. Underneath, your validation runs automatically.
3. **No stored duplicates.** `fahrenheit` and `kelvin` aren't separate variables — they're calculated from `_celsius`. They can never get out of sync.

---

## Practice Exercise

**Scenario:** You're building a simple game character system. Characters can be different types (Warrior, Mage, Archer), each with unique abilities. They can equip items that modify their stats.

**Your task:**

1. Create `game_characters.py`

2. Build these classes:
   - `Item` — has `name`, `slot` ("weapon", "armour", "accessory"), and `stats` (a dict like `{"attack": 5, "defence": 3}`)
   - `Character` (abstract base) — has `name`, `level`, base `stats`, inventory, and abstract method `special_ability()`
   - `Warrior(Character)` — special ability: "Power Strike" (2× attack for one hit)
   - `Mage(Character)` — special ability: "Fireball" (ignores defence)
   - `Archer(Character)` — special ability: "Multi Shot" (hits 3 times at 0.5× attack each)

3. Characters should:
   - `equip(item)` — equip an item in the right slot (replacing existing)
   - `unequip(slot)` — remove item from a slot
   - `effective_stats()` — return base stats + equipment bonuses
   - `__str__` — show name, class, level, and effective stats

4. Use properties, magic methods, and inheritance properly

**Try it yourself first!** Solution below.

---

## Solution

```python
from abc import ABC, abstractmethod


# ═══════════════════════════════════════════════════════════════════
#  ITEM CLASS
#  Items have a name, which slot they go in, and a dict of stats.
#  The stats dict is REQUIRED as a parameter — every item is different
#  (a sword might boost attack by 8, a shield boosts defence by 6).
# ═══════════════════════════════════════════════════════════════════

class Item:
    """Something a character can equip."""

    # Class-level constant — shared by all Items.
    # A set {} so "slot in VALID_SLOTS" is a fast O(1) lookup.
    VALID_SLOTS = {"weapon", "armour", "accessory"}

    def __init__(self, name, slot, stats):
        # ── Guard 1: reject invalid slot names ──
        if slot not in self.VALID_SLOTS:
            raise ValueError(f"Invalid slot: {slot}")

        # ── Guard 2: enforce that stats IS a dict ──
        # Without this, someone could pass a string or a number —
        # Python won't stop them, and the bug only surfaces later
        # when something tries stats["attack"] and gets TypeError.
        # isinstance() checks the actual type at runtime.
        if not isinstance(stats, dict):
            raise TypeError(f"stats must be a dict, got {type(stats).__name__}")

        self.name = name   # e.g. "Dragon Slayer"
        self.slot = slot   # e.g. "weapon"
        self.stats = stats # e.g. {"attack": 8}  ← now guaranteed to be a dict

    def __str__(self):
        """Magic method — called by print() and str().

        Without this, print(sword) would show something ugly like:
            <Item object at 0x7f8a...>
        With it, we get a clean readout:
            Dragon Slayer [weapon] +8 attack

        How it works, step by step with an example:
          sword = Item("Dragon Slayer", "weapon", {"attack": 8, "speed": 2})

          Step 1 — self.stats.items() yields the pairs:
            [("attack", 8), ("speed", 2)]

          Step 2 — the generator builds a string for each pair:
            "+8 attack"   (v=8,  k="attack")
            "+2 speed"    (v=2,  k="speed")

          Step 3 — ", ".join(...) glues them into one string:
            "+8 attack, +2 speed"

          Step 4 — f-string wraps it all together:
            "Dragon Slayer [weapon] +8 attack, +2 speed"

        'bonuses' is just a local variable name — it's created here,
        built entirely from self.stats, and disappears after the return.
        It's not a parameter and not in the exercise description.
        """
        bonuses = ", ".join(f"+{v} {k}" for k, v in self.stats.items())
        return f"{self.name} [{self.slot}] {bonuses}"


# ═══════════════════════════════════════════════════════════════════
#  CHARACTER (Abstract Base Class)
#
#  Unlike Items (where every item has different stats passed in),
#  every Warrior starts with the SAME base stats. So instead of
#  making you pass {"attack": 12, "defence": 10, ...} every time,
#  the subclass overrides _init_stats() to return its defaults.
#
#  This is the key difference:
#    Item.stats    ← comes from a parameter (varies per item)
#    Character.stats ← comes from _init_stats() (fixed per class)
# ═══════════════════════════════════════════════════════════════════

class Character(ABC):
    """Abstract base for all characters."""

    def __init__(self, name, level=1):
        self.name = name
        self.level = level
        # inventory maps slot → Item, e.g. {"weapon": sword, "armour": shield}
        self.inventory = {}
        # Base stats come from the subclass — Warrior/Mage/Archer each
        # override _init_stats() with their own numbers.
        self.stats = self._init_stats()

    def _init_stats(self):
        """Return starting stats for this character class.

        Override in subclasses. The base version exists as a fallback
        and also so the method reference in __init__ never crashes.
        """
        return {"attack": 5, "defence": 5, "speed": 5, "health": 100}

    # ── ABSTRACT PROPERTY: character_class ──────────────────────
    # @property     → accessed without ():  character.character_class
    # @abstractmethod → every subclass MUST provide this (Python won't
    #                    let you create a plain Character() instance)
    # The property is just a name like "Warrior", "Mage", "Archer".
    # Subclasses set it as a class attribute (see Warrior below).

    @property
    @abstractmethod
    def character_class(self):
        pass  # placeholder — subclasses provide the actual string

    # ── ABSTRACT METHOD: special_ability ─────────────────────────
    # Each subclass defines its own unique attack.

    @abstractmethod
    def special_ability(self):
        """Describe and use the character's special move."""
        pass

    # ── EQUIP / UNEQUIP ──────────────────────────────────────────

    def equip(self, item):
        """Place an item into its slot, replacing any existing item."""
        old = self.inventory.get(item.slot)  # None if the slot is empty
        self.inventory[item.slot] = item
        action = "replaced" if old else "equipped"
        return f"{self.name} {action} {item.name} in {item.slot} slot"

    def unequip(self, slot):
        """Remove and return the item from a slot."""
        if slot in self.inventory:
            item = self.inventory.pop(slot)  # pop removes AND returns
            return f"{self.name} unequipped {item.name}"
        return f"No item in {slot} slot"

    # ── EFFECTIVE STATS ──────────────────────────────────────────

    def effective_stats(self):
        """Combine base stats with all equipped item bonuses.

        This is where Character.stats and Item.stats FINALLY interact:
          - Start with the character's base stats (e.g. attack: 12)
          - Loop over every equipped item's stats dict
          - Add each bonus (e.g. sword gives +8 attack → total: 20)

        The copy is important — we don't want to mutate self.stats.
        """
        stats = dict(self.stats)  # shallow copy of base stats
        for item in self.inventory.values():
            # item.stats is the dict we validated in Item.__init__
            for stat, bonus in item.stats.items():
                # If the base character doesn't have this stat yet,
                # default it to 0 before adding the bonus.
                stats[stat] = stats.get(stat, 0) + bonus
        return stats

    # ── MAGIC METHOD: __str__ ────────────────────────────────────
    # Called when you do print(character) or str(character).

    def __str__(self):
        stats = self.effective_stats()
        # Join stats into a readable line: "ATTACK: 20 | DEFENCE: 15 | ..."
        stats_str = " | ".join(f"{k.upper()}: {v}" for k, v in stats.items())
        # List equipped items, or "none" if inventory is empty
        equipment = ", ".join(item.name for item in self.inventory.values()) or "none"
        return (
            f"{self.name} — Lv.{self.level} {self.character_class}\n"
            f"  Stats: {stats_str}\n"
            f"  Equipment: {equipment}"
        )


# ═══════════════════════════════════════════════════════════════════
#  WARRIOR — high attack, high defence, slow, lots of health
# ═══════════════════════════════════════════════════════════════════

class Warrior(Character):
    # This satisfies the @property @abstractmethod from Character.
    # It's a class attribute, but thanks to @property, it acts like
    # a read-only instance attribute — warrior.character_class → "Warrior"
    character_class = "Warrior"

    def _init_stats(self):
        """Warrior base stats — tanky melee fighter."""
        return {"attack": 12, "defence": 10, "speed": 4, "health": 120}

    def special_ability(self):
        """Power Strike: doubles attack for one hit."""
        atk = self.effective_stats()["attack"]  # gets the TOTAL attack (base+items)
        return f"⚔️ POWER STRIKE! Deals {atk * 2} damage!"


# ═══════════════════════════════════════════════════════════════════
#  MAGE — highest attack, fragile, moderate speed
# ═══════════════════════════════════════════════════════════════════

class Mage(Character):
    character_class = "Mage"

    def _init_stats(self):
        """Mage base stats — glass cannon."""
        return {"attack": 15, "defence": 3, "speed": 6, "health": 80}

    def special_ability(self):
        """Fireball: full attack damage, ignores enemy defence."""
        atk = self.effective_stats()["attack"]
        return f"🔥 FIREBALL! Deals {atk} damage (ignores defence)!"


# ═══════════════════════════════════════════════════════════════════
#  ARCHER — balanced attack, fastest, moderate health
# ═══════════════════════════════════════════════════════════════════

class Archer(Character):
    character_class = "Archer"

    def _init_stats(self):
        """Archer base stats — speed-focused ranged fighter."""
        return {"attack": 10, "defence": 5, "speed": 10, "health": 90}

    def special_ability(self):
        """Multi Shot: 3 arrows at 50% attack each."""
        atk = self.effective_stats()["attack"]
        total = int(atk * 0.5 * 3)
        return f"🏹 MULTI SHOT! 3 arrows × {int(atk * 0.5)} = {total} total damage!"


# ═══════════════════════════════════════════════════════════════════
#  TEST — only runs when you execute the file directly:
#         python game_characters.py
#  Won't run if you import this file from somewhere else.
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Create characters (no stats parameter — _init_stats handles it)
    warrior = Warrior("Thorin", level=5)
    mage = Mage("Gandalf", level=5)
    archer = Archer("Legolas", level=5)

    # Create items (stats IS a parameter — every item is unique)
    sword = Item("Dragon Slayer", "weapon", {"attack": 8})
    shield = Item("Iron Shield", "armour", {"defence": 6})
    ring = Item("Ring of Speed", "accessory", {"speed": 3})
    staff = Item("Crystal Staff", "weapon", {"attack": 10, "speed": 2})
    bow = Item("Elven Bow", "weapon", {"attack": 6, "speed": 4})

    # Try to create an item with invalid stats — this WILL crash (by design!)
    # broken = Item("Oops", "weapon", "not a dict")  # raises TypeError

    # Equip items — notice how equipping another weapon REPLACES the first
    print(warrior.equip(sword))    # Thorin equipped Dragon Slayer
    print(warrior.equip(shield))   # Thorin equipped Iron Shield
    print(warrior.equip(ring))     # Thorin equipped Ring of Speed

    print(mage.equip(staff))
    print(archer.equip(bow))

    # Display character sheets — __str__ is called by print()
    print("\n--- Characters ---")
    print(warrior)
    print(f"  Ability: {warrior.special_ability()}")  # shows total attack × 2
    print()
    print(mage)
    print(f"  Ability: {mage.special_ability()}")
    print()
    print(archer)
    print(f"  Ability: {archer.special_ability()}")
```

---

## Quick Recap

- **Encapsulation** — hide internals (`_protected`, `__private`) behind getters and setters (`@property`)
- **Inheritance** — "is-a" relationship, `super()`, override methods
- **Polymorphism** — same interface, different behaviour (duck typing + ABCs)
- **Abstraction** — ABCs define contracts, subclasses implement details
- **Magic methods** — `__str__`, `__add__`, `__eq__`, `__iter__` make your objects Pythonic
- **Composition** — "has-a" is often better than "is-a"
- **@classmethod** — factory methods; **@staticmethod** — utility functions; **@property** — clean getters and setters (write `obj.attr` instead of `obj.get_attr()`)

---

## What's Next?

Now that you can design classes properly, let's look at the simplest data structure: the stack. Continue to **[Lesson 2: Stacks](02-stacks.md)** 📚

---

**Your turn:** Build the character system! Then add an `Inventory` class that limits how many items a character can carry, with `add_item()` and `remove_item()` methods. 🏛️💛
