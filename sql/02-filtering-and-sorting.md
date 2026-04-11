# SQL Lesson 2: Filtering and Sorting Data

**← Back to [Lesson 1: What is a Database](01-what-is-a-database.md)**

---

## What You'll Learn

In this lesson, you'll master:
- Filtering data with `WHERE` (beyond simple equality)
- Sorting results with `ORDER BY`
- Combining conditions with `AND`, `OR`, and `NOT`
- Pattern matching with `LIKE`

---

## Filtering with WHERE (Beyond Basics)

You already learned the basics of `WHERE` in Lesson 1. Now let's go deeper!

### Comparison Operators

You can use more than just `=` to filter data:

| Operator | Meaning | Example |
|----------|---------|---------|
| `=` | Equal to | `WHERE age = 30` |
| `<>` or `!=` | Not equal to | `WHERE age <> 30` |
| `>` | Greater than | `WHERE age > 30` |
| `<` | Less than | `WHERE age < 30` |
| `>=` | Greater than or equal to | `WHERE age >= 30` |
| `<=` | Less than or equal to | `WHERE age <= 30` |

**Examples:**

```sql
-- Get movies made after 2010
SELECT * FROM Movies WHERE year > 2010;

-- Get movies with rating less than 5
SELECT * FROM Movies WHERE rating < 5;

-- Get products that cost $50 or more
SELECT * FROM Products WHERE price >= 50;
```

### Filtering Text with LIKE

`LIKE` lets you search for patterns in text using wildcards:

| Wildcard | Meaning | Example |
|----------|---------|---------|
| `%` | Any number of characters | `'Nol%'` matches "Nolan", "Nol" |
| `_` | Exactly one character | `'_ane'` matches "Jane", "Lane" |

**Examples:**

```sql
-- Find directors whose name starts with "Nolan"
SELECT * FROM Movies WHERE director LIKE 'Nolan%';

-- Find movies with "Star" anywhere in the title
SELECT * FROM Movies WHERE title LIKE '%Star%';

-- Find movies with exactly 4 letters (like "Jaws")
SELECT * FROM Movies WHERE title LIKE '____';
```

**Common patterns:**
- `'A%'` — starts with A
- `'%A'` — ends with A
- `'%A%'` — contains A anywhere
- `'_A%'` — A is the second letter

---

## Combining Conditions

### AND — Both conditions must be true

```sql
-- Get Christopher Nolan movies from after 2010
SELECT * FROM Movies 
WHERE director = 'Christopher Nolan' AND year > 2010;
```

**Result:** Only "Interstellar" (2014) and "Tenet" (2020) would match.

### OR — At least one condition must be true

```sql
-- Get movies directed by Nolan OR Tarantino
SELECT * FROM Movies 
WHERE director = 'Christopher Nolan' OR director = 'Quentin Tarantino';
```

**Result:** All movies by either director.

### NOT — Negate a condition

```sql
-- Get all movies EXCEPT Christopher Nolan's
SELECT * FROM Movies 
WHERE director NOT LIKE '%Nolan%';
```

### Combining AND, OR, NOT

You can mix them together! Use parentheses to make it clear:

```sql
-- Get movies from 2010 or later, but only if directed by Nolan
SELECT * FROM Movies 
WHERE year >= 2010 AND director = 'Christopher Nolan';

-- Get action OR sci-fi movies, but not from 2020
SELECT * FROM Movies 
WHERE (genre = 'Action' OR genre = 'Sci-Fi') AND year <> 2020;
```

---

## Sorting Results with ORDER BY

`ORDER BY` sorts your results. By default, it sorts ascending (A-Z, 0-9).

### Basic Sorting

```sql
-- Sort movies by year (oldest first)
SELECT * FROM Movies 
ORDER BY year;

-- Sort movies alphabetically by title
SELECT * FROM Movies 
ORDER BY title;
```

### Descending Order

Add `DESC` to sort in reverse (Z-A, newest first):

```sql
-- Sort movies by year (newest first)
SELECT * FROM Movies 
ORDER BY year DESC;

-- Sort movies by title (Z-A)
SELECT * FROM Movies 
ORDER BY title DESC;
```

### Sorting by Multiple Columns

You can sort by multiple columns. The first column is the primary sort, then the second, and so on:

```sql
-- Sort by director (A-Z), then by year (newest first)
SELECT * FROM Movies 
ORDER BY director ASC, year DESC;
```

**What this does:**
1. Groups movies by director alphabetically
2. Within each director's movies, shows newest first

### ASC vs DESC

- `ASC` = Ascending (default, A-Z, 0-9)
- `DESC` = Descending (Z-A, 9-0)

```sql
-- These are the same (ASC is default):
ORDER BY title ASC;
ORDER BY title;
```

---

## Putting It All Together

Here's the order of SQL clauses:

```sql
SELECT column1, column2
FROM table_name
WHERE condition
ORDER BY column1 DESC;
```

**Full example:**

```sql
-- Get Christopher Nolan movies from 2010 or later, sorted by year (newest first)
SELECT title, director, year
FROM Movies
WHERE director = 'Christopher Nolan' AND year >= 2010
ORDER BY year DESC;
```

**Result:**
```
| title        | director          | year |
|--------------|-------------------|------|
| Tenet        | Christopher Nolan | 2020 |
| Interstellar | Christopher Nolan | 2014 |
| Inception    | Christopher Nolan | 2010 |
```

---

## Practice Exercise

**Scenario:** You have a `Products` table:

```
| id | product_name    | category    | price | stock |
|----|-----------------|-------------|-------|-------|
| 1  | Laptop          | Electronics | 999   | 15    |
| 2  | Mouse           | Electronics | 25    | 50    |
| 3  | Desk Chair      | Furniture   | 150   | 8     |
| 4  | Coffee Table    | Furniture   | 200   | 12    |
| 5  | Notebook        | Stationery  | 5     | 100   |
| 6  | Pen Set         | Stationery  | 12    | 75    |
```

**Your tasks:**

1. Get all products that cost more than $100
2. Get all products in the "Electronics" category
3. Get products that cost less than $50 AND have more than 20 in stock
4. Get all products sorted by price (highest to lowest)
5. Get products sorted by category (A-Z), then by price (lowest to highest)
6. Get products where the product_name starts with "C"
7. Get products that are NOT in the "Stationery" category

**Try it yourself first!** Then scroll down to check your answers.

---

## Solutions

```sql
-- 1. Products costing more than $100
SELECT * FROM Products 
WHERE price > 100;

-- 2. Electronics category only
SELECT * FROM Products 
WHERE category = 'Electronics';

-- 3. Under $50 AND more than 20 in stock
SELECT * FROM Products 
WHERE price < 50 AND stock > 20;

-- 4. Sorted by price (highest first)
SELECT * FROM Products 
ORDER BY price DESC;

-- 5. Sorted by category, then by price
SELECT * FROM Products 
ORDER BY category ASC, price ASC;

-- 6. Products starting with "C"
SELECT * FROM Products 
WHERE product_name LIKE 'C%';

-- 7. NOT in Stationery category
SELECT * FROM Products 
WHERE category NOT LIKE 'Stationery';
```

---

## Quick Recap

- `WHERE` filters rows based on conditions
- Comparison operators: `=`, `<>`, `>`, `<`, `>=`, `<=`
- `LIKE` searches for patterns (`%` = any characters, `_` = one character)
- `AND` = both conditions must be true
- `OR` = at least one condition must be true
- `NOT` = negates a condition
- `ORDER BY` sorts results
- `ASC` = ascending (default), `DESC` = descending
- Can sort by multiple columns

## What's Next?

In **Lesson 3: Aggregate Functions**, you'll learn how to:
- Count rows with `COUNT()`
- Calculate averages with `AVG()`
- Find minimum/maximum values with `MIN()` and `MAX()`
- Sum values with `SUM()`
- Group results with `GROUP BY`

**Continue to [Lesson 3: Aggregate Functions](03-aggregate-functions.md)**

---

**Your turn:** Try the exercises above. If you get stuck, re-read the examples and try again! 💛
