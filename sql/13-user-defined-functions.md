# SQL Lesson 13: User-Defined Functions — Custom Calculations

**← Back to [Lesson 12: Stored Procedures](12-stored-procedures.md)**

---

## What You'll Learn

In this lesson, you'll master:
- What functions are (vs procedures)
- Creating scalar functions (return single value)
- Creating table-valued functions (return table)
- Function parameters and return types
- Deterministic vs non-deterministic functions
- Built-in functions review

---

## What is a User-Defined Function?

**Plain English:** A function is like a stored procedure that returns a value. You can use it in SELECT statements, just like built-in functions.

**Real-world analogy:** Think of a calculator:
- You input numbers (parameters)
- It performs a calculation
- It gives you a result (return value)

A function works the same way — you pass in values, it processes them, and returns a result.

---

## Functions vs Stored Procedures

| Feature | Function | Stored Procedure |
|---------|----------|------------------|
| **Return value** | Must return a value | Optional (can use OUT params) |
| **Usage** | Can use in SELECT | Called with CALL |
| **Parameters** | IN only (usually) | IN, OUT, INOUT |
| **Side effects** | No data modification | Can INSERT, UPDATE, DELETE |
| **Error handling** | Limited | Full TRY-CATCH |
| **Performance** | Optimized for calculations | Optimized for operations |

**Simple rule:** Use functions for calculations, use procedures for actions.

---

## Setting Up Example Table

**Employees table:**
```
| employee_id | name   | department  | salary | hire_date  |
|-------------|--------|-------------|--------|------------|
| 1           | Szonja | Engineering | 95000  | 2020-01-15 |
| 2           | Arthur | Engineering | 85000  | 2019-06-20 |
| 3           | Maria  | Sales       | 70000  | 2021-03-01 |
| 4           | David  | Sales       | 60000  | 2022-02-14 |
| 5           | Emma   | HR          | 75000  | 2018-11-30 |
```

---

## Creating a Scalar Function

Scalar functions return a single value.

### Basic Syntax

```sql
CREATE FUNCTION function_name(parameters)
RETURNS return_type
DETERMINISTIC
BEGIN
    DECLARE variable_name data_type;
    -- Logic here
    RETURN value;
END;
```

### Example: Calculate Annual Bonus

```sql
DELIMITER //

CREATE FUNCTION CalculateBonus(emp_salary DECIMAL(10,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE bonus DECIMAL(10,2);
    
    -- Calculate 10% bonus
    SET bonus = emp_salary * 0.10;
    
    RETURN bonus;
END //

DELIMITER ;
```

### Using the Function

```sql
SELECT name, salary, CalculateBonus(salary) AS annual_bonus
FROM Employees;
```

**Result:**
```
| name   | salary | annual_bonus |
|--------|--------|--------------|
| Szonja | 95000  | 9500.00      |
| Arthur | 85000  | 8500.00      |
| Maria  | 70000  | 7000.00      |
| David  | 60000  | 6000.00      |
| Emma   | 75000  | 7500.00      |
```

---

## Function Parameters

### Single Parameter

```sql
DELIMITER //

CREATE FUNCTION GetTaxAmount(salary DECIMAL(10,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE tax_rate DECIMAL(3,2) DEFAULT 0.20;
    RETURN salary * tax_rate;
END //

DELIMITER ;
```

### Using the Function

```sql
SELECT name, salary, GetTaxAmount(salary) AS tax_amount
FROM Employees;
```

**Result:**
```
| name   | salary | tax_amount |
|--------|--------|------------|
| Szonja | 95000  | 19000.00   |
| Arthur | 85000  | 17000.00   |
| Maria  | 70000  | 14000.00   |
| David  | 60000  | 12000.00   |
| Emma   | 75000  | 15000.00   |
```

### Multiple Parameters

```sql
DELIMITER //

CREATE FUNCTION CalculateNetSalary(
    base_salary DECIMAL(10,2),
    bonus DECIMAL(10,2),
    tax_rate DECIMAL(3,2)
)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE gross_salary DECIMAL(10,2);
    DECLARE tax_amount DECIMAL(10,2);
    
    -- Calculate gross salary
    SET gross_salary = base_salary + bonus;
    
    -- Calculate tax
    SET tax_amount = gross_salary * tax_rate;
    
    -- Return net salary
    RETURN gross_salary - tax_amount;
END //

DELIMITER ;
```

### Using with Multiple Parameters

```sql
SELECT 
    name,
    salary,
    CalculateBonus(salary) AS bonus,
    CalculateNetSalary(salary, CalculateBonus(salary), 0.20) AS net_salary
FROM Employees;
```

**Result:**
```
| name   | salary | bonus  | net_salary |
|--------|--------|--------|------------|
| Szonja | 95000  | 9500.00| 83600.00   |
| Arthur | 85000  | 8500.00| 74800.00   |
| Maria  | 70000  | 7000.00| 61600.00   |
| David  | 60000  | 6000.00| 52800.00   |
| Emma   | 75000  | 7500.00| 66000.00   |
```

---

## DETERMINISTIC vs NONDETERMINISTIC

### DETERMINISTIC Function

Returns the same result for the same input every time.

```sql
CREATE FUNCTION AddNumbers(a INT, b INT)
RETURNS INT
DETERMINISTIC
BEGIN
    RETURN a + b;
END;
```

**Why it matters:** MySQL requires `DETERMINISTIC` for functions used in certain contexts (like generated columns).

### NONDETERMINISTIC Function

Returns different results for the same input (e.g., uses NOW(), RAND()).

```sql
DELIMITER //

CREATE FUNCTION GetRandomNumber(max_value INT)
RETURNS INT
NO SQL
BEGIN
    RETURN FLOOR(RAND() * max_value);
END //

DELIMITER ;
```

### Using the Function

```sql
SELECT GetRandomNumber(100) AS random_num;
```

**Result:**
```
| random_num |
|------------|
| 47         |
```

---

## Table-Valued Functions

Table-valued functions return a table (multiple rows and columns).

**Note:** MySQL doesn't support true table-valued functions like SQL Server. Instead, we use stored procedures with cursors or views. Here's a PostgreSQL example:

### PostgreSQL Example

```sql
CREATE FUNCTION GetEmployeesByDepartment(dept_name VARCHAR)
RETURNS TABLE(
    emp_id INT,
    emp_name VARCHAR,
    emp_salary DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT employee_id, name, salary
    FROM Employees
    WHERE department = dept_name;
END;
$$ LANGUAGE plpgsql;
```

### Using the Function

```sql
SELECT * FROM GetEmployeesByDepartment('Engineering');
```

**Result:**
```
| emp_id | emp_name | emp_salary |
|--------|----------|------------|
| 1      | Szonja   | 95000      |
| 2      | Arthur   | 85000      |
```

### MySQL Alternative: Use a View

```sql
CREATE VIEW EngineeringEmployees AS
SELECT employee_id, name, salary
FROM Employees
WHERE department = 'Engineering';
```

### Using the View

```sql
SELECT * FROM EngineeringEmployees;
```

Same result!

---

## Built-in Functions Review

Let's review common built-in functions you can use alongside your custom functions.

### String Functions

```sql
-- Concatenate strings
SELECT CONCAT('Hello', ' ', 'World') AS greeting;
-- Result: Hello World

-- Convert to uppercase
SELECT UPPER('hello') AS upper_text;
-- Result: HELLO

-- Get string length
SELECT LENGTH('hello') AS length;
-- Result: 5

-- Extract substring
SELECT SUBSTRING('hello world', 1, 5) AS first_word;
-- Result: hello
```

### Mathematical Functions

```sql
-- Round a number
SELECT ROUND(3.14159, 2) AS rounded;
-- Result: 3.14

-- Get absolute value
SELECT ABS(-5) AS absolute;
-- Result: 5

-- Get square root
SELECT SQRT(16) AS square_root;
-- Result: 4

-- Raise to power
SELECT POWER(2, 3) AS power;
-- Result: 8
```

### Date Functions

```sql
-- Get current date
SELECT CURRENT_DATE AS today;

-- Extract year from date
SELECT EXTRACT(YEAR FROM '2024-01-15') AS year;
-- Result: 2024

-- Add interval to date
SELECT DATE_ADD('2024-01-15', INTERVAL 1 MONTH) AS next_month;
-- Result: 2024-02-15

-- Calculate date difference
SELECT DATEDIFF('2024-01-20', '2024-01-15') AS days_diff;
-- Result: 5
```

### Aggregate Functions

```sql
-- Count rows
SELECT COUNT(*) AS total_employees FROM Employees;

-- Sum values
SELECT SUM(salary) AS total_salary FROM Employees;

-- Average
SELECT AVG(salary) AS avg_salary FROM Employees;

-- Minimum
SELECT MIN(salary) AS min_salary FROM Employees;

-- Maximum
SELECT MAX(salary) AS max_salary FROM Employees;
```

---

## Combining Functions

You can nest functions together!

### Example: Format Salary with Tax

```sql
DELIMITER //

CREATE FUNCTION FormatSalaryWithTax(salary DECIMAL(10,2))
RETURNS VARCHAR(50)
DETERMINISTIC
BEGIN
    DECLARE tax DECIMAL(10,2);
    DECLARE net DECIMAL(10,2);
    
    SET tax = salary * 0.20;
    SET net = salary - tax;
    
    RETURN CONCAT('$', FORMAT(net, 2));
END //

DELIMITER ;
```

### Using the Function

```sql
SELECT name, salary, FormatSalaryWithTax(salary) AS net_salary_formatted
FROM Employees;
```

**Result:**
```
| name   | salary | net_salary_formatted |
|--------|--------|----------------------|
| Szonja | 95000  | $76,000.00           |
| Arthur | 85000  | $68,000.00           |
| Maria  | 70000  | $56,000.00           |
| David  | 60000  | $48,000.00           |
| Emma   | 75000  | $60,000.00           |
```

---

## Dropping Functions

To delete a function:

```sql
DROP FUNCTION IF EXISTS function_name;
```

### Example

```sql
DROP FUNCTION IF EXISTS CalculateBonus;
```

---

## Practice Exercise

**Scenario:** You have a `Products` table:

**Products table structure:**
```
| product_id | product_name | price   | stock |
|------------|--------------|---------|-------|
| INT        | VARCHAR      | DECIMAL | INT   |
```

**Products table data:**
```
| product_id | product_name  | price  | stock |
|------------|---------------|--------|-------|
| 1          | Laptop        | 999.99 | 15    |
| 2          | Mouse         | 25.50  | 50    |
| 3          | Keyboard      | 75.00  | 30    |
| 4          | Monitor       | 299.99 | 20    |
| 5          | Headphones    | 149.99 | 25    |
```

**Copy-paste values (AUTO_INCREMENT):**
```sql
('Laptop', 999.99, 15),
('Mouse', 25.50, 50),
('Keyboard', 75.00, 30),
('Monitor', 299.99, 20),
('Headphones', 149.99, 25);
```

**Your tasks:**

1. Create a function `CalculateTotalValue` that takes price and stock, returns total value (price × stock)
2. Create a function `ApplyDiscount` that takes price and discount_percent, returns discounted price
3. Create a function `GetStockStatus` that takes stock quantity, returns "In Stock" if > 0, "Out of Stock" otherwise
4. Create a function `CalculateShippingCost` that takes weight in kg, returns $5 for first kg, $2 for each additional kg
5. Create a function `FormatPrice` that takes a price and returns it formatted with $ symbol and 2 decimal places
6. Use your functions together in a SELECT query showing product name, price, stock, total value, discounted price (10% off), and stock status

**Try it yourself first!** Then scroll down to check your answers.

---

## Solutions

```sql
-- 1. Calculate total value
DELIMITER //
CREATE FUNCTION CalculateTotalValue(price DECIMAL(10,2), stock INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    RETURN price * stock;
END //
DELIMITER ;

-- 2. Apply discount
DELIMITER //
CREATE FUNCTION ApplyDiscount(price DECIMAL(10,2), discount_percent DECIMAL(5,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE discount_amount DECIMAL(10,2);
    SET discount_amount = price * (discount_percent / 100);
    RETURN price - discount_amount;
END //
DELIMITER ;

-- 3. Get stock status
DELIMITER //
CREATE FUNCTION GetStockStatus(stock_qty INT)
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    IF stock_qty > 0 THEN
        RETURN 'In Stock';
    ELSE
        RETURN 'Out of Stock';
    END IF;
END //
DELIMITER ;

-- 4. Calculate shipping cost
DELIMITER //
CREATE FUNCTION CalculateShippingCost(weight_kg DECIMAL(10,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE cost DECIMAL(10,2);
    IF weight_kg <= 1 THEN
        SET cost = 5.00;
    ELSE
        SET cost = 5.00 + ((weight_kg - 1) * 2.00);
    END IF;
    RETURN cost;
END //
DELIMITER ;

-- 5. Format price
DELIMITER //
CREATE FUNCTION FormatPrice(price DECIMAL(10,2))
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    RETURN CONCAT('$', FORMAT(price, 2));
END //
DELIMITER ;

-- 6. Use all functions together
SELECT 
    product_name,
    FormatPrice(price) AS formatted_price,
    stock,
    FormatPrice(CalculateTotalValue(price, stock)) AS total_value,
    FormatPrice(ApplyDiscount(price, 10)) AS discounted_price,
    GetStockStatus(stock) AS status
FROM Products;
```

**Expected Result:**
```
| product_name | formatted_price | stock | total_value   | discounted_price | status     |
|--------------|-----------------|-------|---------------|------------------|------------|
| Laptop       | $999.99         | 15    | $14,999.85    | $899.99          | In Stock   |
| Mouse        | $25.50          | 50    | $1,275.00     | $22.95           | In Stock   |
| Keyboard     | $75.00          | 30    | $2,250.00     | $67.50           | In Stock   |
| Monitor      | $299.99         | 20    | $5,999.80     | $269.99          | In Stock   |
| Headphones   | $149.99         | 25    | $3,749.75     | $134.99          | In Stock   |
```

---

## Quick Recap

- **Function:** Returns a value, can use in SELECT
- **Stored Procedure:** Performs actions, called with CALL
- **Scalar function:** Returns single value
- **Table-valued function:** Returns table (PostgreSQL/SQL Server)
- **DETERMINISTIC:** Same input = same output
- **NONDETERMINISTIC:** Can return different results
- **Parameters:** Pass values into functions
- **RETURN:** Send value back from function
- **DELIMITER:** Change statement separator for complex functions
- **DROP FUNCTION:** Delete a function
- Built-in functions: String, Math, Date, Aggregate
- Can nest and combine functions

---

## Congratulations! 🎉

You've completed all 13 SQL lessons! You now know:

1. What is a Database
2. Filtering and Sorting
3. Aggregate Functions
4. JOINs
5. Advanced JOINs
6. Subqueries
7. Set Operations
8. String Functions
9. Date/Time Functions
10. Mathematical Functions
11. CASE Statements
12. Stored Procedures
13. User-Defined Functions

**What's Next?**

- Practice with real projects
- Explore advanced topics (triggers, indexes, optimization)
- Learn database design and normalisation
- Try different SQL databases (PostgreSQL, SQL Server, Oracle)

Keep practicing, and you'll be a SQL pro in no time! 💛

---

**Your turn:** Try the exercises above. Functions are powerful for reusable calculations! 💛
