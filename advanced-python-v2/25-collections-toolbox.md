# Lesson 25: The Collections Toolbox 🧰

**← Back to [Lesson 24: Graphs & DFS](24-graphs-dfs.md)**

---

## The Problem: Lists and Dicts Aren't Always Enough

You've met `deque`, `defaultdict`, and `Counter` already. But Python's `collections` module has more tools — each one a little data-structure superpower for a specific job.

The problem: most people write extra code when one import would do the trick. Ten lines of boilerplate that collapse into one line of `namedtuple` or `ChainMap`.

---

## Tool #1: namedtuple — Tuples With Names

Plain tuples work, but they're frustrating to read:

```python
student = ("Alice", 22, "Physics")
print(student[1])  # 22 — wait, was that age or grade?
```

A **namedtuple** gives you a lightweight, immutable container where fields have names:

```python
from collections import namedtuple

Student = namedtuple("Student", ["name", "age", "major"])
alice = Student("Alice", 22, "Physics")

print(alice.name)    # "Alice" — readable!
print(alice.age)     # 22 — no more [1]
print(alice)         # Student(name='Alice', age=22, major='Physics')
```

It's still a tuple underneath — so it's immutable and memory-efficient:

```python
alice.age = 23  # ❌ AttributeError: can't set attribute
```

But you can create a modified copy with `._replace()`:

```python
alice = alice._replace(age=23)  # ✅ New namedtuple, age updated
```

**When to use namedtuple instead of a class:**
- You just need a bucket of named values
- You don't need methods
- You want it to be hashable (for dict keys or sets)

```python
# Without namedtuple — clunky:
def get_point():
    return (3, 5)  # What's 3? What's 5?

# With namedtuple — clear:
Point = namedtuple("Point", ["x", "y"])
def get_point():
    return Point(3, 5)  # x=3, y=5 — obvious!
```

---

## Tool #2: OrderedDict — A Dict That Remembers

Since Python 3.7, regular dicts remember insertion order. So why does `OrderedDict` still exist?

Two reasons: **reordering** and **equality that cares about order**.

```python
from collections import OrderedDict

scores = OrderedDict()
scores["Zara"] = 92
scores["Bob"] = 88
scores["Alice"] = 95

# Move something to the end
scores.move_to_end("Bob")  # Bob is now last

# Move something to the front
scores.move_to_end("Zara", last=False)  # Zara goes first

print(scores)  # OrderedDict({'Zara': 92, 'Alice': 95, 'Bob': 88})
```

And the equality difference:

```python
a = {"x": 1, "y": 2}
b = {"y": 2, "x": 1}
print(a == b)  # True — regular dicts don't care about order

a = OrderedDict([("x", 1), ("y", 2)])
b = OrderedDict([("y", 2), ("x", 1)])
print(a == b)  # False — OrderedDicts DO care
```

`popitem(last=False)` gives you FIFO removal (like a queue built on a dict):

```python
cache = OrderedDict()
cache["page1"] = "..."
cache["page2"] = "..."
cache["page3"] = "..."

# Evict the oldest entry (first-in, first-out)
oldest = cache.popitem(last=False)  # ("page1", "...")
```

This is actually how `functools.lru_cache` works under the hood!

---

## Tool #3: ChainMap — Search Multiple Dicts at Once

Imagine you have defaults in one dict and overrides in another. Without ChainMap, you'd merge them (losing the source). With ChainMap, you search through layers:

```python
from collections import ChainMap

defaults = {"theme": "light", "font_size": 14, "language": "en"}
user_prefs = {"theme": "dark", "font_size": 18}
session = {"font_size": 20}

config = ChainMap(session, user_prefs, defaults)

print(config["theme"])      # "dark" — from user_prefs
print(config["font_size"])  # 20 — from session (first match wins)
print(config["language"])   # "en" — falls through to defaults
```

Each dict stays separate — you can still modify them individually:

```python
user_prefs["theme"] = "solarized"
print(config["theme"])  # "solarized" — ChainMap sees the update live
```

To see *where* a value came from:

```python
print(config.maps)  # [{'font_size': 20}, {'theme': 'dark', ...}, {'theme': 'light', ...}]
```

**Real-world use:** Config systems, command-line args overriding environment variables overriding defaults. Flask and Django both use this pattern under the hood.

---

## Tool #4: UserDict & UserList — When You Need to Subclass

You might think you can subclass `dict` directly:

```python
class CountDict(dict):
    def __setitem__(self, key, value):
        print(f"Setting {key} = {value}")
        super().__setitem__(key, value)

cd = CountDict()
cd["x"] = 1   # ✅ prints "Setting x = 1"
cd.update({"y": 2})  # ❌ DOESN'T print — update() bypasses __setitem__!
```

Dict's C implementation has methods like `update()` that skip Python overrides. **UserDict** fixes this:

```python
from collections import UserDict

class CountDict(UserDict):
    def __setitem__(self, key, value):
        print(f"Setting {key} = {value}")
        super().__setitem__(key, value)

cd = CountDict()
cd["x"] = 1       # ✅ "Setting x = 1"
cd.update({"y": 2})  # ✅ "Setting y = 2" — works now!
```

Same story with `UserList`:

```python
from collections import UserList

class NoisyList(UserList):
    def append(self, item):
        print(f"Adding {item}")
        super().append(item)

nl = NoisyList([1, 2])
nl.append(3)        # ✅ "Adding 3"
nl.extend([4, 5])   # ✅ Also triggers append for each!
```

**Rule of thumb:** Subclass `UserDict`/`UserList`/`UserString` instead of `dict`/`list`/`str` when you're overriding dunder methods.

---

## The Full Toolbox at a Glance

| Tool | What It Does | Use When... |
|------|-------------|------------|
| `namedtuple` | Tuple with named fields | You want a tiny, immutable data container |
| `deque` | Double-ended queue | You need fast appends/pops at both ends (Lesson 17) |
| `Counter` | Counts things | "How many of each?" (Lesson 22) |
| `defaultdict` | Dict with a default factory | You hate `if key not in d` checks (Lesson 22) |
| `OrderedDict` | Dict with reordering powers | You need `move_to_end()` or order-sensitive equality |
| `ChainMap` | Layered dict lookup | Configs, overrides, fallback chains |
| `UserDict` | Subclassable dict | You're overriding `__setitem__`, `__getitem__`, etc. |
| `UserList` | Subclassable list | Same, but for lists |

---

## Your Turn

You're building a simple **game score tracker**. Here's the spec:

1. Each player has a **name**, **score**, and **level** — use `namedtuple`
2. Store players in insertion order and support a "bump to front" for the current leader — use `OrderedDict`
3. Every game has **global config** (difficulty="normal", max_players=4) that individual game sessions can override — use `ChainMap`
4. The score tracker itself is a dict-like object, but you want to **log every score change** — use `UserDict`

Build a `GameTracker` class that:

```python
tracker = GameTracker(difficulty="easy", max_players=3)

# Add players
tracker.add_player("Alice", 0, 1)
tracker.add_player("Bob", 0, 1)
tracker.add_player("Charlie", 0, 1)

# Update scores
tracker["Alice"] = 150
tracker["Bob"] = 200
tracker["Charlie"] = 175

# Get current leader (highest score, bumped to front of OrderedDict)
leader = tracker.leader()
print(leader)  # Player(name='Bob', score=200, level=1)

# Check config
print(tracker.config["difficulty"])   # "easy" (from session)
print(tracker.config["max_players"])  # 3 (from session)
```

**Hints:**
- `namedtuple` for the Player type
- `OrderedDict` keyed by player name, value is the Player namedtuple
- `ChainMap` with session overrides on top of global defaults
- `UserDict` for the tracker itself — override `__setitem__` to log

---

## Solution

<details>
<summary>Click to reveal</summary>

```python
from collections import namedtuple, OrderedDict, ChainMap, UserDict

# 1. Player type
Player = namedtuple("Player", ["name", "score", "level"])

# Global defaults — outside the class so all trackers share them
GLOBAL_CONFIG = {"difficulty": "normal", "max_players": 4}


class GameTracker(UserDict):
    def __init__(self, **session_overrides):
        # 3. ChainMap: session on top, globals as fallback
        self.config = ChainMap(session_overrides, GLOBAL_CONFIG)
        # 2. OrderedDict: players in insertion order
        self._players = OrderedDict()
        # UserDict stores its data in self.data
        super().__init__()

    def add_player(self, name, score=0, level=1):
        player = Player(name, score, level)
        self._players[name] = player
        self.data[name] = score

    # 4. Log every score change via __setitem__
    def __setitem__(self, name, score):
        if name not in self._players:
            raise KeyError(f"No player named '{name}'")
        old_score = self._players[name].score
        print(f"📊 {name}: {old_score} → {score}")
        # Update the namedtuple (immutable, so _replace)
        old = self._players[name]
        self._players[name] = old._replace(score=score)
        super().__setitem__(name, score)

    def leader(self):
        if not self._players:
            return None
        # Find highest score
        best_name = max(self._players, key=lambda n: self._players[n].score)
        # Bump to front
        self._players.move_to_end(best_name, last=False)
        return self._players[best_name]


# --- Test it ---
tracker = GameTracker(difficulty="easy", max_players=3)

tracker.add_player("Alice", 0, 1)
tracker.add_player("Bob", 0, 1)
tracker.add_player("Charlie", 0, 1)

tracker["Alice"] = 150
tracker["Bob"] = 200
tracker["Charlie"] = 175

leader = tracker.leader()
print(leader)  # Player(name='Bob', score=200, level=1)

print(tracker.config["difficulty"])   # easy
print(tracker.config["max_players"])  # 3
print(tracker.config["difficulty"] == "easy")  # True
```

</details>

---

## Why This Matters

You could write all of this with plain lists and dicts. But:

- `namedtuple` gives you **self-documenting** code — `player.score` beats `player[1]`
- `OrderedDict.move_to_end()` is one method call instead of delete-and-reinsert
- `ChainMap` keeps your defaults and overrides **separate** — no accidental mutation
- `UserDict` makes your subclass **actually work** when `update()`, `|=`, and friends are called

The collections module isn't flashy. It's the humble toolkit that quietly removes boilerplate. Import it. Use it. Write less code.

---

**Next lesson: You've finished the curriculum! 🎉** Time to build something real. Pick a project — anything you're curious about — and we'll build it together.
