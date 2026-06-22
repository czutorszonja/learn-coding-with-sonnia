# Lesson 4: Sharing Behaviour with Inheritance 🧬

**← Back to [Lesson 3: Cleaner Access with @property](03-property-basics.md)**

---

## The Problem: Copy-Paste Classes

You're building a game. You need a Warrior and a Mage. You start writing:

```python
class Warrior:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.health = 100

    def take_damage(self, amount):
        self.health -= amount
        return f"{self.name} took {amount} damage! Health: {self.health}"

    def rest(self):
        self.health = 100
        return f"{self.name} rests and recovers."


class Mage:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.health = 80     # Mages are squishier

    def take_damage(self, amount):
        self.health -= amount
        return f"{self.name} took {amount} damage! Health: {self.health}"

    def rest(self):
        self.health = 80
        return f"{self.name} rests and recovers."
```

Look at all that duplication. `__init__`, `take_damage`, `rest` — almost identical in both classes. And now you need to add an Archer, and a Rogue, and a Cleric... each one copying the same code with tiny variations.

This is exactly the problem inheritance solves.

---

## The Idea: A Parent Class

What if the shared stuff lived in ONE place, and the unique stuff lived in the individual classes?

```python
class Character:           # ← The PARENT — holds everything shared
    def __init__(self, name, level, health):
        self.name = name
        self.level = level
        self.health = health

    def take_damage(self, amount):
        self.health -= amount
        return f"{self.name} took {amount} damage! Health: {self.health}"

    def rest(self):
        self.health = self.max_health  # We'll need this...
        return f"{self.name} rests and recovers."


class Warrior(Character):  # ← The CHILD — inherits from Character
    def __init__(self, name, level):
        super().__init__(name, level, 120)  # Warriors have 120 health

    def battle_cry(self):
        return f"{self.name} shouts: FOR GLORY! ⚔️"


class Mage(Character):     # ← Another CHILD
    def __init__(self, name, level):
        super().__init__(name, level, 80)   # Mages have 80 health

    def cast_spell(self):
        return f"{self.name} casts Fireball! 🔥"
```

Now look what we can do:

```python
warrior = Warrior("Thorin", 5)
mage = Mage("Gandalf", 7)

# Both have take_damage and rest — they INHERITED them from Character
print(warrior.take_damage(30))  # Thorin took 30 damage! Health: 90
print(mage.take_damage(30))     # Gandalf took 30 damage! Health: 50

# Each has their own unique abilities too
print(warrior.battle_cry())     # Thorin shouts: FOR GLORY! ⚔️
print(mage.cast_spell())        # Gandalf casts Fireball! 🔥
```

The shared code lives in `Character` once. The unique stuff lives in each child class. No more copy-paste.

---

## The Key Line: `super().__init__()`

```python
class Warrior(Character):
    def __init__(self, name, level):
        super().__init__(name, level, 120)
```

`super()` means "my parent class." So `super().__init__(name, level, 120)` means "call Character's `__init__` with name, level, and 120 as the health."

In plain English: "Set up everything Character needs, and give me 120 health."

Without `super().__init__()`, the parent class never gets set up — `self.name` wouldn't exist, `self.health` would be missing, everything would break.

**Rule:** If your parent has an `__init__`, always call `super().__init__()` in the child.

---

## Overriding: Customising Inherited Behaviour

Sometimes you want MOST of what the parent does, but with a twist:

```python
class Warrior(Character):
    def __init__(self, name, level):
        super().__init__(name, level, 120)

    def rest(self):
        """Warriors heal more because they're tough."""
        self.health = self.max_health + 20  # Extra recovery!
        return f"{self.name} rests deeply. Health: {self.health}"

    def battle_cry(self):
        return f"{self.name} shouts: FOR GLORY! ⚔️"
```

The child's `rest()` REPLACES the parent's `rest()`. This is called **overriding**.

---

## The "is-a" Test

How do you know if inheritance makes sense? Use the "is-a" test:

- A Warrior **is a** Character ✅ → inheritance works
- A Car **is a** Vehicle ✅ → inheritance works  
- A Cat **is an** Animal ✅ → inheritance works
- A BankAccount **is a** TransactionLog ❌ → doesn't make sense! Use composition instead

If you can't say "[child] is a [parent]" naturally, inheritance is probably the wrong tool.

---

## Practice: An Animal Shelter

**Your task:** Build a simple system for an animal shelter.

1. Create an `Animal` parent class with:
   - `name` (string)
   - `species` (string)  
   - `age` (integer)
   - `make_sound()` — returns `"*generic animal noise*"`
   - `info()` — returns something like `"Luna is a 3-year-old Cat"`

2. Create two child classes:
   - `Dog(Animal)` — `make_sound()` returns `"Woof! 🐕"`
   - `Cat(Animal)` — `make_sound()` returns `"Meow! 🐱"`

3. Create a `Shelter` class that:
   - Stores animals in a list
   - `add_animal(animal)` — adds any Animal to the shelter
   - `list_all()` — prints info for every animal
   - `make_everyone_speak()` — prints each animal's name and sound

**Test it:**

```python
shelter = Shelter()
shelter.add_animal(Dog("Rex", 2))
shelter.add_animal(Cat("Luna", 3))
shelter.add_animal(Dog("Buddy", 1))

shelter.list_all()
# Rex is a 2-year-old Dog
# Luna is a 3-year-old Cat
# Buddy is a 1-year-old Dog

shelter.make_everyone_speak()
# Rex says: Woof! 🐕
# Luna says: Meow! 🐱
# Buddy says: Woof! 🐕
```

Create `shelter.py` and try it!

---

## Solution

```python
class Animal:
    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age

    def make_sound(self):
        return "*generic animal noise*"

    def info(self):
        return f"{self.name} is a {self.age}-year-old {self.species}"


class Dog(Animal):
    def __init__(self, name, age):
        super().__init__(name, "Dog", age)

    def make_sound(self):
        return "Woof! 🐕"


class Cat(Animal):
    def __init__(self, name, age):
        super().__init__(name, "Cat", age)

    def make_sound(self):
        return "Meow! 🐱"


class Shelter:
    def __init__(self):
        self.animals = []

    def add_animal(self, animal):
        self.animals.append(animal)

    def list_all(self):
        for animal in self.animals:
            print(animal.info())

    def make_everyone_speak(self):
        for animal in self.animals:
            print(f"{animal.name} says: {animal.make_sound()}")


# Test
shelter = Shelter()
shelter.add_animal(Dog("Rex", 2))
shelter.add_animal(Cat("Luna", 3))
shelter.add_animal(Dog("Buddy", 1))

shelter.list_all()
print()
shelter.make_everyone_speak()
```

---

## What You Just Learned

- **Inheritance** lets child classes reuse code from a parent class
- **`super().__init__()`** calls the parent's constructor — always do this!
- **Overriding** — a child can replace a parent's method with its own version
- **The "is-a" test** — use inheritance only when it makes sense in plain English
- **One parent, many children** — but each child adds its own personality

---

## What's Next?

Your `Shelter` can hold any Animal and call `make_sound()` on all of them — even though Dogs and Cats sound different. Python just figures it out. This is **polymorphism**, and it's next.

Continue to **[Lesson 5: Same Interface, Different Behaviour](05-polymorphism.md)** 🎭

---

**Your turn:** Build the shelter! Then add a `Bird` class where `make_sound()` returns "Chirp! 🐦" and add one to the shelter. Notice you didn't have to change ANY other code — the shelter handles it automatically. That's the power of inheritance. 🧬💛
