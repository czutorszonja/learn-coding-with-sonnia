# SQL Lesson 4: JOINs — Combining Data from Multiple Tables

**← Back to [Lesson 3: Aggregate Functions](03-aggregate-functions.md)**

---

## What You'll Learn

In this lesson, you'll master:
- What JOINs are and why they matter
- `INNER JOIN` — matching rows only
- `LEFT JOIN` — all rows from left table
- `RIGHT JOIN` — all rows from right table
- `FULL JOIN` — all rows from both tables
- Join conditions and relationships
- Working with multiple tables

---

## What is a JOIN?

**Plain English:** A JOIN combines data from two or more tables based on a related column.

**Real-world analogy:** Imagine you have:
- A **Customers** table with customer info (name, email, phone)
- An **Orders** table with order info (product, price, date)

The Orders table only has `customer_id`, not the customer's name. To see which customer placed which order, you need to JOIN the two tables together.

**Why use JOINs?**
- Avoid duplicating data (normalization)
- Keep related data in separate tables
- Query across relationships

---

## Important: Normalization vs JOINs

This is a common point of confusion! **Normalization** and **JOINs** are related but **completely different** things:

| Concept | What it is | When it happens |
|---------|-----------|-----------------|
| **Normalization** | Database **design** principle | When you **create** the database |
| **JOIN** | Query **operation** | When you **query** the database |

### What is Normalization?

**Normalization** is about organizing your data INTO separate tables in the first place.

**Example WITHOUT normalization (one big table):**

```
| customer_name | customer_email       | product    | price | quantity |
|---------------|----------------------|------------|-------|----------|
| John Smith    | john@email.com       | Laptop     | 999   | 1        |
| John Smith    | john@email.com       | Mouse      | 25    | 2        |
| Jane Doe      | jane@email.com       | Keyboard   | 75    | 1        |
```

**Problem:** John's info is repeated! If he changes his email, you need to update multiple rows.

**Example WITH normalization (two tables):**

**Customers table:**
```
| id | name       | email           |
|----|------------|-----------------|
| 1  | John Smith | john@email.com  |
| 2  | Jane Doe   | jane@email.com  |
```

**Orders table:**
```
| id | customer_id | product  | price | quantity |
|----|-------------|----------|-------|----------|
| 1  | 1           | Laptop   | 999   | 1        |
| 2  | 1           | Mouse    | 25    | 2        |
| 3  | 2           | Keyboard | 75    | 1        |
```

**Benefit:** John's info is stored ONCE. No repetition!

**This is normalization** — splitting data into logical, separate tables.

### So Where Do JOINs Come In?

Once you have normalized tables, you use **JOINs** to bring the data back together when you need it.

```sql
SELECT c.name, c.email, o.product, o.price
FROM Customers AS c
INNER JOIN Orders AS o ON c.id = o.customer_id;
```

**Result:**
```
| name       | email           | product  | price |
|------------|-----------------|----------|-------|
| John Smith | john@email.com  | Laptop   | 999   |
| John Smith | john@email.com  | Mouse    | 25    |
| Jane Doe   | jane@email.com  | Keyboard | 75    |
```

**The JOIN reconstructs** the combined view from the separate tables.

### The Relationship

Think of it like LEGO:

1. **Normalization** = Breaking a big LEGO structure into smaller, organized pieces (by color, size, etc.)
2. **JOIN** = Snapping those pieces together when you want to see the full picture

You **normalize first** (design phase), then you **JOIN later** (query phase).

### Is Normalization Automatic?

**No!** Normalization is a **conscious design decision** YOU make when creating your database.

**When you build your database:**
1. You decide what tables to create ✅ (your design choice)
2. You decide what columns go where ✅ (your design choice)
3. You decide on relationships (foreign keys) ✅ (your design choice)

**Nothing is automatic** — you choose to normalize!

### Why Normalize?

**Benefits:**
- ✅ No duplicate data
- ✅ Easier to update (change in one place)
- ✅ Less storage space
- ✅ Better data integrity

**Trade-off:**
- ❌ Need JOINs to get complete data (slightly more complex queries)

### Simple Rule of Thumb

**Ask yourself:** "Does this piece of information belong HERE, or does it belong somewhere else?"

**Example:**
- Should `customer_email` be in the Orders table? ❌ No! It's about the customer, not the order.
- Should `product_name` be in the Orders table? ❌ No! It's about the product, not the order.
- Should `customer_id` be in the Orders table? ✅ Yes! It links the order to a customer.

### Does This Make Sense?

The timeline:

```
1. Design phase → You NORMALIZE (split into tables)
2. Query phase  → You JOIN (bring back together)
```

**In our lessons:**
- Lesson 1: You learned to CREATE tables (this is where normalization happens!)
- Lesson 4: You learned to JOIN tables (this is how you query normalized data)

---

## The Example Tables

We'll use two tables for most examples:

**Customers table:**
```
| id | name          | email                  | city        |
|----|---------------|------------------------|-------------|
| 1  | John Smith    | john@email.com         | New York    |
| 2  | Jane Doe      | jane@email.com         | Los Angeles |
| 3  | Bob Johnson   | bob@email.com          | Chicago     |
| 4  | Alice Brown   | alice@email.com        | Miami       |
| 5  | Charlie Wilson| charlie@email.com      | Seattle     |
```

**Orders table:**
```
| id | customer_id | product       | price | quantity |
|----|-------------|---------------|-------|----------|
| 1  | 1           | Laptop        | 999   | 1        |
| 2  | 1           | Mouse         | 25    | 2        |
| 3  | 2           | Keyboard      | 75    | 1        |
| 4  | 3           | Monitor       | 300   | 2        |
| 5  | 4           | Headphones    | 150   | 1        |
```

**Key relationship:** `Orders.customer_id` refers to `Customers.id`

---

## INNER JOIN — Matching Rows Only

`INNER JOIN` returns only rows where there's a match in **both** tables.

### Basic INNER JOIN

```sql
SELECT Customers.name, Orders.product, Orders.price
FROM Customers
INNER JOIN Orders ON Customers.id = Orders.customer_id;
```

**Result:**
```
| name          | product    | price |
|---------------|------------|-------|
| John Smith    | Laptop     | 999   |
| John Smith    | Mouse      | 25    |
| Jane Doe      | Keyboard   | 75    |
| Bob Johnson   | Monitor    | 300   |
| Alice Brown   | Headphones | 150   |
```

**What happened:**
1. SQL matched each customer with their orders
2. Only customers WITH orders appear (Charlie Wilson is NOT in the result)
3. Each order shows the customer's name

### Understanding the ON Clause

The `ON` clause specifies how the tables are related:

```sql
ON Customers.id = Orders.customer_id
```

This tells SQL: "Match rows where the customer's id equals the order's customer_id."

### Using Table Aliases

When tables have long names, use aliases:

```sql
SELECT c.name, o.product, o.price
FROM Customers AS c
INNER JOIN Orders AS o ON c.id = o.customer_id;
```

**Result:** Same as above, but shorter to type!

---

## LEFT JOIN — All Rows from Left Table

`LEFT JOIN` returns **all** rows from the left table, plus matching rows from the right table.

### Basic LEFT JOIN

```sql
SELECT c.name, o.product, o.price
FROM Customers AS c
LEFT JOIN Orders AS o ON c.id = o.customer_id;
```

**Result:**
```
| name           | product    | price |
|----------------|------------|-------|
| John Smith     | Laptop     | 999   |
| John Smith     | Mouse      | 25    |
| Jane Doe       | Keyboard   | 75    |
| Bob Johnson    | Monitor    | 300   |
| Alice Brown    | Headphones | 150   |
| Charlie Wilson | NULL       | NULL  |
```

**Key difference:** Charlie Wilson appears now (with NULL values) because he has no orders!

**When to use LEFT JOIN:**
- Find customers who haven't ordered anything
- Include all records from the "main" table
- Don't want to lose data from the left table

---

## RIGHT JOIN — All Rows from Right Table

`RIGHT JOIN` is the opposite of LEFT JOIN — it returns **all** rows from the right table.

### Basic RIGHT JOIN

```sql
SELECT c.name, o.product, o.price
FROM Customers AS c
RIGHT JOIN Orders AS o ON c.id = o.customer_id;
```

**Result:**
```
| name        | product    | price |
|-------------|------------|-------|
| John Smith  | Laptop     | 999   |
| John Smith  | Mouse      | 25    |
| Jane Doe    | Keyboard   | 75    |
| Bob Johnson | Monitor    | 300   |
| Alice Brown | Headphones | 150   |
```

**Note:** In this case, the result is the same as INNER JOIN because every order has a matching customer. But if there was an order with `customer_id = 999` (no matching customer), it would appear with NULL for the customer name.

**When to use RIGHT JOIN:**
- Less common than LEFT JOIN
- When the right table is your "main" table
- Many developers prefer to use LEFT JOIN instead (just swap the table order)

---

## FULL JOIN — All Rows from Both Tables

`FULL JOIN` (or `FULL OUTER JOIN`) returns **all** rows from both tables.

### Basic FULL JOIN

```sql
SELECT c.name, o.product, o.price
FROM Customers AS c
FULL JOIN Orders AS o ON c.id = o.customer_id;
```

**Result:**
```
| name           | product    | price |
|----------------|------------|-------|
| John Smith     | Laptop     | 999   |
| John Smith     | Mouse      | 25    |
| Jane Doe       | Keyboard   | 75    |
| Bob Johnson    | Monitor    | 300   |
| Alice Brown    | Headphones | 150   |
| Charlie Wilson | NULL       | NULL  |
```

**What you get:**
- All customers (including Charlie Wilson with NULL order)
- All orders (if any order had no matching customer, it would appear with NULL customer name)

**Note:** MySQL doesn't support `FULL JOIN` directly. You'd need to use `UNION` of LEFT and RIGHT JOIN.

---

## JOIN Comparison

| Join Type | What it Returns |
|-----------|-----------------|
| `INNER JOIN` | Only matching rows from both tables |
| `LEFT JOIN` | All rows from left table + matches from right |
| `RIGHT JOIN` | All rows from right table + matches from left |
| `FULL JOIN` | All rows from both tables |

**Visual:**
```
Table A: [1, 2, 3, 4]
Table B: [3, 4, 5, 6]

INNER:  [3, 4]
LEFT:   [1, 2, 3, 4]
RIGHT:  [3, 4, 5, 6]
FULL:   [1, 2, 3, 4, 5, 6]
```

---

## JOIN with WHERE Clause

You can filter JOIN results with `WHERE`:

```sql
-- Get orders over $100 with customer names
SELECT c.name, o.product, o.price
FROM Customers AS c
INNER JOIN Orders AS o ON c.id = o.customer_id
WHERE o.price > 100;
```

**Result:**
```
| name        | product    | price |
|-------------|------------|-------|
| John Smith  | Laptop     | 999   |
| Bob Johnson | Monitor    | 300   |
| Alice Brown | Headphones | 150   |
```

---

## JOIN with Aggregate Functions

Combine JOINs with what you learned in Lesson 3:

```sql
-- Total spent by each customer
SELECT c.name, SUM(o.price * o.quantity) AS total_spent
FROM Customers AS c
INNER JOIN Orders AS o ON c.id = o.customer_id
GROUP BY c.name;
```

**Result:**
```
| name          | total_spent |
|---------------|-------------|
| John Smith    | 1049        |
| Jane Doe      | 75          |
| Bob Johnson   | 600         |
| Alice Brown   | 150         |
```

**With LEFT JOIN (includes customers with no orders):**

```sql
SELECT c.name, SUM(o.price * o.quantity) AS total_spent
FROM Customers AS c
LEFT JOIN Orders AS o ON c.id = o.customer_id
GROUP BY c.name;
```

**Result:**
```
| name           | total_spent |
|----------------|-------------|
| John Smith     | 1049        |
| Jane Doe       | 75          |
| Bob Johnson    | 600         |
| Alice Brown    | 150         |
| Charlie Wilson | NULL        |
```

---

## Joining More Than Two Tables

You can JOIN multiple tables in one query:

**Example:** Add a third table — `Products`:

```
| id | product       | category    |
|----|---------------|-------------|
| 1  | Laptop        | Electronics |
| 2  | Mouse         | Electronics |
| 3  | Keyboard      | Electronics |
| 4  | Monitor       | Electronics |
| 5  | Headphones    | Accessories |
```

**Query:**

```sql
SELECT c.name, o.product, p.category, o.price
FROM Customers AS c
INNER JOIN Orders AS o ON c.id = o.customer_id
INNER JOIN Products AS p ON o.product = p.product;
```

**Result:**
```
| name        | product    | category    | price |
|-------------|------------|-------------|-------|
| John Smith  | Laptop     | Electronics | 999   |
| John Smith  | Mouse      | Electronics | 25    |
| Jane Doe    | Keyboard   | Electronics | 75    |
| Bob Johnson | Monitor    | Electronics | 300   |
| Alice Brown | Headphones | Accessories | 150   |
```

---

## Practice Exercise

**Scenario:** You have three tables:

**Employees table:**
```
| id | name          | department_id |
|----|---------------|---------------|
| 1  | John Smith    | 1             |
| 2  | Jane Doe      | 1             |
| 3  | Bob Johnson   | 2             |
| 4  | Alice Brown   | 2             |
| 5  | Charlie Wilson| 3             |
```

**Departments table:**
```
| id | name          | location    |
|----|---------------|-------------|
| 1  | Sales         | New York    |
| 2  | Engineering   | San Francisco|
| 3  | HR            | Chicago     |
| 4  | Marketing     | Boston      |
```

**Projects table:**
```
| id | name           | department_id | budget  |
|----|----------------|---------------|---------|
| 1  | Website Redesign| 1            | 50000   |
| 2  | Mobile App      | 2            | 100000  |
| 3  | Recruitment     | 3            | 30000   |
| 4  | Brand Campaign  | 4            | 75000   |
```

**Your tasks:**

1. Get all employees with their department names
2. Get all employees with their department location
3. Find which department each project belongs to (project name + department name)
4. List all departments and their projects (department name + project name)
5. Find employees who work in the same department as the "Mobile App" project (hint: use department_id)
6. Count how many employees are in each department
7. Find departments that have no employees (hint: use LEFT/RIGHT JOIN)
8. Get the total budget per department

**Try it yourself first!** Then scroll down to check your answers.

---

## Solutions

```sql
-- 1. Employees with department names
SELECT e.name AS employee_name, d.name AS department_name
FROM Employees AS e
INNER JOIN Departments AS d ON e.department_id = d.id;

-- 2. Employees with department location
SELECT e.name AS employee_name, d.location
FROM Employees AS e
INNER JOIN Departments AS d ON e.department_id = d.id;

-- 3. Projects with department names
SELECT p.name AS project_name, d.name AS department_name
FROM Projects AS p
INNER JOIN Departments AS d ON p.department_id = d.id;

-- 4. Departments and their projects
SELECT d.name AS department_name, p.name AS project_name
FROM Departments AS d
INNER JOIN Projects AS p ON d.id = p.department_id;

-- 5. Employees in same department as Mobile App project
SELECT e.name AS employee_name
FROM Employees AS e
INNER JOIN Departments AS d ON e.department_id = d.id
INNER JOIN Projects AS p ON d.id = p.department_id
WHERE p.name = 'Mobile App';

-- 6. Count employees per department
SELECT d.name AS department_name, COUNT(e.id) AS employee_count
FROM Departments AS d
INNER JOIN Employees AS e ON d.id = e.department_id
GROUP BY d.name;

-- 7. Departments with no employees
SELECT d.name AS department_name
FROM Departments AS d
LEFT JOIN Employees AS e ON d.id = e.department_id
WHERE e.id IS NULL;

-- 8. Total budget per department
SELECT d.name AS department_name, SUM(p.budget) AS total_budget
FROM Departments AS d
INNER JOIN Projects AS p ON d.id = p.department_id
GROUP BY d.name;
```

---

## Quick Recap

- `JOIN` combines data from multiple tables
- `INNER JOIN` — only matching rows
- `LEFT JOIN` — all rows from left table + matches
- `RIGHT JOIN` — all rows from right table + matches
- `FULL JOIN` — all rows from both tables
- `ON` clause specifies the join condition
- Use table aliases for cleaner code
- Can JOIN multiple tables
- Can combine with `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`

## What's Next?

In **Lesson 5: Subqueries**, you'll learn how to:
- Write queries inside queries
- Use subqueries in SELECT, FROM, and WHERE clauses
- Compare values against query results
- Solve complex problems with nested queries

**Continue to [Lesson 5: Subqueries](05-subqueries.md)**

---

**Your turn:** Try the exercises above. JOINs are fundamental to SQL — take your time and make sure you understand them! 💛
