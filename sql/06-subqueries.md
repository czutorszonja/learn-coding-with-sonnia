# SQL Lesson 6: Subqueries — Queries Within Queries

**← Back to [Lesson 5: Advanced JOINs](05-advanced-joins.md)**

---

## What You'll Learn

In this lesson, you'll master:
- What subqueries are and when to use them
- Subqueries in the WHERE clause
- Subqueries in the SELECT clause
- Subqueries in the FROM clause
- Correlated subqueries
- IN, EXISTS, and ANY/ALL operators

---

## What is a Subquery?

**Plain English:** A subquery is a query nested inside another query. The inner query runs first, and its result is used by the outer query.

**Real-world analogy:** Imagine you're shopping:
1. First, you find out which stores have the item you want (inner query)
2. Then, you go to those stores to buy it (outer query)

The first step is like a subquery — it gives you information you need for the second step.

---

## Subquery in the WHERE Clause

This is the most common type of subquery.

### Example: Find Products Above Average Price

**Products table:**
```
| product_id | product_name | price   |
|------------|--------------|---------|
| 1          | Laptop       | 999.99  |
| 2          | Mouse        | 25.00   |
| 3          | Keyboard     | 75.00   |
| 4          | Monitor      | 300.00  |
| 5          | Headphones   | 150.00  |
```

**Goal:** Find all products that cost more than the average price.

**Step 1:** Calculate the average price (inner query):
```sql
SELECT AVG(price) FROM Products;
-- Result: 309.998
```

**Step 2:** Use that result in the outer query:
```sql
SELECT product_name, price
FROM Products
WHERE price > (SELECT AVG(price) FROM Products);
```

**Result:**
```
| product_name | price  |
|--------------|--------|
| Laptop       | 999.99 |
| Monitor      | 300.00 |
```

**How it works:**
1. Inner query `(SELECT AVG(price) FROM Products)` runs first
2. It returns `309.998`
3. Outer query becomes: `WHERE price > 309.998`
4. Only Laptop and Monitor match

---

## Subquery with IN Operator

Use `IN` when the subquery returns multiple values.

### Example: Find Customers Who Have Placed Orders

**Customers table:**
```
| customer_id | name   | email              |
|-------------|--------|------------------|
| 1           | Szonja | szonja@email.com |
| 2           | Arthur | arthur@email.com |
| 3           | Maria  | maria@email.com  |
| 4           | David  | david@email.com  |
```

**Orders table:**
```
| order_id | customer_id | product  |
|----------|-------------|----------|
| 1        | 1           | Laptop   |
| 2        | 1           | Mouse    |
| 3        | 2           | Keyboard |
```

**Goal:** Find all customers who have placed at least one order.

```sql
SELECT name, email
FROM Customers
WHERE customer_id IN (SELECT customer_id FROM Orders);
```

**Result:**
```
| name   | email              |
|--------|--------------------|
| Szonja | szonja@email.com   |
| Arthur | arthur@email.com   |
```

**How it works:**
1. Inner query `(SELECT customer_id FROM Orders)` returns: `1, 2`
2. Outer query becomes: `WHERE customer_id IN (1, 2)`
3. Only Szonja (id=1) and Arthur (id=2) match
4. David (id=4) is excluded because he has no orders

### Using NOT IN

Find customers who have NOT placed any orders:

```sql
SELECT name, email
FROM Customers
WHERE customer_id NOT IN (SELECT customer_id FROM Orders);
```

**Result:**
```
| name  | email             |
|-------|-------------------|
| Maria | maria@email.com   |
| David | david@email.com   |
```

---

## Subquery in the SELECT Clause

You can use a subquery as a column in your result.

### Example: Show Each Order with Customer Name

```sql
SELECT 
    order_id,
    product,
    (SELECT name FROM Customers WHERE Customers.customer_id = Orders.customer_id) AS customer_name
FROM Orders;
```

**Result:**
```
| order_id | product  | customer_name |
|----------|----------|---------------|
| 1        | Laptop   | Szonja        |
| 2        | Mouse    | Szonja        |
| 3        | Keyboard | Arthur        |
```

**How it works:**
- For each row in `Orders`, the subquery finds the matching customer name
- The subquery runs once per row (this is called a **correlated subquery**)

### Example: Show Products with Price Compared to Average

```sql
SELECT 
    product_name,
    price,
    (SELECT AVG(price) FROM Products) AS average_price,
    price - (SELECT AVG(price) FROM Products) AS difference
FROM Products;
```

**Result:**
```
| product_name | price  | average_price | difference |
|--------------|--------|---------------|------------|
| Laptop       | 999.99 | 309.998       | 689.992    |
| Mouse        | 25.00  | 309.998       | -284.998   |
| Keyboard     | 75.00  | 309.998       | -234.998   |
| Monitor      | 300.00 | 309.998       | -9.998     |
| Headphones   | 150.00 | 309.998       | -159.998   |
```

---

## Subquery in the FROM Clause

You can treat a subquery result as a temporary table.

### Example: Find Departments with Above-Average Sales

**Sales table:**
```
| sale_id | department  | amount |
|---------|-------------|--------|
| 1       | Electronics | 5000   |
| 2       | Electronics | 3000   |
| 3       | Clothing    | 2000   |
| 4       | Clothing    | 1500   |
| 5       | Food        | 800    |
| 6       | Food        | 1200   |
```

**Goal:** Find departments with total sales above the overall average.

```sql
SELECT department, total_sales
FROM (
    SELECT department, SUM(amount) AS total_sales
    FROM Sales
    GROUP BY department
) AS dept_totals
WHERE total_sales > (SELECT AVG(total_sales) FROM (
    SELECT SUM(amount) AS total_sales
    FROM Sales
    GROUP BY department
) AS averages);
```

**Result:**
```
| department  | total_sales |
|-------------|-------------|
| Electronics | 8000        |
```

**How it works:**
1. Inner subquery groups sales by department
2. This becomes a temporary table called `dept_totals`
3. Outer query filters to show only departments above average

**Tip:** You MUST give the subquery an alias (like `AS dept_totals`).

---

## Correlated Subqueries

**Plain English:** A correlated subquery depends on the outer query. It runs once for each row of the outer query.

### Example: Find Employees Earning More Than Their Department Average

**Employees table:**
```
| employee_id | name   | department  | salary |
|-------------|--------|-------------|--------|
| 1           | Szonja | Engineering | 95000  |
| 2           | Arthur | Engineering | 85000  |
| 3           | Maria  | Sales       | 70000  |
| 4           | David  | Sales       | 60000  |
| 5           | Emma   | Engineering | 90000  |
```

```sql
SELECT 
    name,
    department,
    salary,
    (SELECT AVG(salary) 
     FROM Employees e2 
     WHERE e2.department = e1.department) AS dept_average
FROM Employees e1
WHERE salary > (
    SELECT AVG(salary) 
    FROM Employees e2 
    WHERE e2.department = e1.department
);
```

**Result:**
```
| name   | department  | salary | dept_average |
|--------|-------------|--------|--------------|
| Szonja | Engineering | 95000  | 90000        |
| Maria  | Sales       | 70000  | 65000        |
```

**How correlated subqueries work:**
1. Outer query starts with first employee (Szonja)
2. Inner query calculates Engineering department average
3. Compare Szonja's salary to that average
4. Repeat for each employee

**Performance warning:** Correlated subqueries can be slow on large datasets because they run once per row!

---

## EXISTS Operator

`EXISTS` checks if a subquery returns any rows. It returns `TRUE` or `FALSE`.

### Example: Find Customers Who Have Orders

```sql
SELECT name
FROM Customers
WHERE EXISTS (SELECT 1 FROM Orders WHERE Orders.customer_id = Customers.customer_id);
```

**Result:**
```
| name   |
|--------|
| Szonja |
| Arthur |
```

**How it works:**
- For each customer, the subquery checks if any matching order exists
- If yes, `EXISTS` returns `TRUE` and the customer is included
- If no, `EXISTS` returns `FALSE` and the customer is excluded

### EXISTS vs IN

Both work, but `EXISTS` is often faster:
- `IN` — runs the subquery once, gets all values, then checks
- `EXISTS` — stops as soon as it finds a match (short-circuits)

Use `EXISTS` when:
- You only care if rows exist (not the actual values)
- The subquery might return many rows
- Performance matters

---

## ANY and ALL Operators

### ANY — Compare to Any Value

```sql
-- Find products more expensive than ANY product in the 'Electronics' category
SELECT product_name, price
FROM Products
WHERE price > ANY (SELECT price FROM Products WHERE product_name LIKE '%Laptop%');
```

**Meaning:** Find products more expensive than at least one Laptop.

### ALL — Compare to All Values

```sql
-- Find products more expensive than ALL products in the 'Electronics' category
SELECT product_name, price
FROM Products
WHERE price > ALL (SELECT price FROM Products WHERE product_name LIKE '%Laptop%');
```

**Meaning:** Find products more expensive than every single Laptop.

---

## Practice Exercise

**Scenario:** You have a `Students` table and a `Grades` table:

**Students table:**
```
| student_id | name          | major          |
|------------|---------------|----------------|
| 1          | Emma Wilson   | Computer Science|
| 2          | Liam Brown    | Mathematics    |
| 3          | Olivia Davis  | Physics        |
| 4          | Noah Martinez | Chemistry      |
```

**Grades table:**
```
| grade_id | student_id | course_name       | grade |
|----------|------------|-------------------|-------|
| 1        | 1          | Programming 101   | A     |
| 2        | 1          | Data Structures   | B+    |
| 3        | 2          | Calculus          | A-    |
| 4        | 3          | Quantum Physics   | B     |
```

**Copy-paste values for Students (AUTO_INCREMENT):**
```sql
('Emma Wilson', 'Computer Science'),
('Liam Brown', 'Mathematics'),
('Olivia Davis', 'Physics'),
('Noah Martinez', 'Chemistry');
```

**Copy-paste values for Grades (AUTO_INCREMENT):**
```sql
(1, 'Programming 101', 'A'),
(1, 'Data Structures', 'B+'),
(2, 'Calculus', 'A-'),
(3, 'Quantum Physics', 'B');
```

**Your tasks:**

1. Find students who have received an 'A' grade (use subquery with IN)
2. Find students who have NOT received any grade (use subquery with NOT IN)
3. Show each student with their total number of courses (use subquery in SELECT)
4. Find the highest grade count among all students (use subquery to get MAX)
5. Find students who have more than 1 grade (use subquery in SELECT with WHERE)

**Try it yourself first!** Then scroll down to check your answers.

---

## Solutions

```sql
-- 1. Students who received an 'A' grade
SELECT name
FROM Students
WHERE student_id IN (SELECT student_id FROM Grades WHERE grade = 'A');

-- 2. Students who have NOT received any grade
SELECT name
FROM Students
WHERE student_id NOT IN (SELECT student_id FROM Grades);

-- 3. Each student with their course count
SELECT 
    name,
    (SELECT COUNT(*) FROM Grades g WHERE g.student_id = s.student_id) AS course_count
FROM Students s;

-- 4. Find the highest grade count among all students
SELECT MAX(course_count) AS highest_count
FROM (
    SELECT COUNT(*) AS course_count
    FROM Grades
    GROUP BY student_id
) AS counts;

-- 5. Find students who have more than 1 grade
SELECT name,
       (SELECT COUNT(*) FROM Grades g WHERE g.student_id = s.student_id) AS grade_count
FROM Students s
WHERE (SELECT COUNT(*) FROM Grades g WHERE g.student_id = s.student_id) > 1;
```

---

## Quick Recap

- **Subquery:** Query nested inside another query
- **WHERE clause subquery:** Filter based on subquery result
- **SELECT clause subquery:** Add calculated columns
- **FROM clause subquery:** Treat subquery as a temporary table
- **Correlated subquery:** Depends on outer query, runs once per row
- **IN operator:** Check if value matches any subquery result
- **EXISTS operator:** Check if subquery returns any rows
- **ANY/ALL operators:** Compare to any or all subquery results
- Subqueries in FROM need an alias
- Correlated subqueries can be slow on large datasets

## What's Next?

In **Lesson 7: Set Operations**, you'll learn:
- UNION — combine results from multiple queries
- UNION ALL — combine with duplicates
- INTERSECT — find common rows
- EXCEPT — find differences

**Continue to [Lesson 7: Set Operations](07-set-operations.md)**

---

**Your turn:** Try the exercises above. Subqueries are powerful but can be confusing — practice makes perfect! 💛
