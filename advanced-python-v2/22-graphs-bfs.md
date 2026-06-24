# Lesson 22: Graphs & BFS 🕸️

**← Back to [Lesson 21: Time & Space Complexity](21-complexity.md)**

---

## The Problem: Trees Aren't Enough

Trees are brilliant for branching data. But what about connections that go in ANY direction?

- **Social networks** — Alice is friends with Bob, Bob with Charlie, but Charlie might also know Alice directly. That's a loop — trees can't have loops.
- **Road maps** — cities connect to each other. There's no "root city" and no "parent-child" relationship. London connects to Paris, Paris to Brussels, Brussels back to London.
- **The web** — pages link to each other. There's no single starting point and no hierarchy.
- **Recommendation systems** — "people who bought this also bought that" forms a tangled web of products.
- **Game maps** — rooms connect to rooms, sometimes with multiple paths between the same two places.

These aren't trees. They're **graphs**.

---

## The Idea: Nodes + Edges, No Rules

A **graph** is the simplest possible network:

- **Nodes** (also called **vertices**) — the things (people, cities, web pages)
- **Edges** — the connections between them

```
    Alice ──── Bob
      │          │
      │          │
    Charlie ── Diana
      │
      │
    Edward
```

No root. No parent-child. Just connections. Alice connects to Bob and Charlie. Bob connects to Alice and Diana. Charlie connects to Alice, Diana, and Edward. That's a graph.

**Graph vocabulary:**

| Term | Meaning |
|------|---------|
| Node / Vertex | A thing in the graph (Alice, Bob, etc.) |
| Edge | A connection between two nodes |
| Neighbour | A node directly connected to another |
| Path | A sequence of nodes connected by edges |
| Cycle | A path that starts and ends at the same node |
| Directed graph | Edges have a direction (Twitter: Alice follows Bob, Bob may not follow back) |
| Undirected graph | Edges go both ways (Facebook friendship: mutual) |

We'll start with **undirected graphs** — friendships, road maps, the simplest case.

---

## How to Store a Graph: Adjacency Lists

A tree stores children with `left` and `right` pointers. A graph node can have any number of connections — so we use a dictionary:

```python
graph = {
    "Alice":   ["Bob", "Charlie"],
    "Bob":     ["Alice", "Diana"],
    "Charlie": ["Alice", "Diana", "Edward"],
    "Diana":   ["Bob", "Charlie"],
    "Edward":  ["Charlie"],
}
```

Each key is a node. Each value is a **list of neighbours** — the nodes it connects to. This is called an **adjacency list**.

```python
# Who is Alice friends with?
print(graph["Alice"])  # ['Bob', 'Charlie']

# Is Bob friends with Edward?
print("Edward" in graph["Bob"])  # False

# How many friends does Charlie have?
print(len(graph["Charlie"]))  # 3
```

That's the entire data structure. A dictionary of lists. No special classes needed — though we'll wrap one shortly.

---

## Step by Step: Building a Graph Class

### Step 1: A Simple Undirected Graph

```python
class Graph:
    def __init__(self):
        self.adj = {}  # node → list of neighbours

    def add_node(self, node):
        """Add a node if it doesn't already exist."""
        if node not in self.adj:
            self.adj[node] = []

    def add_edge(self, u, v):
        """Add an undirected edge between u and v."""
        # Make sure both nodes exist
        if u not in self.adj:
            self.add_node(u)
        if v not in self.adj:
            self.add_node(v)
        # Add each to the other's neighbour list
        self.adj[u].append(v)
        self.adj[v].append(u)

    def neighbours(self, node):
        """Return the neighbours of a node."""
        return self.adj.get(node, [])

    def __str__(self):
        result = ""
        for node, neighbours in self.adj.items():
            result += f"  {node} → {neighbours}\n"
        return f"Graph:\n{result}"
```

```python
g = Graph()
g.add_edge("Alice", "Bob")
g.add_edge("Alice", "Charlie")
g.add_edge("Bob", "Diana")
g.add_edge("Charlie", "Diana")
g.add_edge("Charlie", "Edward")

print(g)
# Graph:
#   Alice → ['Bob', 'Charlie']
#   Bob → ['Alice', 'Diana']
#   Charlie → ['Alice', 'Diana', 'Edward']
#   Diana → ['Bob', 'Charlie']
#   Edward → ['Charlie']
```

`add_edge(u, v)` does the crucial thing: it adds `v` to `u`'s list AND `u` to `v`'s list. That's what makes it undirected — the connection goes both ways.

---

## The Core Question: How Do You Explore a Graph?

Trees have a natural order — start at the root, go down. Graphs don't have a root. You pick a starting node and explore outward.

But which direction? The two classic strategies:

| Strategy | How it explores | Data structure | Best for |
|----------|----------------|----------------|----------|
| **BFS** (Breadth-First Search) | Ring by ring, like ripples in water | Queue | Shortest path |
| **DFS** (Depth-First Search) | Follows one path to the end before backtracking | Stack (or recursion) | Exploring all paths |

This lesson covers BFS. The next covers DFS.

---

## BFS: Explore Ring by Ring

Imagine you're at a party and want to find someone. You could:

1. Ask everyone in the room you're in (ring 0 — yourself)
2. Ask everyone in the next room (ring 1 — direct friends)
3. Ask everyone in the room after that (ring 2 — friends of friends)
4. Keep going outward until you find them

That's **Breadth-First Search**. You explore level by level — all nodes at distance 1, then all at distance 2, then all at distance 3.

```
Starting from Alice:

Distance 0:  Alice
Distance 1:  Bob, Charlie          ← all of Alice's friends
Distance 2:  Diana, Edward         ← friends of Bob + Charlie
```

The key insight: BFS uses a **queue** (remember Lesson 9?). You add neighbours to the queue and process them in order — first in, first out. That guarantees you see closer nodes before farther ones.

---

### Step 2: Basic BFS Traversal

```python
from collections import deque


def bfs(graph, start):
    """Visit every node reachable from start, in BFS order."""
    visited = set()
    queue = deque([start])
    visited.add(start)
    order = []

    while queue:
        current = queue.popleft()   # Take from the front
        order.append(current)

        for neighbour in graph.neighbours(current):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)   # Add to the back

    return order
```

Let's trace it on our friendship graph starting from Alice:

```
Start:  queue = [Alice], visited = {Alice}

Pop Alice → order = [Alice]
  Neighbours: Bob, Charlie
  Bob not visited → queue = [Bob], visited = {Alice, Bob}
  Charlie not visited → queue = [Bob, Charlie], visited = {Alice, Bob, Charlie}

Pop Bob → order = [Alice, Bob]
  Neighbours: Alice (visited, skip), Diana
  Diana not visited → queue = [Charlie, Diana], visited = {Alice, Bob, Charlie, Diana}

Pop Charlie → order = [Alice, Bob, Charlie]
  Neighbours: Alice (skip), Diana (skip), Edward
  Edward not visited → queue = [Diana, Edward], visited = {Alice, Bob, Charlie, Diana, Edward}

Pop Diana → order = [Alice, Bob, Charlie, Diana]
  Neighbours: Bob (skip), Charlie (skip)

Pop Edward → order = [Alice, Bob, Charlie, Diana, Edward]
  Neighbours: Charlie (skip)

Done! BFS order: Alice → Bob → Charlie → Diana → Edward
```

Notice the order: Alice first, then ALL her friends (Bob, Charlie), then friends-of-friends (Diana, Edward). Ring by ring. 🎯

---

### Step 3: Finding the Shortest Path

BFS doesn't just visit nodes — it finds the **shortest path** (fewest edges) from start to any reachable node. Here's why:

- BFS visits nodes in order of distance from the start
- The first time you reach a node, you've found the shortest path to it
- All you need is to track "who discovered whom"

```python
def bfs_shortest_path(graph, start, target):
    """Return the shortest path from start to target, or None if unreachable."""
    if start == target:
        return [start]

    visited = set()
    queue = deque([start])
    visited.add(start)

    # parent[node] = who discovered this node
    parent = {start: None}

    while queue:
        current = queue.popleft()

        for neighbour in graph.neighbours(current):
            if neighbour not in visited:
                visited.add(neighbour)
                parent[neighbour] = current   # "current discovered neighbour"
                queue.append(neighbour)

                if neighbour == target:
                    # Reconstruct the path backwards
                    path = []
                    node = target
                    while node is not None:
                        path.append(node)
                        node = parent[node]
                    path.reverse()
                    return path

    return None  # Target not reachable
```

The `parent` dictionary is the magic: `parent["Diana"] = "Bob"` means "Bob discovered Diana." When we find the target, we walk backwards through `parent` to reconstruct the full path.

```python
g = Graph()
g.add_edge("Alice", "Bob")
g.add_edge("Alice", "Charlie")
g.add_edge("Bob", "Diana")
g.add_edge("Charlie", "Diana")
g.add_edge("Charlie", "Edward")

print(bfs_shortest_path(g, "Alice", "Edward"))
# ['Alice', 'Charlie', 'Edward']   ← 2 hops, not via Diana

print(bfs_shortest_path(g, "Alice", "Diana"))
# ['Alice', 'Bob', 'Diana']        ← could also be ['Alice', 'Charlie', 'Diana']
#                                      (both are length 2 — equally short)
```

---

## Practice: Degrees of Separation

**Your task:** Build a "degrees of separation" finder for a social network.

You're given a friendship graph. Write a function `degrees_of_separation(graph, person_a, person_b)` that returns the shortest chain of friends connecting them, and the number of steps.

**The Graph class is provided.** You just need to write the function.

```python
from collections import deque


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


def degrees_of_separation(graph, person_a, person_b):
    """Return (path, degrees) or (None, -1) if no connection."""
    # Your code here
    pass


# Test
network = Graph()
network.add_edge("Szonja", "Arthur")
network.add_edge("Arthur", "Cece")
network.add_edge("Cece", "David")
network.add_edge("David", "Elena")
network.add_edge("Szonja", "Frank")
network.add_edge("Frank", "Elena")

path, degrees = degrees_of_separation(network, "Szonja", "Elena")
print(f"Path: {path}")      # ['Szonja', 'Frank', 'Elena']  (2 degrees)
print(f"Degrees: {degrees}")  # 2

# Test direct connection
path, degrees = degrees_of_separation(network, "Szonja", "Arthur")
print(f"Direct: {path} → {degrees} degree(s)")  # ['Szonja', 'Arthur'] → 1

# Test no connection
network.add_node("Ghost")  # Isolated — no edges
path, degrees = degrees_of_separation(network, "Szonja", "Ghost")
print(f"No connection: {path}, {degrees}")  # None, -1
```

**Hint:** This is exactly `bfs_shortest_path` but wrapped to return `(path, len(path) - 1)`. The degrees is one less than the path length (path length counts people; degrees counts handshakes between them).

Save as `degrees_of_separation.py` and try it!

---

## Solution

```python
from collections import deque


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


def degrees_of_separation(graph, person_a, person_b):
    """Return (path, degrees) or (None, -1) if no connection."""
    if person_a == person_b:
        return [person_a], 0

    if person_a not in graph.adj or person_b not in graph.adj:
        return None, -1

    visited = set()
    queue = deque([person_a])
    visited.add(person_a)
    parent = {person_a: None}

    while queue:
        current = queue.popleft()

        for neighbour in graph.neighbours(current):
            if neighbour not in visited:
                visited.add(neighbour)
                parent[neighbour] = current
                queue.append(neighbour)

                if neighbour == person_b:
                    # Reconstruct path
                    path = []
                    node = person_b
                    while node is not None:
                        path.append(node)
                        node = parent[node]
                    path.reverse()
                    return path, len(path) - 1

    return None, -1


# Test
network = Graph()
network.add_edge("Szonja", "Arthur")
network.add_edge("Arthur", "Cece")
network.add_edge("Cece", "David")
network.add_edge("David", "Elena")
network.add_edge("Szonja", "Frank")
network.add_edge("Frank", "Elena")

path, degrees = degrees_of_separation(network, "Szonja", "Elena")
print(f"Path: {path}")
print(f"Degrees: {degrees}")

path, degrees = degrees_of_separation(network, "Szonja", "Arthur")
print(f"Direct: {path} → {degrees} degree(s)")

network.add_node("Ghost")
path, degrees = degrees_of_separation(network, "Szonja", "Ghost")
print(f"No connection: {path}, {degrees}")
```

The `parent` dictionary is the key to BFS pathfinding. It's a breadcrumb trail — every node remembers who discovered it. Walk backwards from the target and you get the shortest path.

---

## Real BFS: Where You'll See It

- **LinkedIn's "How you're connected"** — BFS from you to the target profile
- **Web crawlers** — BFS from one page to all linked pages
- **Chess AI** — BFS explores moves level by level
- **GPS / Maps** — the building block for Dijkstra's algorithm (weighted BFS)
- **Peer-to-peer networks** — finding other peers in a torrent or blockchain
- **Word Ladder puzzles** — transform "cold" to "warm" changing one letter at a time: cold → cord → card → ward → warm

---

## What You Just Learned

- **Graph** = nodes connected by edges — more flexible than trees
- **Adjacency list** = a dictionary mapping each node to its neighbours
- **Undirected graph** = edges go both ways; `add_edge(u, v)` adds v to u's list AND u to v's list
- **BFS** = breadth-first search — explores ring by ring using a queue
- **BFS guarantees shortest path** (in an unweighted graph) — first time you reach a node is the shortest way
- **The `parent` trick** — track who discovered whom, then walk backwards to reconstruct the path

---

## What's Next?

BFS explores wide. DFS explores deep — it follows one path all the way to the end before backtracking. That's useful for maze solving, cycle detection, and finding ALL paths (not just the shortest).

Next up: **[Lesson 23: Graphs & DFS](23-graphs-dfs.md)** 🔍

---

**Your turn:** Build the degrees-of-separation finder! Then try modifying it to return ALL shortest paths if there are multiple (BFS visits Diana from Bob AND Charlie at the same distance — can you return both paths?). 🕸️💛
