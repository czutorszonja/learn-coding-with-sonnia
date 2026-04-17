# SQL Lesson 7: Set Operations — UNION, INTERSECT, EXCEPT

**← Back to [Lesson 6: Subqueries](06-subqueries.md)**

---

## What You'll Learn

In this lesson, you'll master:
- `UNION` — combine results from multiple queries
- `UNION ALL` — combine with duplicates
- `INTERSECT` — find common rows
- `EXCEPT` — find differences
- Rules for set operations
- Performance considerations

---

## What are Set Operations?

**Plain English:** Set operations combine the results of two or more SELECT queries into a single result set.

**Real-world analogy:** Imagine you have two guest lists for a party:
- List A: People invited by Szonja
- List B: People invited by Arthur

Set operations help you answer questions like:
- **UNION:** Who's on either list? (everyone invited)
- **INTERSECT:** Who's on both lists? (double-invited guests)
- **EXCEPT:** Who's on Szonja's list but not Arthur's?

---

## Setting Up Example Tables

**Customers_A table:**
```
| customer_id | name   | email              |
|-------------|--------|--------------------|
| 1           | Szonja | szonja@email.com   |
| 2           | Arthur | arthur@email.com   |
| 3           | Maria  | maria@email.com    |
```

**Customers_B table:**
```
| customer_id | name   | email              |
|-------------|--------|--------------------|
| 2           | Arthur | arthur@email.com   |
| 3           | Maria  | maria@email.com    |
| 4           | David  | david@email.com    |
```

**Notice:**
- Arthur and Maria appear in BOTH tables
- Szonja is only in table A
- David is only in table B

---

## UNION — Combine Results (No Duplicates)

`UNION` combines results from two queries and removes duplicates.

### Basic UNION

```sql
SELECT name FROM Customers_A
UNION
SELECT name FROM Customers_B;
```

**Result:**
```
| name   |
|--------|
| Szonja |
| Arthur |
| Maria  |
| David  |
```

**How it works:**
1. First query returns: Szonja, Arthur, Maria
2. Second query returns: Arthur, Maria, David
3. UNION combines them and removes duplicates
4. Arthur and Maria appear only once

### UNION with Multiple Columns

```sql
SELECT name, email FROM Customers_A
UNION
SELECT name, email FROM Customers_B;
```

**Result:**
```
| name   | email              |
|--------|--------------------|
| Szonja | szonja@email.com   |
| Arthur | arthur@email.com   |
| Maria  | maria@email.com    |
| David  | david@email.com    |
```

**Important:** Both queries must have the same number of columns, and corresponding columns must have compatible data types.

### UNION with ORDER BY

```sql
SELECT name FROM Customers_A
UNION
SELECT name FROM Customers_B
ORDER BY name;
```

**Result:**
```
| name   |
|--------|
| Arthur |
| David  |
| Maria  |
| Szonja |
```

**Tip:** The `ORDER BY` goes at the END, after all UNION queries.

---

## UNION ALL — Combine Results (With Duplicates)

`UNION ALL` combines results but keeps all duplicates.

```sql
SELECT name FROM Customers_A
UNION ALL
SELECT name FROM Customers_B;
```

**Result:**
```
| name   |
|--------|
| Szonja |
| Arthur |
| Maria  |
| Arthur |
| Maria  |
| David  |
```

**Notice:** Arthur and Maria appear twice!

### When to Use UNION ALL:

- You want to see all occurrences (including duplicates)
- You know there are no duplicates and want better performance
- You're combining truly distinct datasets

### Performance Tip:

`UNION ALL` is faster than `UNION` because it doesn't need to check for and remove duplicates. Use `UNION ALL` when you don't need deduplication.

---

## INTERSECT — Find Common Rows

`INTERSECT` returns only rows that appear in BOTH queries.

```sql
SELECT name FROM Customers_A
INTERSECT
SELECT name FROM Customers_B;
```

**Result:**
```
| name   |
|--------|
| Arthur |
| Maria  |
```

**How it works:**
- First query returns: Szonja, Arthur, Maria
- Second query returns: Arthur, Maria, David
- INTERSECT finds what's common: Arthur, Maria

### INTERSECT with Multiple Columns

```sql
SELECT name, email FROM Customers_A
INTERSECT
SELECT name, email FROM Customers_B;
```

**Result:**
```
| name   | email              |
|--------|--------------------|
| Arthur | arthur@email.com   |
| Maria  | maria@email.com    |
```

**Important:** ALL columns must match for a row to be included.

---

## EXCEPT — Find Differences

`EXCEPT` returns rows from the first query that are NOT in the second query.

### EXCEPT (A minus B)

```sql
SELECT name FROM Customers_A
EXCEPT
SELECT name FROM Customers_B;
```

**Result:**
```
| name   |
|--------|
| Szonja |
```

**How it works:**
- First query returns: Szonja, Arthur, Maria
- Second query returns: Arthur, Maria, David
- EXCEPT removes Arthur and Maria (they're in both)
- Only Szonja remains (she's only in A)

### EXCEPT in Reverse (B minus A)

```sql
SELECT name FROM Customers_B
EXCEPT
SELECT name FROM Customers_A;
```

**Result:**
```
| name  |
|-------|
| David |
```

**Notice:** Now David is the result (he's only in B, not in A).

### EXCEPT vs NOT IN

You can achieve similar results with `NOT IN`:

```sql
-- Using EXCEPT:
SELECT name FROM Customers_A
EXCEPT
SELECT name FROM Customers_B;

-- Equivalent using NOT IN:
SELECT name FROM Customers_A
WHERE name NOT IN (SELECT name FROM Customers_B);
```

Both return: Szonja

**Difference:** `EXCEPT` is often cleaner and more readable.

---

## Rules for Set Operations

### 1. Same Number of Columns

Both queries must have the same number of columns:

```sql
-- ✓ Valid:
SELECT name, email FROM Customers_A
UNION
SELECT name, email FROM Customers_B;

-- ✗ Invalid:
SELECT name FROM Customers_A
UNION
SELECT name, email FROM Customers_B;
-- Error: Different number of columns
```

### 2. Compatible Data Types

Corresponding columns must have compatible data types:

```sql
-- ✓ Valid:
SELECT name, age FROM Customers_A
UNION
SELECT name, age FROM Customers_B;

-- ✗ Problematic:
SELECT name FROM Customers_A
UNION
SELECT email FROM Customers_B;
-- Both are text, so it works, but might not make sense
```

### 3. Column Names Come from First Query

```sql
SELECT name AS customer_name FROM Customers_A
UNION
SELECT name FROM Customers_B;
```

**Result column:** `customer_name` (from the first query)

### 4. ORDER BY Goes at the End

```sql
-- ✓ Valid:
SELECT name FROM Customers_A
UNION
SELECT name FROM Customers_B
ORDER BY name;

-- ✗ Invalid:
SELECT name FROM Customers_A
ORDER BY name
UNION
SELECT name FROM Customers_B;
```

### 5. WHERE Clauses Apply to Individual Queries

```sql
SELECT name FROM Customers_A WHERE customer_id > 1
UNION
SELECT name FROM Customers_B WHERE customer_id > 2;
```

**Result:**
```
| name   |
|--------|
| Arthur |
| Maria  |
| David  |
```

---

## Combining Multiple Set Operations

You can chain multiple set operations together:

```sql
SELECT name FROM Customers_A
UNION
SELECT name FROM Customers_B
EXCEPT
SELECT name FROM Customers_A WHERE customer_id = 2;
```

**How it works:**
1. First UNION combines A and B: Szonja, Arthur, Maria, David
2. Then EXCEPT removes Arthur (customer_id = 2)
3. Final result: Szonja, Maria, David

**Tip:** Use parentheses to make the order clear:

```sql
(SELECT name FROM Customers_A
UNION
SELECT name FROM Customers_B)
EXCEPT
SELECT name FROM Customers_A WHERE customer_id = 2;
```

---

## Practice Exercise

**Scenario:** You have two tables of product orders:

**Orders_January table:**
```
| order_id | product_name  |
|----------|---------------|
| 1        | Laptop        |
| 2        | Mouse         |
| 3        | Keyboard      |
| 4        | Monitor       |
```

**Orders_February table:**
```
| order_id | product_name  |
|----------|---------------|
| 5        | Mouse         |
| 6        | Headphones    |
| 7        | Laptop        |
| 8        | Webcam        |
```

**Copy-paste values for Orders_January (AUTO_INCREMENT):**
```sql
('Laptop'),
('Mouse'),
('Keyboard'),
('Monitor');
```

**Copy-paste values for Orders_February (AUTO_INCREMENT):**
```sql
('Mouse'),
('Headphones'),
('Laptop'),
('Webcam');
```

**Your tasks:**

1. Get all unique products ordered in January OR February
2. Get ALL orders (including duplicates) from both months
3. Find products ordered in BOTH January AND February
4. Find products ordered in January but NOT in February
5. Find products ordered in February but NOT in January

**Try it yourself first!** Then scroll down to check your answers.

---

## Solutions

```sql
-- 1. All unique products (UNION)
SELECT product_name FROM Orders_January
UNION
SELECT product_name FROM Orders_February;

-- 2. All orders including duplicates (UNION ALL)
SELECT product_name FROM Orders_January
UNION ALL
SELECT product_name FROM Orders_February;

-- 3. Products ordered in both months (INTERSECT)
SELECT product_name FROM Orders_January
INTERSECT
SELECT product_name FROM Orders_February;

-- 4. Products in January but not February (EXCEPT)
SELECT product_name FROM Orders_January
EXCEPT
SELECT product_name FROM Orders_February;

-- 5. Products in February but not January (EXCEPT reversed)
SELECT product_name FROM Orders_February
EXCEPT
SELECT product_name FROM Orders_January;
```

**Expected Results:**

1. Unique products: Laptop, Mouse, Keyboard, Monitor, Headphones, Webcam
2. All orders: Laptop, Mouse, Keyboard, Monitor, Mouse, Headphones, Laptop, Webcam
3. Both months: Laptop, Mouse
4. January only: Keyboard, Monitor
5. February only: Headphones, Webcam

---

## Quick Recap

- **UNION:** Combine results, remove duplicates
- **UNION ALL:** Combine results, keep duplicates (faster!)
- **INTERSECT:** Find common rows in both queries
- **EXCEPT:** Find rows in first query but not in second
- Both queries must have same number of columns
- Corresponding columns must have compatible data types
- Column names come from the first query
- `ORDER BY` goes at the end
- Can chain multiple set operations together
- Use parentheses for clarity in complex queries

## What's Next?

In **Lesson 8: String Functions**, you'll learn:
- Concatenating strings
- Changing case (upper/lower)
- Extracting substrings
- Finding string length
- Trimming whitespace
- Replacing text

**Continue to [Lesson 8: String Functions](08-string-functions.md)**

---

**Your turn:** Try the exercises above. Set operations are powerful for combining and comparing datasets! 💛
