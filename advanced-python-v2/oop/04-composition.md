# OOP Lesson 4: Composition — "Has-a" vs "Is-a" 🧩

**← Back to [Lesson 3: Magic Methods](03-magic-methods.md)**

---

## Two Ways to Reuse Code

You've learned **inheritance**: a Dog _is an_ Animal. It works when there's a clear parent-child relationship.

But what about this?

```python
class Car:
    # A car has an engine, has wheels, has seats...
```

A car is NOT a specialised engine. A car HAS an engine. This is **composition**: building complex objects by combining simpler ones.

---

## Inheritance vs Composition, Side By Side

**Inheritance** ("is-a"):

```python
class Vehicle:
    def __init__(self):
        self.speed = 0

    def accelerate(self, amount):
        self.speed += amount


class SportsCar(Vehicle):    # SportsCar IS a Vehicle
    def accelerate(self, amount):
        self.speed += amount * 2  # Faster acceleration!


car = SportsCar()
car.accelerate(10)
print(car.speed)  # 20
```

**Composition** ("has-a"):

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


class Car:                   # Car HAS an Engine (and Wheels, and seats...)
    def __init__(self, make, horsepower):
        self.make = make
        self.engine = Engine(horsepower)  # Composition!
        self.speed = 0

    def start(self):
        return self.engine.start()

    def accelerate(self, amount):
        self.speed += amount


car = Car("Mini", 134)
print(car.start())            # Vroom! 🔥
print(car.engine.horsepower)  # 134
```

---

## Why Composition Is Often Better

**Problem with inheritance:** It creates rigid hierarchies. What if you need a `FlyingCar`? Does it inherit from `Car` or `Aircraft`? What about an `AmphibiousVehicle`?

**Composition solves this:** A flying car IS a car that HAS wings. An amphibious vehicle IS a vehicle that HAS a propeller.

```python
class Car:
    def __init__(self):
        self.engine = Engine(150)
        self.wheels = Wheels(4)
        self.speed = 0

    def drive(self):
        self.engine.start()
        self.speed = 50
        return "Driving on the road 🚗"


class Boat:
    def __init__(self):
        self.engine = Engine(200)
        self.propeller = Propeller()
        self.speed = 0

    def sail(self):
        self.engine.start()
        self.speed = 20
        return "Sailing on water ⛵"


# Now a SeaPlane — no inheritance madness needed:
class SeaPlane:
    def __init__(self):
        self.engine = Engine(300)     # Has an engine
        self.wings = Wings()          # Has wings
        self.floats = Floats()        # Has floats

    def fly(self):
        return "Flying ✈️"

    def land_on_water(self):
        return "Landing on water 🌊"
```

No `class SeaPlane(Car, Boat, Aircraft)` nonsense. Just compose the pieces you need.

---

## A Practical Example: A Character System

**Inheritance approach** (rigid):

```python
class Character:
    def __init__(self, name):
        self.name = name
        self.health = 100

class Warrior(Character): ...
class Mage(Character): ...
class Archer(Character): ...
```

What if a Warrior picks up a spell book? Now they can cast spells. Inheritance can't handle that — a Warrior is not a Mage.

**Composition approach** (flexible):

```python
class Character:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.abilities = []   # Characters HAVE abilities — composition!

    def add_ability(self, ability):
        self.abilities.append(ability)

    def use_ability(self, index):
        if index < len(self.abilities):
            return self.abilities[index].activate(self)
        return "No such ability"


class Slash:
    def activate(self, user):
        return f"{user.name} slashes! ⚔️"


class Fireball:
    def activate(self, user):
        return f"{user.name} casts Fireball! 🔥"


class Heal:
    def activate(self, user):
        user.health = min(100, user.health + 20)
        return f"{user.name} heals! Health: {user.health} 💚"


# Any character can have any combination of abilities:
warrior = Character("Thorin")
warrior.add_ability(Slash())

mage = Character("Gandalf")
mage.add_ability(Fireball())
mage.add_ability(Heal())

# A warrior-mage hybrid? Just add both:
battle_mage = Character("Elara")
battle_mage.add_ability(Slash())
battle_mage.add_ability(Fireball())

print(warrior.use_ability(0))     # Thorin slashes! ⚔️
print(mage.use_ability(0))        # Gandalf casts Fireball! 🔥
print(mage.use_ability(1))        # Gandalf heals! Health: 100 💚
print(battle_mage.use_ability(0)) # Elara slashes! ⚔️
print(battle_mage.use_ability(1)) # Elara casts Fireball! 🔥
```

No class hierarchy can express "Warrior who learned magic" as cleanly as composition.

---

## The Rule of Thumb

| Use Inheritance when… | Use Composition when… |
|----------------------|---------------------|
| There's a clear "is-a" relationship | It's a "has-a" relationship |
| Behaviour is mostly shared | Behaviour varies a lot between objects |
| The hierarchy won't change much | You need flexibility |
| Example: `Dog → Animal` | Example: `Car → Engine, Wheels, Seats` |

**When in doubt, prefer composition.** It's more flexible and causes fewer headaches down the line.

---

## Practice: A Computer Builder

**Your task:** Build a `Computer` class using composition. A computer HAS components.

1. Create component classes:
   - `CPU` — has `model` and `cores`
   - `RAM` — has `size_gb`
   - `Storage` — has `type` ("SSD" or "HDD") and `capacity_gb`

2. Create a `Computer` class that:
   - Takes `cpu`, `ram`, and `storage` in `__init__`
   - `specs()` — prints a summary of all components
   - `total_storage()` — returns the capacity in GB
   - `is_powerful()` — returns `True` if CPU has ≥ 4 cores AND RAM ≥ 16GB

**Test it:**

```python
my_pc = Computer(
    CPU("Intel i7", 8),
    RAM(32),
    Storage("SSD", 1000),
)

print(my_pc.specs())
my_pc.is_powerful()  # True (8 cores, 32GB RAM)
```

Create `computer.py` and try it!

---

## Solution

```python
class CPU:
    def __init__(self, model, cores):
        self.model = model
        self.cores = cores

    def __str__(self):
        return f"{self.model} ({self.cores} cores)"


class RAM:
    def __init__(self, size_gb):
        self.size_gb = size_gb

    def __str__(self):
        return f"{self.size_gb}GB RAM"


class Storage:
    def __init__(self, type_, capacity_gb):
        self.type = type_
        self.capacity_gb = capacity_gb

    def __str__(self):
        return f"{self.capacity_gb}GB {self.type}"


class Computer:
    def __init__(self, cpu, ram, storage):
        self.cpu = cpu          # Has-a CPU
        self.ram = ram          # Has-a RAM
        self.storage = storage  # Has-a Storage

    def specs(self):
        return f"Computer: {self.cpu} | {self.ram} | {self.storage}"

    def total_storage(self):
        return self.storage.capacity_gb

    def is_powerful(self):
        return self.cpu.cores >= 4 and self.ram.size_gb >= 16


# Test
my_pc = Computer(
    CPU("Intel i7", 8),
    RAM(32),
    Storage("SSD", 1000),
)

print(my_pc.specs())
print(f"Storage: {my_pc.total_storage()}GB")
print(f"Is powerful: {my_pc.is_powerful()}")

# Weak computer
cheap_pc = Computer(CPU("Celeron", 2), RAM(4), Storage("HDD", 500))
print(f"Is powerful: {cheap_pc.is_powerful()}")
```

---

## What You Just Learned

- **Inheritance = "is-a"** — rigid hierarchy, good for shared behaviour
- **Composition = "has-a"** — flexible, build from pieces
- **Prefer composition** — it's easier to change later
- **Combine both** — use inheritance for the big picture, composition for the details

---

This wraps up the OOP section. You now know:
1. How to create classes (`__init__`, `self`)
2. How to protect data (encapsulation, `@property`)
3. How to share behaviour (inheritance, `super()`)
4. How to use the same interface for different objects (polymorphism)
5. How to make objects feel Pythonic (magic methods)
6. How to build from pieces (composition)

Next up: **data structures** — the building blocks that make your programs fast and elegant.

Continue to **[Data Structures Lesson 1: Stacks](../data-structures/01-stacks.md)** 📚

---

**Your turn:** Build the computer! Then add a `GPU` component and add it to the Computer class. 🧩💛
