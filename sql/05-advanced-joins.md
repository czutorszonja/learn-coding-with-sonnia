# SQL Lesson 5: Advanced JOINs

**← Back to [Lesson 4: JOINs](04-joins.md)**

---

## What You'll Learn

In this lesson, you'll master:
- Self-joins (joining a table to itself)
- Cross joins (Cartesian products)
- Multiple join conditions
- Joining with multiple columns
- Natural joins

---

## Self-Joins — Joining a Table to Itself

**Plain English:** A self-join is when you join a table to itself. It sounds weird, but it's useful for comparing rows within the same table!

**Real-world analogy:** Imagine you have a list of employees and you want to find who works in the same department. You're comparing the list against itself!

### Example: Employee Hierarchy

**Employees table:**
```
| employee_id | name   | department  | manager_id |
|-------------|--------|-------------|------------|
| 1           | Szonja | Engineering | NULL       |
| 2           | Arthur | Engineering | 1          |
| 3           | Maria  | Sales       | NULL       |
| 4           | David  | Sales       | 3          |
| 5           | Emma   | Engineering | 2          |
| 6           | Liam   | HR          | NULL       |
```

**Notice:**
- `manager_id` is `NULL` for people with no manager (the bosses!)
- Szonja manages Arthur, and Arthur manages Emma
- Maria manages David

### Finding Employees and Their Managers

```sql
SELECT 
    e.name AS employee,
    m.name AS manager,
    e.department
FROM Employees e
INNER JOIN Employees m ON e.manager_id = m.employee_id;
```

**Result:**
```
| employee | manager  | department  |
|----------|----------|-------------|
| Arthur   | Szonja   | Engineering |
| David    | Maria    | Sales       |
| Emma     | Arthur   | Engineering |
```

**How it works:**
1. We use the `Employees` table twice
2. First instance (`e`) = the employee
3. Second instance (`m`) = the manager
4. Join condition: employee's `manager_id` = manager's `employee_id`

**Notice:** Szonja, Maria, and Liam don't appear as employees because they have `NULL` manager_id (no match).

### Including Employees Without Managers

Use `LEFT JOIN` to include everyone:

```sql
SELECT 
    e.name AS employee,
    m.name AS manager,
    e.department
FROM Employees e
LEFT JOIN Employees m ON e.manager_id = m.employee_id;
```

**Result:**
```
| employee | manager | department  |
|----------|---------|-------------|
| Szonja   | NULL    | Engineering |
| Arthur   | Szonja  | Engineering |
| Maria    | NULL    | Sales       |
| David    | Maria   | Sales       |
| Emma     | Arthur  | Engineering |
| Liam     | NULL    | HR          |
```

Now everyone appears! Employees without managers show `NULL` for the manager column.

---

## Cross Join — Cartesian Product

**Plain English:** A `CROSS JOIN` pairs every row from the first table with every row from the second table.

**Warning:** This can create HUGE result sets! If table A has 100 rows and table B has 100 rows, you get 100 × 100 = 10,000 rows!

### Example: Product Sizes and Colors

**Sizes table:**
```
| size_name |
|-----------|
| S         |
| M         |
| L         |
```

**Colors table:**
```
| colour_name |
|-------------|
| Red         |
| Blue        |
| Green       |
```

Now cross join them:

```sql
SELECT size_name, colour_name
FROM Sizes
CROSS JOIN Colors;
```

**Result:**
```
| size_name | colour_name |
|-----------|------------|
| S         | Red        |
| S         | Blue       |
| S         | Green      |
| M         | Red        |
| M         | Blue       |
| M         | Green      |
| L         | Red        |
| L         | Blue       |
| L         | Green      |
```

**What happened:** Every size was paired with every colour (3 × 3 = 9 combinations).

### When to Use CROSS JOIN:
- Generating all possible combinations
- Creating test data
- Building schedule templates (every room × every time slot)

### Cross Join Without the CROSS JOIN Keyword

You can also write it as:

```sql
SELECT size_name, colour_name
FROM Sizes, Colors;
```

**Result:** Same as above! But using `CROSS JOIN` is clearer and recommended.

---

## Multiple Join Conditions

Sometimes you need to match on more than one column.

### Example: Orders and OrderItems

**Orders table:**
```
| order_id | customer_id | order_date  |
|----------|-------------|-------------|
| 1        | 1           | 2024-01-15  |
| 2        | 1           | 2024-01-20  |
| 3        | 2           | 2024-01-18  |
```

**OrderItems table:**
```
| item_id | order_id | product  | quantity |
|---------|----------|----------|----------|
| 1       | 1        | Laptop   | 1        |
| 2       | 1        | Mouse    | 2        |
| 3       | 2        | Keyboard | 1        |
| 4       | 3        | Monitor  | 2        |
```

### Joining on Multiple Columns

If you had a composite key (multiple columns as the primary key), you'd join on all of them:

```sql
SELECT o.order_id, o.customer_id, oi.product, oi.quantity
FROM Orders o
INNER JOIN OrderItems oi 
    ON o.order_id = oi.order_id;
```

**Result:**
```
| order_id | customer_id | product  | quantity |
|----------|-------------|----------|----------|
| 1        | 1           | Laptop   | 1        |
| 1        | 1           | Mouse    | 2        |
| 2        | 1           | Keyboard | 1        |
| 3        | 2           | Monitor  | 2        |
```

### Adding Extra Conditions to the Join

You can add more conditions with `AND`:

```sql
SELECT o.order_id, oi.product, oi.quantity
FROM Orders o
INNER JOIN OrderItems oi 
    ON o.order_id = oi.order_id
    AND oi.quantity > 1;
```

**Result:**
```
| order_id | product | quantity |
|----------|---------|----------|
| 1        | Mouse   | 2        |
| 3        | Monitor | 2        |
```

**Difference from WHERE:**
- Condition in `ON` clause: Filters which rows get joined
- Condition in `WHERE` clause: Filters results after joining

For `INNER JOIN`, they often give the same result. For `LEFT JOIN`, the difference matters!

---

## Joining with Multiple Tables

You can chain multiple JOINs together.

### Example: Customers → Orders → OrderItems → Products

**Products table:**
```
| product_id | product_name | price   |
|------------|--------------|---------|
| 1          | Laptop       | 999.99  |
| 2          | Mouse        | 25.00   |
| 3          | Keyboard     | 75.00   |
| 4          | Monitor      | 300.00  |
```

Now join all four tables:

```sql
SELECT 
    c.name AS customer,
    o.order_id,
    p.product_name,
    oi.quantity,
    p.price
FROM Customers c
INNER JOIN Orders o ON c.customer_id = o.customer_id
INNER JOIN OrderItems oi ON o.order_id = oi.order_id
INNER JOIN Products p ON oi.product_id = p.product_id;
```

**Result:**
```
| customer | order_id | product_name | quantity | price  |
|----------|----------|--------------|----------|--------|
| Szonja   | 1        | Laptop       | 1        | 999.99 |
| Szonja   | 1        | Mouse        | 2        | 25.00  |
| Szonja   | 2        | Keyboard     | 1        | 75.00  |
| Arthur   | 3        | Monitor      | 2        | 300.00 |
```

**Tip:** When joining many tables, use clear aliases and consider breaking complex queries into smaller parts or using CTEs (covered in Lesson 7).

---

## Natural Join

**Plain English:** A `NATURAL JOIN` automatically joins tables based on columns with the same name.

**Warning:** This is risky! If table structure changes, your query might break or give wrong results. Most developers avoid it.

### Example:

```sql
-- Both tables have customer_id column
SELECT *
FROM Customers
NATURAL JOIN Orders;
```

**Result:** Same as `INNER JOIN ... ON Customers.customer_id = Orders.customer_id`

**Why it's risky:**
- You don't explicitly see the join condition
- If a new column with the same name is added, it changes the join behavior
- Harder to read and maintain

**Recommendation:** Always use explicit `JOIN ... ON` syntax instead.

---

## Practice Exercise

**Scenario:** You have a `Teachers` table and a `Classes` table:

**Teachers table:**
```
| teacher_id | name          | department  |
|------------|---------------|-------------|
| 1          | Dr. Smith     | Math        |
| 2          | Dr. Johnson   | Science     |
| 3          | Dr. Williams  | Math        |
| 4          | Dr. Brown     | History     |
```

**Classes table:**
```
| class_id | teacher_id | course_name      | room  |
|----------|------------|------------------|-------|
| 1        | 1          | Algebra 101      | 101   |
| 2        | 1          | Calculus         | 102   |
| 3        | 2          | Physics          | 201   |
| 4        | 3          | Statistics       | 103   |
| 5        | 4          | World History    | 301   |
```

**Copy-paste values for Teachers (AUTO_INCREMENT):**
```sql
('Dr. Smith', 'Math'),
('Dr. Johnson', 'Science'),
('Dr. Williams', 'Math'),
('Dr. Brown', 'History');
```

**Copy-paste values for Classes (AUTO_INCREMENT):**
```sql
(1, 'Algebra 101', '101'),
(1, 'Calculus', '102'),
(2, 'Physics', '201'),
(3, 'Statistics', '103'),
(4, 'World History', '301');
```

**Your tasks:**

1. Get all teachers with their classes (use INNER JOIN)
2. Get ALL teachers, even those without classes (use LEFT JOIN)
3. Find teachers who are NOT teaching any class
4. Get teacher name, department, and course name for all classes
5. Find all Math department teachers and their courses (use multiple conditions)

**Try it yourself first!** Then scroll down to check your answers.

---

## Solutions

```sql
-- 1. All teachers with their classes (INNER JOIN)
SELECT t.name, c.course_name
FROM Teachers t
INNER JOIN Classes c ON t.teacher_id = c.teacher_id;

-- 2. ALL teachers, even without classes (LEFT JOIN)
SELECT t.name, c.course_name
FROM Teachers t
LEFT JOIN Classes c ON t.teacher_id = c.teacher_id;

-- 3. Teachers NOT teaching any class (LEFT JOIN + WHERE NULL)
SELECT t.name
FROM Teachers t
LEFT JOIN Classes c ON t.teacher_id = c.teacher_id
WHERE c.class_id IS NULL;

-- 4. Teacher name, department, and course
SELECT t.name, t.department, c.course_name
FROM Teachers t
INNER JOIN Classes c ON t.teacher_id = c.teacher_id;

-- 5. Math department teachers and their courses
SELECT t.name, c.course_name
FROM Teachers t
INNER JOIN Classes c ON t.teacher_id = c.teacher_id
WHERE t.department = 'Math';
```

---

## Quick Recap

- **Self-join:** Join a table to itself (use aliases!)
- **Cross join:** Every row × every row (Cartesian product)
- **Multiple join conditions:** Use `AND` in the `ON` clause
- **Multiple table joins:** Chain JOINs together
- **Natural join:** Automatic join on same column names (avoid it!)
- Table aliases are essential for self-joins and complex queries
- `LEFT JOIN` with `WHERE ... IS NULL` finds unmatched rows

## What's Next?

In **Lesson 6: Subqueries**, you'll learn:
- What subqueries are and when to use them
- Subqueries in the WHERE clause
- Subqueries in the SELECT clause
- Subqueries in the FROM clause
- Correlated subqueries

**Continue to [Lesson 6: Subqueries](06-subqueries.md)**

---

**Your turn:** Try the exercises above. Self-joins and cross joins are tricky but powerful! 💛
