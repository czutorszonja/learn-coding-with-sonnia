# SQL Lesson 4: JOINs — Combining Tables

**← Back to [Lesson 3: Aggregate Functions](03-aggregate-functions.md)**

---

## What You'll Learn

In this lesson, you'll master:
- What JOINs are and why you need them
- `INNER JOIN` — matching records only
- `LEFT JOIN` — all from left table, matches from right
- `RIGHT JOIN` — all from right table, matches from left
- `FULL JOIN` — everything from both tables
- Join conditions and relationships

---

## What is a JOIN?

**Plain English:** A JOIN combines data from two or more tables based on a related column.

**Real-world analogy:** Imagine you have two separate lists:
- **List 1:** Customer names and their IDs
- **List 2:** Order details with customer IDs

To see which customer placed which order, you need to match them up using the customer ID. That's what a JOIN does!

---

## Why Use JOINs?

In real databases, data is split across multiple tables (this is called **normalization**). This prevents duplication and keeps things organized.

**Example without normalization (BAD):**
```
| order_id | customer_name | customer_email          | product     | price |
|----------|---------------|-------------------------|-------------|-------|
| 1        | Szonja        | szonja@email.com        | Laptop      | 999   |
| 2        | Szonja        | szonja@email.com        | Mouse       | 25    |
| 3        | Arthur        | arthur@email.com        | Keyboard    | 75    |
```

See the problem? Szonja's info is repeated. If she changes her email, you need to update it in multiple places!

**Example with normalization (GOOD):**
```
Customers table:
| customer_id | name   | email            |
|-------------|--------|------------------|
| 1           | Szonja | szonja@email.com |
| 2           | Arthur | arthur@email.com |

Orders table:
| order_id | customer_id | product  | price |
|----------|-------------|----------|-------|
| 1        | 1           | Laptop   | 999   |
| 2        | 1           | Mouse    | 25    |
| 3        | 2           | Keyboard | 75    |
```

Now each customer appears only once. To get complete order info with customer names, you use a JOIN!

---

## Setting Up Example Tables

Let's create two tables to practice with:

```sql
-- Customers table
CREATE TABLE Customers (
    customer_id INT,
    name VARCHAR(100),
    email VARCHAR(100)
);

INSERT INTO Customers (customer_id, name, email) VALUES
    (1, 'Szonja', 'szonja@email.com'),
    (2, 'Arthur', 'arthur@email.com'),
    (3, 'Maria', 'maria@email.com'),
    (4, 'David', 'david@email.com');

-- Orders table
CREATE TABLE Orders (
    order_id INT,
    customer_id INT,
    product VARCHAR(100),
    price INT
);

INSERT INTO Orders (order_id, customer_id, product, price) VALUES
    (1, 1, 'Laptop', 999),
    (2, 1, 'Mouse', 25),
    (3, 2, 'Keyboard', 75),
    (4, 2, 'Monitor', 300),
    (5, 3, 'Headphones', 150);
```

**Notice:**
- Customer 1 (Szonja) has 2 orders
- Customer 2 (Arthur) has 2 orders
- Customer 3 (Maria) has 1 order
- Customer 4 (David) has NO orders yet

---

## INNER JOIN — Matching Records Only

`INNER JOIN` returns only rows where there's a match in **both** tables.

```sql
SELECT Customers.name, Orders.product, Orders.price
FROM Customers
INNER JOIN Orders ON Customers.customer_id = Orders.customer_id;
```

**Result:**
```
| name   | product    | price |
|--------|------------|-------|
| Szonja | Laptop     | 999   |
| Szonja | Mouse      | 25    |
| Arthur | Keyboard   | 75    |
| Arthur | Monitor    | 300   |
| Maria  | Headphones | 150   |
```

**Notice:** David is NOT in the results because he has no orders.

### How INNER JOIN Works:
1. SQL looks at each row in `Customers`
2. For each customer, it searches `Orders` for matching `customer_id`
3. Only returns rows where a match exists in BOTH tables

### Using Table Aliases

When tables have long names, use aliases (nicknames):

```sql
SELECT c.name, o.product, o.price
FROM Customers AS c
INNER JOIN Orders AS o ON c.customer_id = o.customer_id;
```

**Result:** Same as above, but cleaner!

**Tip:** `AS` is optional for table aliases:
```sql
FROM Customers c
INNER JOIN Orders o ON c.customer_id = o.customer_id;
```

---

## LEFT JOIN — All from Left, Matches from Right

`LEFT JOIN` returns **all** rows from the left table, and matching rows from the right table. If no match exists, you get `NULL` for the right table's columns.

```sql
SELECT Customers.name, Orders.product, Orders.price
FROM Customers
LEFT JOIN Orders ON Customers.customer_id = Orders.customer_id;
```

**Result:**
```
| name   | product    | price |
|--------|------------|-------|
| Szonja | Laptop     | 999   |
| Szonja | Mouse      | 25    |
| Arthur | Keyboard   | 75    |
| Arthur | Monitor    | 300   |
| Maria  | Headphones | 150   |
| David  | NULL       | NULL  |
```

**Notice:** David IS included now! His order columns show `NULL` because he has no orders.

### When to Use LEFT JOIN:
- Find customers who haven't ordered anything
- Show all products, even if they have no reviews
- List all employees, even if they're not assigned to a project yet

### Example: Find Customers Without Orders

```sql
SELECT Customers.name
FROM Customers
LEFT JOIN Orders ON Customers.customer_id = Orders.customer_id
WHERE Orders.order_id IS NULL;
```

**Result:**
```
| name  |
|-------|
| David |
```

This finds customers where the join produced NULL values (no matching order).

---

## RIGHT JOIN — All from Right, Matches from Left

`RIGHT JOIN` is the opposite of `LEFT JOIN`. It returns **all** rows from the right table, and matching rows from the left table.

```sql
SELECT Customers.name, Orders.product, Orders.price
FROM Customers
RIGHT JOIN Orders ON Customers.customer_id = Orders.customer_id;
```

**Result:**
```
| name   | product    | price |
|--------|------------|-------|
| Szonja | Laptop     | 999   |
| Szonja | Mouse      | 25    |
| Arthur | Keyboard   | 75    |
| Arthur | Monitor    | 300   |
| Maria  | Headphones | 150   |
```

**Notice:** Same as INNER JOIN in this case, because all orders have matching customers.

### When RIGHT JOIN Matters:

Imagine an Orders table with an order that has no matching customer (maybe the customer was deleted):

```sql
-- Add an order with no matching customer
INSERT INTO Orders (order_id, customer_id, product, price) 
VALUES (6, 99, 'Mystery Item', 500);

-- Now RIGHT JOIN shows it:
SELECT Customers.name, Orders.product
FROM Customers
RIGHT JOIN Orders ON Customers.customer_id = Orders.customer_id;
```

**Result:**
```
| name   | product      |
|--------|--------------|
| Szonja | Laptop       |
| Szonja | Mouse        |
| Arthur | Keyboard     |
| Arthur | Monitor      |
| Maria  | Headphones   |
| NULL   | Mystery Item |
```

**Tip:** In practice, `LEFT JOIN` is more common than `RIGHT JOIN`. You can usually rewrite a RIGHT JOIN as a LEFT JOIN by swapping the table order.

---

## FULL JOIN — Everything from Both Tables

`FULL JOIN` (or `FULL OUTER JOIN`) returns **all** rows from both tables, matching where possible.

```sql
SELECT Customers.name, Orders.product
FROM Customers
FULL JOIN Orders ON Customers.customer_id = Orders.customer_id;
```

**Result:**
```
| name   | product      |
|--------|--------------|
| Szonja | Laptop       |
| Szonja | Mouse        |
| Arthur | Keyboard     |
| Arthur | Monitor      |
| Maria  | Headphones   |
| David  | NULL         |
| NULL   | Mystery Item |
```

**Notice:**
- David appears (customer with no order)
- "Mystery Item" appears (order with no customer)
- Everyone else is matched normally

**Important:** MySQL does NOT support `FULL JOIN`. You need to use `UNION` of LEFT and RIGHT JOINs instead.

---

## Joining More Than Two Tables

You can chain multiple JOINs together!

**Example:** Add an `OrderItems` table:

```sql
CREATE TABLE OrderItems (
    item_id INT,
    order_id INT,
    product VARCHAR(100),
    quantity INT
);

INSERT INTO OrderItems (item_id, order_id, product, quantity) VALUES
    (1, 1, 'Laptop', 1),
    (2, 2, 'Mouse', 2),
    (3, 3, 'Keyboard', 1),
    (4, 4, 'Monitor', 2),
    (5, 5, 'Headphones', 3);
```

Now join all three tables:

```sql
SELECT 
    c.name AS customer,
    o.order_id,
    oi.product,
    oi.quantity
FROM Customers c
INNER JOIN Orders o ON c.customer_id = o.customer_id
INNER JOIN OrderItems oi ON o.order_id = oi.order_id;
```

**Result:**
```
| customer | order_id | product    | quantity |
|----------|----------|------------|----------|
| Szonja   | 1        | Laptop     | 1        |
| Szonja   | 2        | Mouse      | 2        |
| Arthur   | 3        | Keyboard   | 1        |
| Arthur   | 4        | Monitor    | 2        |
| Maria    | 5        | Headphones | 3        |
```

**How it works:**
1. First JOIN: Customers → Orders (match on customer_id)
2. Second JOIN: Result → OrderItems (match on order_id)

---

## Practice Exercise

**Scenario:** You have a `Students` table and an `Enrollments` table:

**Students table:**
```
| student_id | name          | major          |
|------------|---------------|----------------|
| 1          | Emma Wilson   | Computer Science|
| 2          | Liam Brown    | Mathematics    |
| 3          | Olivia Davis  | Physics        |
| 4          | Noah Martinez | Chemistry      |
```

**Enrollments table:**
```
| enrollment_id | student_id | course_name       | grade |
|---------------|------------|-------------------|-------|
| 1             | 1          | Programming 101   | A     |
| 2             | 1          | Data Structures   | B+    |
| 3             | 2          | Calculus          | A-    |
| 4             | 3          | Quantum Physics   | B     |
```

**Copy-paste values for Students (AUTO_INCREMENT):**
```sql
('Emma Wilson', 'Computer Science'),
('Liam Brown', 'Mathematics'),
('Olivia Davis', 'Physics'),
('Noah Martinez', 'Chemistry');
```

**Copy-paste values for Enrollments (AUTO_INCREMENT):**
```sql
(1, 'Programming 101', 'A'),
(1, 'Data Structures', 'B+'),
(2, 'Calculus', 'A-'),
(3, 'Quantum Physics', 'B');
```

**Your tasks:**

1. Get all students with their enrolled courses (use INNER JOIN)
2. Get ALL students, even those not enrolled in any course (use LEFT JOIN)
3. Get all enrollments, even if the student doesn't exist (use RIGHT JOIN)
4. Find students who are NOT enrolled in any course
5. Get student name, course name, and grade for all enrollments

**Try it yourself first!** Then scroll down to check your answers.

---

## Solutions

```sql
-- 1. All students with their courses (INNER JOIN)
SELECT s.name, e.course_name
FROM Students s
INNER JOIN Enrollments e ON s.student_id = e.student_id;

-- 2. ALL students, even unenrolled (LEFT JOIN)
SELECT s.name, e.course_name
FROM Students s
LEFT JOIN Enrollments e ON s.student_id = e.student_id;

-- 3. ALL enrollments, even missing students (RIGHT JOIN)
SELECT s.name, e.course_name
FROM Students s
RIGHT JOIN Enrollments e ON e.student_id = s.student_id;

-- 4. Students NOT enrolled (LEFT JOIN + WHERE NULL)
SELECT s.name
FROM Students s
LEFT JOIN Enrollments e ON s.student_id = e.student_id
WHERE e.enrollment_id IS NULL;

-- 5. Student name, course, and grade
SELECT s.name, e.course_name, e.grade
FROM Students s
INNER JOIN Enrollments e ON s.student_id = e.student_id;
```

---

## Quick Recap

- `JOIN` combines data from multiple tables
- `INNER JOIN` — only matching rows from both tables
- `LEFT JOIN` — all from left table, matches from right (NULL if no match)
- `RIGHT JOIN` — all from right table, matches from left (NULL if no match)
- `FULL JOIN` — everything from both tables (not supported in MySQL)
- Use `ON` to specify the join condition
- Table aliases make queries cleaner
- Can chain multiple JOINs together
- `WHERE ... IS NULL` finds unmatched rows after a LEFT JOIN

## What's Next?

In **Lesson 5: Advanced JOINs**, you'll learn:
- Self-joins (joining a table to itself)
- Cross joins (Cartesian products)
- Multiple join conditions
- Join performance tips

**Continue to [Lesson 5: Advanced JOINs](05-advanced-joins.md)**

---

**Your turn:** Try the exercises above. JOINs are fundamental to SQL — practice makes perfect! 💛
