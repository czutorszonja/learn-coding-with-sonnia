# SQL Lesson 9: Date/Time Functions — Working with Dates and Times

**← Back to [Lesson 8: String Functions](08-string-functions.md)**

---

## What You'll Learn

In this lesson, you'll master:
- Getting current date and time
- Extracting parts of dates (year, month, day)
- Formatting dates
- Adding and subtracting time intervals
- Calculating differences between dates
- Date comparison and filtering

---

## Setting Up Example Table

```sql
CREATE TABLE Orders (
    order_id INT,
    customer_name VARCHAR(100),
    order_date DATE,
    shipped_date DATE,
    amount DECIMAL(10,2)
);

INSERT INTO Orders (order_id, customer_name, order_date, shipped_date, amount) VALUES
    (1, 'Szonja', '2024-01-15', '2024-01-17', 999.99),
    (2, 'Arthur', '2024-01-20', '2024-01-22', 25.00),
    (3, 'Maria', '2024-02-01', '2024-02-03', 150.00),
    (4, 'David', '2024-02-14', '2024-02-16', 75.50),
    (5, 'Emma', '2024-03-01', NULL, 300.00);
```

**Notice:** Emma's order has `NULL` for `shipped_date` (not shipped yet).

---

## CURRENT_DATE, CURRENT_TIME, CURRENT_TIMESTAMP

Get the current date and time from the database server.

### CURRENT_DATE — Today's Date

```sql
SELECT CURRENT_DATE AS today;
```

**Result:**
```
| today       |
|-------------|
| 2024-03-15  |
```

### CURRENT_TIME — Current Time

```sql
SELECT CURRENT_TIME AS now;
```

**Result:**
```
| now      |
|----------|
| 14:30:45 |
```

### CURRENT_TIMESTAMP — Date and Time Combined

```sql
SELECT CURRENT_TIMESTAMP AS current_datetime;
```

**Result:**
```
| current_datetime       |
|------------------------|
| 2024-03-15 14:30:45    |
```

### NOW() — Alternative (MySQL, PostgreSQL)

```sql
SELECT NOW() AS current_datetime;
```

Same result as `CURRENT_TIMESTAMP`!

---

## EXTRACT — Get Parts of a Date

`EXTRACT()` pulls out specific parts of a date (year, month, day, etc.).

### Extract Year, Month, Day

```sql
SELECT 
    order_date,
    EXTRACT(YEAR FROM order_date) AS year,
    EXTRACT(MONTH FROM order_date) AS month,
    EXTRACT(DAY FROM order_date) AS day
FROM Orders;
```

**Result:**
```
| order_date | year | month | day |
|------------|------|-------|-----|
| 2024-01-15 | 2024 | 1     | 15  |
| 2024-01-20 | 2024 | 1     | 20  |
| 2024-02-01 | 2024 | 2     | 1   |
| 2024-02-14 | 2024 | 2     | 14  |
| 2024-03-01 | 2024 | 3     | 1   |
```

### Extract Hour, Minute, Second (from TIMESTAMP)

```sql
SELECT 
    CURRENT_TIMESTAMP AS now,
    EXTRACT(HOUR FROM CURRENT_TIMESTAMP) AS hour,
    EXTRACT(MINUTE FROM CURRENT_TIMESTAMP) AS minute,
    EXTRACT(SECOND FROM CURRENT_TIMESTAMP) AS second
FROM Orders
LIMIT 1;
```

**Result:**
```
| now                 | hour | minute | second |
|---------------------|------|--------|--------|
| 2024-03-15 14:30:45 | 14   | 30     | 45     |
```

### Alternative: YEAR(), MONTH(), DAY() Functions

Some databases provide shortcut functions:

```sql
SELECT 
    order_date,
    YEAR(order_date) AS year,
    MONTH(order_date) AS month,
    DAY(order_date) AS day
FROM Orders;
```

Same result as `EXTRACT()`!

---

## DATE_TRUNC — Truncate to Specific Precision

`DATE_TRUNC()` rounds a date down to a specified unit.

### Truncate to Month

```sql
SELECT 
    order_date,
    DATE_TRUNC('month', order_date) AS month_start
FROM Orders;
```

**Result:**
```
| order_date | month_start |
|------------|-------------|
| 2024-01-15 | 2024-01-01  |
| 2024-01-20 | 2024-01-01  |
| 2024-02-01 | 2024-02-01  |
| 2024-02-14 | 2024-02-01  |
| 2024-03-01 | 2024-03-01  |
```

**Use case:** Group orders by month for reporting.

### Truncate to Year

```sql
SELECT 
    order_date,
    DATE_TRUNC('year', order_date) AS year_start
FROM Orders;
```

**Result:**
```
| order_date | year_start  |
|------------|-------------|
| 2024-01-15 | 2024-01-01  |
| 2024-01-20 | 2024-01-01  |
| 2024-02-01 | 2024-01-01  |
| 2024-02-14 | 2024-01-01  |
| 2024-03-01 | 2024-01-01  |
```

All dates become January 1st of their respective year.

---

## TO_CHAR — Format Dates

`TO_CHAR()` converts dates to formatted strings.

### Basic Formatting

```sql
SELECT 
    order_date,
    TO_CHAR(order_date, 'YYYY-MM-DD') AS formatted_date
FROM Orders;
```

**Result:**
```
| order_date | formatted_date |
|------------|----------------|
| 2024-01-15 | 2024-01-15     |
| 2024-01-20 | 2024-01-20     |
| 2024-02-01 | 2024-02-01     |
| 2024-02-14 | 2024-02-14     |
| 2024-03-01 | 2024-03-01     |
```

### Common Format Patterns

| Pattern | Meaning | Example |
|---------|---------|---------|
| `YYYY` | 4-digit year | 2024 |
| `YY` | 2-digit year | 24 |
| `MM` | 2-digit month | 01-12 |
| `DD` | 2-digit day | 01-31 |
| `MONTH` | Full month name | January |
| `Mon` | Abbreviated month | Jan |
| `DAY` | Full day name | Monday |
| `Dy` | Abbreviated day | Mon |

### Examples

```sql
SELECT 
    order_date,
    TO_CHAR(order_date, 'MM/DD/YYYY') AS us_format,
    TO_CHAR(order_date, 'DD/MM/YYYY') AS eu_format,
    TO_CHAR(order_date, 'Month DD, YYYY') AS long_format,
    TO_CHAR(order_date, 'Dy, Mon DD, YYYY') AS pretty_format
FROM Orders;
```

**Result:**
```
| order_date | us_format  | eu_format  | long_format        | pretty_format       |
|------------|------------|------------|--------------------|---------------------|
| 2024-01-15 | 01/15/2024 | 15/01/2024 | January 15, 2024   | Mon, Jan 15, 2024   |
| 2024-01-20 | 01/20/2024 | 20/01/2024 | January 20, 2024   | Sat, Jan 20, 2024   |
| 2024-02-01 | 02/01/2024 | 01/02/2024 | February 01, 2024  | Thu, Feb 01, 2024   |
| 2024-02-14 | 02/14/2024 | 14/02/2024 | February 14, 2024  | Wed, Feb 14, 2024   |
| 2024-03-01 | 03/01/2024 | 01/03/2024 | March 01, 2024     | Fri, Mar 01, 2024   |
```

---

## Adding and Subtracting Time Intervals

### Add Days to a Date

```sql
SELECT 
    order_date,
    order_date + INTERVAL '7 days' AS one_week_later
FROM Orders;
```

**Result:**
```
| order_date | one_week_later |
|------------|----------------|
| 2024-01-15 | 2024-01-22     |
| 2024-01-20 | 2024-01-27     |
| 2024-02-01 | 2024-02-08     |
| 2024-02-14 | 2024-02-21     |
| 2024-03-01 | 2024-03-08     |
```

### Add Months to a Date

```sql
SELECT 
    order_date,
    order_date + INTERVAL '1 month' AS one_month_later
FROM Orders;
```

**Result:**
```
| order_date | one_month_later |
|------------|-----------------|
| 2024-01-15 | 2024-02-15      |
| 2024-01-20 | 2024-02-20      |
| 2024-02-01 | 2024-03-01      |
| 2024-02-14 | 2024-03-14      |
| 2024-03-01 | 2024-04-01      |
```

### Add Years to a Date

```sql
SELECT 
    order_date,
    order_date + INTERVAL '1 year' AS one_year_later
FROM Orders;
```

**Result:**
```
| order_date | one_year_later |
|------------|----------------|
| 2024-01-15 | 2025-01-15     |
| 2024-01-20 | 2025-01-20     |
| 2024-02-01 | 2025-02-01     |
| 2024-02-14 | 2025-02-14     |
| 2024-03-01 | 2025-03-01     |
```

### Subtract Time

```sql
SELECT 
    order_date,
    order_date - INTERVAL '30 days' AS one_month_ago
FROM Orders;
```

**Result:**
```
| order_date | one_month_ago  |
|------------|----------------|
| 2024-01-15 | 2023-12-16     |
| 2024-01-20 | 2023-12-21     |
| 2024-02-01 | 2024-01-02     |
| 2024-02-14 | 2024-01-15     |
| 2024-03-01 | 2024-01-30     |
```

### Alternative: DATE_ADD() and DATE_SUB() (MySQL)

```sql
SELECT 
    order_date,
    DATE_ADD(order_date, INTERVAL 7 DAY) AS one_week_later,
    DATE_SUB(order_date, INTERVAL 30 DAY) AS one_month_ago
FROM Orders;
```

Same result!

---

## Calculating Date Differences

### AGE() — Difference Between Two Dates

```sql
SELECT 
    order_date,
    shipped_date,
    AGE(shipped_date, order_date) AS shipping_time
FROM Orders
WHERE shipped_date IS NOT NULL;
```

**Result:**
```
| order_date | shipped_date | shipping_time |
|------------|--------------|---------------|
| 2024-01-15 | 2024-01-17   | 2 days        |
| 2024-01-20 | 2024-01-22   | 2 days        |
| 2024-02-01 | 2024-02-03   | 2 days        |
| 2024-02-14 | 2024-02-16   | 2 days        |
```

### DATEDIFF() — Difference in Days (MySQL, SQL Server)

```sql
SELECT 
    order_date,
    shipped_date,
    DATEDIFF(shipped_date, order_date) AS days_to_ship
FROM Orders
WHERE shipped_date IS NOT NULL;
```

**Result:**
```
| order_date | shipped_date | days_to_ship |
|------------|--------------|--------------|
| 2024-01-15 | 2024-01-17   | 2            |
| 2024-01-20 | 2024-01-22   | 2            |
| 2024-02-01 | 2024-02-03   | 2            |
| 2024-02-14 | 2024-02-16   | 2            |
```

### Simple Subtraction (PostgreSQL)

```sql
SELECT 
    order_date,
    shipped_date,
    shipped_date - order_date AS days_to_ship
FROM Orders
WHERE shipped_date IS NOT NULL;
```

**Result:** Same as DATEDIFF!

---

## Date Comparison and Filtering

### Filter by Specific Date

```sql
SELECT * FROM Orders
WHERE order_date = '2024-01-15';
```

**Result:** Returns only Szonja's order.

### Filter by Date Range

```sql
SELECT * FROM Orders
WHERE order_date >= '2024-02-01' AND order_date <= '2024-02-28';
```

**Result:** Returns orders from February 2024.

### BETWEEN for Date Ranges

```sql
SELECT * FROM Orders
WHERE order_date BETWEEN '2024-02-01' AND '2024-02-28';
```

Same result, cleaner syntax!

### Filter by Month

```sql
SELECT * FROM Orders
WHERE EXTRACT(MONTH FROM order_date) = 2;
```

**Result:** All February orders.

### Filter by Year

```sql
SELECT * FROM Orders
WHERE EXTRACT(YEAR FROM order_date) = 2024;
```

**Result:** All 2024 orders.

### Find Orders Not Yet Shipped

```sql
SELECT * FROM Orders
WHERE shipped_date IS NULL;
```

**Result:** Emma's order (not shipped yet).

---

## Practice Exercise

**Scenario:** You have an `Employees` table:

**Create the table first:**
```sql
CREATE TABLE Employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    hire_date DATE,
    salary DECIMAL(10,2)
);
```

**Copy-paste values (AUTO_INCREMENT):**
```sql
('Szonja Smith', '2020-01-15', 95000),
('Arthur Johnson', '2019-06-20', 85000),
('Maria Williams', '2021-03-01', 70000),
('David Brown', '2022-02-14', 60000),
('Emma Davis', '2018-11-30', 90000);
```

**Your tasks:**

1. Get current date
2. Extract the year each employee was hired
3. Extract the month each employee was hired
4. Format hire_date as "Month DD, YYYY" (e.g., "January 15, 2020")
5. Calculate when each employee's 5-year anniversary will be
6. Calculate how many days each employee has worked (from hire_date to today)
7. Find employees hired in 2020 or later
8. Find employees hired before 2020

**Try it yourself first!** Then scroll down to check your answers.

---

## Solutions

```sql
-- 1. Get current date
SELECT CURRENT_DATE AS today;

-- 2. Extract hire year
SELECT name, EXTRACT(YEAR FROM hire_date) AS hire_year FROM Employees;

-- 3. Extract hire month
SELECT name, EXTRACT(MONTH FROM hire_date) AS hire_month FROM Employees;

-- 4. Format hire_date as "Month DD, YYYY"
SELECT name, TO_CHAR(hire_date, 'Month DD, YYYY') AS formatted_hire_date FROM Employees;

-- 5. Calculate 5-year anniversary
SELECT name, hire_date, hire_date + INTERVAL '5 years' AS five_year_anniversary FROM Employees;

-- 6. Calculate days worked (PostgreSQL)
SELECT name, hire_date, CURRENT_DATE - hire_date AS days_worked FROM Employees;

-- For MySQL, use:
-- SELECT name, hire_date, DATEDIFF(CURRENT_DATE, hire_date) AS days_worked FROM Employees;

-- 7. Employees hired in 2020 or later
SELECT * FROM Employees
WHERE EXTRACT(YEAR FROM hire_date) >= 2020;

-- 8. Employees hired before 2020
SELECT * FROM Employees
WHERE EXTRACT(YEAR FROM hire_date) < 2020;
```

---

## Quick Recap

- **CURRENT_DATE:** Today's date
- **CURRENT_TIME:** Current time
- **CURRENT_TIMESTAMP:** Current date and time
- **EXTRACT():** Get parts of a date (year, month, day, hour, etc.)
- **DATE_TRUNC():** Round down to specific precision
- **TO_CHAR():** Format dates as strings
- **INTERVAL:** Add or subtract time periods
- **AGE() / DATEDIFF():** Calculate difference between dates
- **Date filtering:** Use `=`, `>`, `<`, `BETWEEN`, `EXTRACT()`
- **NULL dates:** Use `IS NULL` or `IS NOT NULL`
- Date functions vary by database (PostgreSQL, MySQL, SQL Server, Oracle)

## What's Next?

In **Lesson 10: Mathematical Functions**, you'll learn:
- Basic arithmetic operations
- Rounding numbers
- Absolute values
- Power and square root
- Modulo operations
- Random numbers

**Continue to [Lesson 10: Mathematical Functions](10-mathematical-functions.md)**

---

**Your turn:** Try the exercises above. Date/time functions are crucial for reporting and analytics! 💛
