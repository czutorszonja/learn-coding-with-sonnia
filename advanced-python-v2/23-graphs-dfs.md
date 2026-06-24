# Lesson 23: Graphs & DFS 🔍

**← Back to [Lesson 22: Graphs & BFS](22-graphs-bfs.md)**

---

## The Problem: Sometimes "Shortest" Isn't What You Need

BFS is brilliant for finding the shortest path. But not every problem wants the shortest route:

- **Maze solving** — you want to explore every corridor until you find the exit. Taking the shortest known route might mean missing a hidden passage.
- **Dependency resolution** — installing a Python package might require another package, which requires another… you need to follow the chain all the way down before you know what to install.
- **Cycle detection** — is there a loop in this dependency graph? DFS can spot cycles that BFS might miss.
- **Finding ALL paths** — how many different ways can you get from A to B? BFS gives you the shortest. DFS explores everything.
- **Topological sorting** — what order should you take classes, given prerequisites? DFS naturally produces this order.
- **Puzzle solving** — Sudoku solvers, chess move trees, escape rooms. DFS goes deep into possibilities, backtracks when it hits a dead end.

BFS asks "what's the fastest way?" DFS asks "what's out there?"

---

## The Idea: Follow One Path to the End, Then Backtrack

Imagine you're exploring a cave system. Two strategies:

**BFS (the cautious explorer):** Check every tunnel at the entrance first. Then every tunnel one room deeper. Then the next level. You'll find the shortest route to the treasure, but you're constantly running back to the entrance.

**DFS (the bold explorer):** Pick a tunnel and follow it as far as it goes. When you hit a dead end, backtrack to the last junction and try the next tunnel. You might go very deep before finding anything, but you'll eventually explore the entire cave.

```
      A
     / \
    B   C
   / \   \
  D   E   F

BFS order: A → B → C → D → E → F   (level by level)
DFS order: A → B → D → E → C → F   (deep first, then backtrack)
```

DFS goes A → B → D (all the way down the left), then backtracks to B → E, then backtracks all the way to A → C → F.

---

## Two Ways to Do DFS

DFS uses a **stack** instead of a queue. There are two ways to implement it:

| Approach | How | Best when |
|----------|-----|-----------|
| **Iterative** | Use an explicit stack (a Python list) | You want to see every step, avoid recursion limits |
| **Recursive** | Use the function call stack | The code is cleaner, the problem is naturally recursive |

You already know both tools: stacks from Lesson 8, recursion from Lesson 19. DFS is where they meet.

We'll build both.

---

## Step by Step: Iterative DFS

### Step 1: DFS With an Explicit Stack

Remember BFS? It used a queue — `popleft()` takes from the front. DFS uses a stack — `pop()` takes from the back (the top). That one difference changes the entire exploration order:

```python
from collections import deque


# BFS (for comparison)
def bfs_traversal(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    order = []

    while queue:
        current = queue.popleft()   # Front — FIFO
        order.append(current)
        for neighbour in graph.neighbours(current):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
    return order


# DFS (iterative — using a stack)
def dfs_traversal(graph, start):
    visited = set()
    stack = [start]          # A plain list — no deque needed
    order = []

    while stack:
        current = stack.pop()    # Top — LIFO (the ONLY difference!)
        if current in visited:
            continue
        visited.add(current)
        order.append(current)

        for neighbour in graph.neighbours(current):
            if neighbour not in visited:
                stack.append(neighbour)
    return order
```

The ONLY difference: `popleft()` → `pop()`. Queue → Stack. That's it.

```python
# Using the same Graph class from Lesson 22
class Graph:
    def __init__(self):
        self.adj = {}

    def add_node(self, node):
        if node not in self.adj:
            self.adj[node] = []

    def add_edge(self, u, v):
        if u not in self.adj:
            self.add_node(u)
        if v not in self.adj:
            self.add_node(v)
        self.adj[u].append(v)
        self.adj[v].append(u)

    def neighbours(self, node):
        return self.adj.get(node, [])


g = Graph()
g.add_edge("A", "B")
g.add_edge("A", "C")
g.add_edge("B", "D")
g.add_edge("B", "E")
g.add_edge("C", "F")

print("BFS:", bfs_traversal(g, "A"))
print("DFS:", dfs_traversal(g, "A"))
```

We're using the same `Graph` class from Lesson 22. Graph traversal doesn't care about the graph structure — it only cares about the exploration order.

One gotcha: the `if current in visited: continue` check is needed in the iterative version because a node can be added to the stack multiple times before it's actually visited. In BFS, this rarely matters because the queue processes in order. In DFS, the stack can hold duplicates of the same node from different paths — we skip them when they surface.

---

### Step 2: DFS Pathfinding (All Paths)

BFS finds the shortest path. DFS can find **all paths** between two nodes:

```python
def dfs_all_paths(graph, start, target):
    """Return all paths from start to target."""
    all_paths = []
    stack = [(start, [start])]  # (current_node, path_so_far)

    while stack:
        current, path = stack.pop()

        if current == target:
            all_paths.append(path)
            continue

        for neighbour in graph.neighbours(current):
            if neighbour not in path:  # Avoid cycles — don't revisit nodes in the same path
                stack.append((neighbour, path + [neighbour]))

    return all_paths
```

Each item on the stack carries its own path. When we hit the target, we save that path. When we explore neighbours, we create new paths — `path + [neighbour]` makes a copy so each branch has its own trail.

```python
# Find all ways from A to F in our graph:
#   A → B → D (dead end, backtrack)
#   A → B → E (dead end, backtrack)
#   A → C → F (found!)
# But wait — we could also imagine: A → B → (some connection to C) → F

paths = dfs_all_paths(g, "A", "F")
for p in paths:
    print(" → ".join(p))
# A → C → F
```

With that graph, there's only one path from A to F. But in a more connected graph, you'd get multiple.

---

## Step by Step: Recursive DFS

### Step 3: DFS With Recursion

Here's the elegant version. Recursion uses the call stack as the DFS stack — no explicit list needed:

```python
def dfs_recursive(graph, current, visited=None, order=None):
    """Visit every node reachable from current, in DFS order."""
    if visited is None:
        visited = set()
    if order is None:
        order = []

    visited.add(current)
    order.append(current)

    for neighbour in graph.neighbours(current):
        if neighbour not in visited:
            dfs_recursive(graph, neighbour, visited, order)

    return order
```

That's it. A few lines, no manual stack management. The recursion naturally goes deep — each recursive call pushes a new frame onto the call stack, exactly like pushing onto a DFS stack.

```python
print(dfs_recursive(g, "A"))
# ['A', 'B', 'D', 'E', 'C', 'F']
```

Trace the recursion:
1. `dfs_recursive(A)` → visits A, calls `dfs_recursive(B)`
2. `dfs_recursive(B)` → visits B, calls `dfs_recursive(D)`
3. `dfs_recursive(D)` → visits D, no unvisited neighbours → returns
4. Back in B's loop → calls `dfs_recursive(E)`
5. `dfs_recursive(E)` → visits E, no unvisited neighbours → returns
6. Back in A's loop → calls `dfs_recursive(C)`
7. `dfs_recursive(C)` → visits C, calls `dfs_recursive(F)`
8. `dfs_recursive(F)` → visits F, no unvisited neighbours → returns

The call stack mirrors the exploration exactly.

---

### Step 4: Recursive All-Paths

The recursive all-paths version is especially clean:

```python
def dfs_all_paths_recursive(graph, current, target, visited=None, path=None, all_paths=None):
    """Find all paths from current to target."""
    if visited is None:
        visited = set()
    if path is None:
        path = []
    if all_paths is None:
        all_paths = []

    visited.add(current)
    path.append(current)

    if current == target:
        all_paths.append(list(path))  # Save a copy!
    else:
        for neighbour in graph.neighbours(current):
            if neighbour not in visited:
                dfs_all_paths_recursive(graph, neighbour, target, visited, path, all_paths)

    # Backtrack — remove current before returning to caller
    path.pop()
    visited.remove(current)

    return all_paths
```

The crucial detail: **backtracking**. After exploring all paths from `current`, we `path.pop()` and `visited.remove(current)` — undoing our visit so other branches can use a different route through this node.

Backtracking is the DFS superpower. BFS can't do this cleanly — it explores level by level and doesn't naturally "undo."

---

## DFS vs BFS: When to Use Which

| | BFS | DFS |
|---|---|---|
| **Finds** | Shortest path (unweighted) | Any path, all paths |
| **Uses** | Queue (FIFO) | Stack or recursion (LIFO) |
| **Memory** | Can be large (stores an entire level) | Proportional to depth (call stack) |
| **Best for** | "Closest X," web crawling, social distance | Maze/puzzle solving, cycles, dependencies |
| **Order** | Level by level | Deep first, backtrack |
| **Can get stuck?** | No (always makes progress outward) | Yes — can go infinitely deep on infinite graphs (use `visited`) |

---

## Practice: Find All Paths in a Social Network

**Your task:** Given a friendship graph, find ALL possible chains of introductions between two people.

Write a function `all_introduction_chains(graph, person_a, person_b)` that returns every unique path of friends connecting them. Each person should appear at most once per chain (no loops).

```python
def all_introduction_chains(graph, person_a, person_b):
    """Return a list of all paths from person_a to person_b."""
    # Your code here — use DFS (iterative or recursive, your choice)
    pass


# Test with a more connected network
network = Graph()
network.add_edge("Szonja", "Arthur")
network.add_edge("Szonja", "Cece")
network.add_edge("Szonja", "Frank")
network.add_edge("Arthur", "Cece")
network.add_edge("Arthur", "Diana")
network.add_edge("Cece", "Frank")
network.add_edge("Frank", "Diana")

# Find all ways from Szonja to Diana
chains = all_introduction_chains(network, "Szonja", "Diana")

print(f"Found {len(chains)} introduction chain(s):")
for i, chain in enumerate(chains, 1):
    print(f"  {i}. {' → '.join(chain)}")

# Expected output (order may vary):
# Found 3 introduction chain(s):
#   1. Szonja → Arthur → Diana
#   2. Szonja → Cece → Frank → Diana
#   3. Szonja → Frank → Diana
```

**Think about it:**
- You need to explore ALL paths — that's DFS territory
- Use a `visited` set or check that `neighbour not in current_path` to avoid cycles
- When you reach the target, save a copy of the current path and backtrack
- BFS could find some paths, but DFS is the natural tool for exhaustive exploration

Save as `introduction_chains.py` and try it!

---

## Solution

```python
# Iterative version (using explicit stack)
def all_introduction_chains(graph, person_a, person_b):
    """Return all unique paths from person_a to person_b."""
    if person_a not in graph.adj or person_b not in graph.adj:
        return []

    all_paths = []
    stack = [(person_a, [person_a])]

    while stack:
        current, path = stack.pop()

        if current == person_b:
            all_paths.append(path)
            continue

        for neighbour in graph.neighbours(current):
            if neighbour not in path:
                stack.append((neighbour, path + [neighbour]))

    return all_paths


# Recursive version (more elegant)
def all_introduction_chains_recursive(graph, person_a, person_b):
    """Return all unique paths from person_a to person_b."""
    all_paths = []

    def dfs(current, path, visited):
        if current == person_b:
            all_paths.append(list(path))
            return

        for neighbour in graph.neighbours(current):
            if neighbour not in visited:
                visited.add(neighbour)
                path.append(neighbour)
                dfs(neighbour, path, visited)
                path.pop()
                visited.remove(neighbour)

    dfs(person_a, [person_a], {person_a})
    return all_paths


# Test
class Graph:
    def __init__(self):
        self.adj = {}

    def add_node(self, node):
        if node not in self.adj:
            self.adj[node] = []

    def add_edge(self, u, v):
        if u not in self.adj:
            self.add_node(u)
        if v not in self.adj:
            self.add_node(v)
        self.adj[u].append(v)
        self.adj[v].append(u)

    def neighbours(self, node):
        return self.adj.get(node, [])


network = Graph()
network.add_edge("Szonja", "Arthur")
network.add_edge("Szonja", "Cece")
network.add_edge("Szonja", "Frank")
network.add_edge("Arthur", "Cece")
network.add_edge("Arthur", "Diana")
network.add_edge("Cece", "Frank")
network.add_edge("Frank", "Diana")

chains = all_introduction_chains(network, "Szonja", "Diana")

print(f"Found {len(chains)} introduction chain(s):")
for i, chain in enumerate(chains, 1):
    print(f"  {i}. {' → '.join(chain)}")
```

---

## Where DFS Shows Up in the Real World

- **Maze solvers** — DFS explores every corridor; backtrack at dead ends
- **Cycle detection** — if you encounter a node already in your current path, you've found a cycle
- **Topological sorting** — "what order do I install these packages?" DFS gives the dependency order
- **Connected components** — DFS from every unvisited node finds all separate "islands" in a graph
- **Solving puzzles** — Sudoku, N-Queens, crossword generation — all use DFS with backtracking
- **Finding bridges/articulation points** — which connection, if removed, would split the network? DFS can tell you.
- **Garbage collection** — programming language runtimes use DFS to find which objects are still reachable

---

## What You Just Learned

- **DFS** = depth-first search — follows one path to the end, then backtracks
- **Iterative DFS** uses a `stack` (a plain Python list with `pop()`)
- **Recursive DFS** uses the function call stack — cleaner code, same behaviour
- **The only BFS → DFS change**: `queue.popleft()` becomes `stack.pop()`
- **DFS finds ALL paths** — BFS finds the shortest. Different tools for different jobs.
- **Backtracking** = `path.pop()` + `visited.remove()` — undo your visit so other branches can explore differently
- **Use `visited`** to avoid infinite loops — graphs can have cycles, unlike trees

---

## What's Next?

You now have the complete graph toolkit: adjacency lists, BFS, and DFS. These three ideas power everything from Google Maps to LinkedIn to video game AI.

From here, the path branches. You could explore:
- **Dijkstra's algorithm** — BFS on weighted graphs (roads with distances)
- **A\* search** — "smart BFS" with a heuristic (how GPS really works)
- **Dynamic programming** — solving problems by breaking them into overlapping subproblems
- Or jump back to any lesson that needs a second look

The graph is yours to explore. 🕸️

---

**Your turn:** Build the introduction chains finder! Then try writing `has_cycle(graph)` — a function that returns `True` if the graph contains at least one cycle. (Hint: in DFS, if you ever see a neighbour that's already in your current path — but ISN'T the node you just came from — you've found a cycle.) 🔍💛
