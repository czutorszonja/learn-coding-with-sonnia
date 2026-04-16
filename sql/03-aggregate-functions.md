# SQL Lesson 3: Aggregate Functions

**← Back to [Lesson 2: Filtering and Sorting](02-filtering-and-sorting.md)**

---

## What You'll Learn

In this lesson, you'll master:
- Counting rows with `COUNT()`
- Calculating averages with `AVG()`
- Finding minimum/maximum values with `MIN()` and `MAX()`
- Summing values with `SUM()`
- Grouping results with `GROUP BY`
- Filtering groups with `HAVING`

---

## What are Aggregate Functions?

**Plain English:** Aggregate functions perform calculations on multiple rows and return a single result.

**Real-world analogy:** Imagine you have a list of test scores:
- `COUNT()` tells you how many students took the test
- `AVG()` tells you the class average
- `MIN()` tells you the lowest score
- `MAX()` tells you the highest score
- `SUM()` tells you the total of all scores combined

Instead of looking at each row individually, you're getting summary information about the whole group.

---

## The Five Main Aggregate Functions

Let's use this `Orders` table for our examples:

```
| id | product       | price | quantity |
|----|---------------|-------|----------|
| 1  | Laptop        | 999   | 2        |
| 2  | Mouse         | 25    | 5        |
| 3  | Keyboard      | 75    | 3        |
| 4  | Monitor       | 300   | 2        |
| 5  | Headphones    | 150   | 4        |
```

### 1. COUNT() — Count the Rows

```sql
-- Count all orders
SELECT COUNT(*) FROM Orders;
```

**Result:** `5` (there are 5 orders)

```sql
-- Count orders with quantity greater than 2
SELECT COUNT(*) FROM Orders WHERE quantity > 2;
```

**Result:** `3` (Mouse, Keyboard, and Headphones have quantity > 2. Note: Laptop and Monitor both have quantity = 2, which is NOT greater than 2)

**Tip:** `COUNT(*)` counts all rows. `COUNT(column_name)` counts only non-NULL values in that column.

---

### 2. SUM() — Add Up Values

```sql
-- Total quantity of all items ordered
SELECT SUM(quantity) FROM Orders;
```

**Result:** `16` (2 + 5 + 3 + 2 + 4 = 16)

```sql
-- Total value of all orders (price × quantity)
SELECT SUM(price * quantity) FROM Orders;
```

**Result:** `3,548` (1998 + 125 + 225 + 600 + 600 = 3,548)

---

### 3. AVG() — Calculate the Average

```sql
-- Average price of products
SELECT AVG(price) FROM Orders;
```

**Result:** `309.8` ((999 + 25 + 75 + 300 + 150) ÷ 5 = 309.8)

```sql
-- Average quantity per order
SELECT AVG(quantity) FROM Orders;
```

**Result:** `3.2` (16 ÷ 5 = 3.2)

**Note:** `AVG()` only works with numeric columns.

---

### 4. MIN() — Find the Minimum Value

```sql
-- Cheapest product
SELECT MIN(price) FROM Orders;
```

**Result:** `25` (Mouse is the cheapest)

```sql
-- Smallest order quantity
SELECT MIN(quantity) FROM Orders;
```

**Result:** `2` (Laptop and Monitor both have quantity of 2)

---

### 5. MAX() — Find the Maximum Value

```sql
-- Most expensive product
SELECT MAX(price) FROM Orders;
```

**Result:** `999` (Laptop is the most expensive)

```sql
-- Largest order quantity
SELECT MAX(quantity) FROM Orders;
```

**Result:** `5` (Mouse has the highest quantity)

---

## Combining Aggregate Functions

You can use multiple aggregate functions in one query:

```sql
SELECT 
    COUNT(*) AS total_orders,
    SUM(quantity) AS total_items,
    AVG(price) AS average_price,
    MIN(price) AS lowest_price,
    MAX(price) AS highest_price
FROM Orders;
```

**Result:**
```
| total_orders | total_items | average_price | lowest_price | highest_price |
|--------------|-------------|---------------|--------------|---------------|
| 5            | 16          | 309.8         | 25           | 999           |
```

**Note:** `AS` gives the column a nickname (alias) so it's easier to read.

---

## GROUP BY — Grouping Results

So far, we've been aggregating the entire table. But what if you want to aggregate by category?

**Example:** You have a `Sales` table:

```
| id | product       | category    | price | quantity |
|----|---------------|-------------|-------|----------|
| 1  | Laptop        | Electronics | 999   | 2        |
| 2  | Mouse         | Electronics | 25    | 5        |
| 3  | Desk Chair    | Furniture   | 150   | 3        |
| 4  | Coffee Table  | Furniture   | 200   | 2        |
| 5  | Notebook      | Stationery  | 5     | 10       |
| 6  | Pen Set       | Stationery  | 12    | 8        |
```

### Grouping by Category

```sql
SELECT category, SUM(quantity) AS total_sold
FROM Sales
GROUP BY category;
```

**Result:**
```
| category    | total_sold |
|-------------|------------|
| Electronics | 7          |
| Furniture   | 5          |
| Stationery  | 18         |
```

**What happened:**
1. SQL grouped all rows by `category`
2. For each group, it calculated `SUM(quantity)`
3. Returned one row per category

### Multiple Aggregates per Group

```sql
SELECT 
    category,
    COUNT(*) AS number_of_products,
    SUM(quantity) AS total_sold,
    AVG(price) AS average_price
FROM Sales
GROUP BY category;
```

**Result:**
```
| category    | number_of_products | total_sold | average_price |
|-------------|-------------------|------------|---------------|
| Electronics | 2                 | 7          | 512.0         |
| Furniture   | 2                 | 5          | 175.0         |
| Stationery  | 2                 | 18         | 8.5           |
```

---

## HAVING — Filtering Groups

You learned `WHERE` for filtering rows. `HAVING` is similar, but it filters **groups** (after `GROUP BY`).

**Example:** Get only categories where total sales are greater than 10:

```sql
SELECT category, SUM(quantity) AS total_sold
FROM Sales
GROUP BY category
HAVING SUM(quantity) > 10;
```

**Result:**
```
| category    | total_sold |
|-------------|------------|
| Stationery  | 18         |
```

**Why not use WHERE?** Because `WHERE` filters rows *before* grouping. `HAVING` filters groups *after* grouping.

### WHERE vs HAVING

| Clause | Filters | When | Example |
|--------|---------|------|---------|
| `WHERE` | Rows | Before grouping | `WHERE price > 100` |
| `HAVING` | Groups | After grouping | `HAVING SUM(quantity) > 10` |

**Example using both:**

```sql
-- Get categories where average price > 100, but only count expensive products
SELECT category, AVG(price) AS avg_price
FROM Sales
WHERE price > 50
GROUP BY category
HAVING AVG(price) > 100;
```

---

## ORDER BY with Aggregates

You can sort aggregated results just like regular queries:

```sql
-- Sort categories by total sold (highest first)
SELECT category, SUM(quantity) AS total_sold
FROM Sales
GROUP BY category
ORDER BY total_sold DESC;
```

**Result:**
```
| category    | total_sold |
|-------------|------------|
| Stationery  | 18         |
| Electronics | 7          |
| Furniture   | 5          |
```

---

## Practice Exercise

**Scenario:** You have an `Employees` table:

```
| id | name          | department  | salary | years_employed |
|----|---------------|-------------|--------|----------------|
| 1  | John Smith    | Sales       | 50000  | 5              |
| 2  | Jane Doe      | Sales       | 55000  | 7              |
| 3  | Bob Johnson   | Engineering | 75000  | 10             |
| 4  | Alice Brown   | Engineering | 80000  | 8              |
| 5  | Charlie Wilson| HR          | 45000  | 3              |
| 6  | Diana Lee     | HR          | 48000  | 4              |
```

**Copy-paste values (for AUTO_INCREMENT):**
```sql
('John Smith', 'Sales', 50000, 5),
('Jane Doe', 'Sales', 55000, 7),
('Bob Johnson', 'Engineering', 75000, 10),
('Alice Brown', 'Engineering', 80000, 8),
('Charlie Wilson', 'HR', 45000, 3),
('Diana Lee', 'HR', 48000, 4);
```

**Your tasks:**

1. Count the total number of employees
2. Calculate the total salary budget (sum of all salaries)
3. Find the average salary across all employees
4. Find the highest salary
5. Find the lowest salary
6. Group employees by department and count how many in each
7. Group by department and calculate average salary per department
8. Find departments where the average salary is greater than $50,000
9. Get the total years of experience per department (sum of years_employed)
10. Sort departments by total salary (highest to lowest)

**Try it yourself first!** Then scroll down to check your answers.

---

## Solutions

```sql
-- 1. Count total employees
SELECT COUNT(*) AS total_employees FROM Employees;

-- 2. Total salary budget
SELECT SUM(salary) AS total_budget FROM Employees;

-- 3. Average salary
SELECT AVG(salary) AS average_salary FROM Employees;

-- 4. Highest salary
SELECT MAX(salary) AS highest_salary FROM Employees;

-- 5. Lowest salary
SELECT MIN(salary) AS lowest_salary FROM Employees;

-- 6. Count employees per department
SELECT department, COUNT(*) AS employee_count
FROM Employees
GROUP BY department;

-- 7. Average salary per department
SELECT department, AVG(salary) AS avg_salary
FROM Employees
GROUP BY department;

-- 8. Departments with average salary > $50,000
SELECT department, AVG(salary) AS avg_salary
FROM Employees
GROUP BY department
HAVING AVG(salary) > 50000;

-- 9. Total years of experience per department
SELECT department, SUM(years_employed) AS total_experience
FROM Employees
GROUP BY department;

-- 10. Sort departments by total salary (highest first)
SELECT department, SUM(salary) AS total_salary
FROM Employees
GROUP BY department
ORDER BY total_salary DESC;
```

---

## Quick Recap

- `COUNT()` — counts rows
- `SUM()` — adds up values
- `AVG()` — calculates average
- `MIN()` — finds minimum value
- `MAX()` — finds maximum value
- `GROUP BY` — groups results by a column
- `HAVING` — filters groups (use after `GROUP BY`)
- `WHERE` filters rows, `HAVING` filters groups
- Can use `ORDER BY` with aggregated results

## What's Next?

In **Lesson 4: JOINs**, you'll learn how to:
- Combine data from multiple tables
- Use `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, and `FULL JOIN`
- Understand join conditions and relationships
- Work with complex multi-table queries
- Join multiple tables in one query

**Continue to [Lesson 4: JOINs](04-joins-explained.md)**

---

**Your turn:** Try the exercises above. Take your time — aggregate functions can be tricky at first, but they're incredibly powerful! 💛
