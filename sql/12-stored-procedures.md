# SQL Lesson 12: Stored Procedures — Reusable Code Blocks

**← Back to [Lesson 11: CASE Statements](11-case-statements.md)**

---

## What You'll Learn

In this lesson, you'll master:
- What stored procedures are
- Creating and executing procedures
- Parameters (IN, OUT, INOUT)
- Variables in procedures
- Control flow (IF, WHILE, LOOP)
- Error handling basics

---

## What is a Stored Procedure?

**Plain English:** A stored procedure is a saved SQL program that you can run multiple times. It's like a function in programming.

**Real-world analogy:** Imagine a coffee machine:
- You don't need to know how it works internally
- You just press the "espresso" button
- It runs the same steps every time

A stored procedure works the same way — you save a set of SQL commands and run them with one command.

### Benefits of Stored Procedures:

1. **Reusability:** Write once, use many times
2. **Consistency:** Same logic every time
3. **Security:** Grant access to procedure, not underlying tables
4. **Performance:** Pre-compiled and optimized
5. **Maintainability:** Change in one place, affects all uses

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

## Creating a Simple Stored Procedure

### Basic Syntax

```sql
CREATE PROCEDURE procedure_name()
BEGIN
    -- SQL statements go here
END;
```

### Example: Get All Employees

```sql
DELIMITER //

CREATE PROCEDURE GetAllEmployees()
BEGIN
    SELECT * FROM Employees;
END //

DELIMITER ;
```

**Important notes:**
- `DELIMITER //` changes the statement separator from `;` to `//`
- This allows semicolons inside the procedure
- `DELIMITER ;` changes it back after creation

### Calling the Procedure

```sql
CALL GetAllEmployees();
```

**Result:**
```
| employee_id | name   | department  | salary  | hire_date  |
|-------------|--------|-------------|---------|------------|
| 1           | Szonja | Engineering | 95000   | 2020-01-15 |
| 2           | Arthur | Engineering | 85000   | 2019-06-20 |
| 3           | Maria  | Sales       | 70000   | 2021-03-01 |
| 4           | David  | Sales       | 60000   | 2022-02-14 |
| 5           | Emma   | HR          | 75000   | 2018-11-30 |
```

---

## Stored Procedures with Parameters

Parameters let you pass values into procedures.

### IN Parameters (Input Only)

`IN` parameters pass values INTO the procedure.

```sql
DELIMITER //

CREATE PROCEDURE GetEmployeesByDepartment(IN dept_name VARCHAR(100))
BEGIN
    SELECT * FROM Employees
    WHERE department = dept_name;
END //

DELIMITER ;
```

### Calling with Parameter

```sql
CALL GetEmployeesByDepartment('Engineering');
```

**Result:**
```
| employee_id | name   | department  | salary | hire_date  |
|-------------|--------|-------------|--------|------------|
| 1           | Szonja | Engineering | 95000  | 2020-01-15 |
| 2           | Arthur | Engineering | 85000  | 2019-06-20 |
```

### Multiple IN Parameters

```sql
DELIMITER //

CREATE PROCEDURE GetEmployeesByDeptAndSalary(
    IN dept_name VARCHAR(100),
    IN min_salary DECIMAL(10,2)
)
BEGIN
    SELECT * FROM Employees
    WHERE department = dept_name
    AND salary >= min_salary;
END //

DELIMITER ;
```

### Calling with Multiple Parameters

```sql
CALL GetEmployeesByDeptAndSalary('Engineering', 90000);
```

**Result:**
```
| employee_id | name   | department  | salary | hire_date  |
|-------------|--------|-------------|--------|------------|
| 1           | Szonja | Engineering | 95000  | 2020-01-15 |
```

---

## OUT Parameters (Output Only)

`OUT` parameters return values FROM the procedure.

### Example: Count Employees

```sql
DELIMITER //

CREATE PROCEDURE CountEmployees(OUT emp_count INT)
BEGIN
    SELECT COUNT(*) INTO emp_count FROM Employees;
END //

DELIMITER ;
```

### Calling and Getting the Result

```sql
CALL CountEmployees(@total);
SELECT @total AS employee_count;
```

**Result:**
```
| employee_count |
|----------------|
| 5              |
```

**How it works:**
1. `CALL CountEmployees(@total)` runs the procedure
2. `@total` is a session variable that stores the result
3. `SELECT @total` retrieves the value

---

## INOUT Parameters (Input and Output)

`INOUT` parameters pass values in AND get modified values back.

### Example: Increment Counter

```sql
DELIMITER //

CREATE PROCEDURE IncrementValue(INOUT value INT)
BEGIN
    SET value = value + 1;
END //

DELIMITER ;
```

### Calling INOUT Procedure

```sql
SET @num = 5;
CALL IncrementValue(@num);
SELECT @num AS result;
```

**Result:**
```
| result |
|--------|
| 6      |
```

**How it works:**
1. `SET @num = 5` initializes the variable
2. `CALL IncrementValue(@num)` passes 5 in, gets 6 back
3. `SELECT @num` shows the modified value

---

## Variables in Stored Procedures

You can declare local variables inside procedures.

### Example: Calculate Bonus

```sql
DELIMITER //

CREATE PROCEDURE CalculateBonus(IN emp_id INT, OUT bonus_amount DECIMAL(10,2))
BEGIN
    DECLARE emp_salary DECIMAL(10,2);
    DECLARE bonus_rate DECIMAL(3,2);
    
    -- Get employee's salary
    SELECT salary INTO emp_salary
    FROM Employees
    WHERE employee_id = emp_id;
    
    -- Set bonus rate (10% of salary)
    SET bonus_rate = 0.10;
    
    -- Calculate bonus
    SET bonus_amount = emp_salary * bonus_rate;
END //

DELIMITER ;
```

### Calling the Procedure

```sql
CALL CalculateBonus(1, @bonus);
SELECT @bonus AS employee_bonus;
```

**Result:**
```
| employee_bonus |
|----------------|
| 9500.00        |
```

### Variable with Default Value

```sql
DECLARE variable_name data_type DEFAULT value;
```

**Example:**
```sql
DECLARE tax_rate DECIMAL(3,2) DEFAULT 0.20;
```

---

## Control Flow: IF Statements

### Basic IF

```sql
DELIMITER //

CREATE PROCEDURE CheckSalary(IN emp_id INT)
BEGIN
    DECLARE emp_salary DECIMAL(10,2);
    
    SELECT salary INTO emp_salary
    FROM Employees
    WHERE employee_id = emp_id;
    
    IF emp_salary > 80000 THEN
        SELECT 'High earner' AS status;
    ELSE
        SELECT 'Regular earner' AS status;
    END IF;
END //

DELIMITER ;
```

### Calling the Procedure

```sql
CALL CheckSalary(1);
```

**Result:**
```
| status        |
|---------------|
| High earner   |
```

### IF-ELSEIF-ELSE

```sql
DELIMITER //

CREATE PROCEDURE GetSalaryLevel(IN emp_id INT)
BEGIN
    DECLARE emp_salary DECIMAL(10,2);
    
    SELECT salary INTO emp_salary
    FROM Employees
    WHERE employee_id = emp_id;
    
    IF emp_salary >= 90000 THEN
        SELECT 'Executive' AS level;
    ELSEIF emp_salary >= 70000 THEN
        SELECT 'Senior' AS level;
    ELSEIF emp_salary >= 50000 THEN
        SELECT 'Junior' AS level;
    ELSE
        SELECT 'Entry' AS level;
    END IF;
END //

DELIMITER ;
```

### Calling

```sql
CALL GetSalaryLevel(1);
```

**Result:**
```
| level     |
|-----------|
| Executive |
```

---

## Control Flow: CASE Statements

You can use CASE inside procedures too!

```sql
DELIMITER //

CREATE PROCEDURE GetDepartmentBudget(IN dept_name VARCHAR(100))
BEGIN
    DECLARE budget DECIMAL(10,2);
    
    SET budget = CASE dept_name
        WHEN 'Engineering' THEN 500000
        WHEN 'Sales' THEN 300000
        WHEN 'HR' THEN 200000
        ELSE 100000
    END;
    
    SELECT budget AS department_budget;
END //

DELIMITER ;
```

### Calling

```sql
CALL GetDepartmentBudget('Engineering');
```

**Result:**
```
| department_budget |
|-------------------|
| 500000            |
```

---

## Control Flow: WHILE Loop

`WHILE` loops repeat while a condition is true.

### Example: Simple Counter

```sql
DELIMITER //

CREATE PROCEDURE CountToFive()
BEGIN
    DECLARE counter INT DEFAULT 1;
    
    WHILE counter <= 5 DO
        SELECT counter AS current_count;
        SET counter = counter + 1;
    END WHILE;
END //

DELIMITER ;
```

### Calling

```sql
CALL CountToFive();
```

**Result:**
```
| current_count |
|---------------|
| 1             |
| 2             |
| 3             |
| 4             |
| 5             |
```

### Practical Example: Insert Multiple Rows

```sql
DELIMITER //

CREATE PROCEDURE AddMultipleEmployees(IN count INT)
BEGIN
    DECLARE i INT DEFAULT 1;
    
    WHILE i <= count DO
        INSERT INTO Employees (name, department, salary, hire_date)
        VALUES (
            CONCAT('Employee ', i),
            'General',
            50000,
            CURDATE()
        );
        SET i = i + 1;
    END WHILE;
    
    SELECT 'Employees added successfully!' AS message;
END //

DELIMITER ;
```

### Calling

```sql
CALL AddMultipleEmployees(3);
```

**Result:**
```
| message                        |
|--------------------------------|
| Employees added successfully!  |
```

---

## Control Flow: REPEAT Loop

`REPEAT` loops run at least once, then repeat while condition is true.

```sql
DELIMITER //

CREATE PROCEDURE CountDown(IN start_num INT)
BEGIN
    DECLARE counter INT DEFAULT start_num;
    
    REPEAT
        SELECT counter AS countdown;
        SET counter = counter - 1;
    UNTIL counter < 1
    END REPEAT;
    
    SELECT 'Blast off!' AS message;
END //

DELIMITER ;
```

### Calling

```sql
CALL CountDown(3);
```

**Result:**
```
| countdown |
|-----------|
| 3         |
| 2         |
| 1         |
| message   |
|-----------|
| Blast off!|
```

---

## Error Handling

Use `DECLARE HANDLER` to handle errors gracefully.

### Example: Handle Duplicate Key

```sql
DELIMITER //

CREATE PROCEDURE AddEmployeeSafe(
    IN emp_name VARCHAR(100),
    IN dept VARCHAR(100),
    IN sal DECIMAL(10,2)
)
BEGIN
    DECLARE duplicate_key CONDITION FOR SQLSTATE '23000';
    DECLARE EXIT HANDLER FOR duplicate_key
    BEGIN
        SELECT 'Error: Employee already exists!' AS message;
    END;
    
    INSERT INTO Employees (name, department, salary)
    VALUES (emp_name, dept, sal);
    
    SELECT 'Employee added successfully!' AS message;
END //

DELIMITER ;
```

### Testing Error Handling

```sql
CALL AddEmployeeSafe('Szonja', 'Engineering', 95000);
```

**Result:**
```
| message                        |
|--------------------------------|
| Error: Employee already exists!|
```

---

## Dropping Stored Procedures

To delete a procedure:

```sql
DROP PROCEDURE IF EXISTS procedure_name;
```

### Example

```sql
DROP PROCEDURE IF EXISTS GetAllEmployees;
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

1. Create a procedure `GetAllProducts` that returns all products
2. Create a procedure `GetProductById` that takes a product_id parameter
3. Create a procedure `GetProductsByPriceRange` that takes min_price and max_price parameters
4. Create a procedure `GetTotalStock` that returns the total stock count (OUT parameter)
5. Create a procedure `UpdateStock` that takes product_id and quantity, and updates the stock
6. Create a procedure `CheckStockStatus` that returns "In Stock" if stock > 0, "Out of Stock" otherwise
7. Create a procedure `AddNewProduct` that adds a new product with name, price, and stock parameters

**Try it yourself first!** Then scroll down to check your answers.

---

## Solutions

```sql
-- 1. Get all products
DELIMITER //
CREATE PROCEDURE GetAllProducts()
BEGIN
    SELECT * FROM Products;
END //
DELIMITER ;

-- 2. Get product by ID
DELIMITER //
CREATE PROCEDURE GetProductById(IN prod_id INT)
BEGIN
    SELECT * FROM Products WHERE product_id = prod_id;
END //
DELIMITER ;

-- 3. Get products by price range
DELIMITER //
CREATE PROCEDURE GetProductsByPriceRange(
    IN min_price DECIMAL(10,2),
    IN max_price DECIMAL(10,2)
)
BEGIN
    SELECT * FROM Products
    WHERE price BETWEEN min_price AND max_price;
END //
DELIMITER ;

-- 4. Get total stock (OUT parameter)
DELIMITER //
CREATE PROCEDURE GetTotalStock(OUT total INT)
BEGIN
    SELECT SUM(stock) INTO total FROM Products;
END //
DELIMITER ;

-- Call: CALL GetTotalStock(@total); SELECT @total;

-- 5. Update stock
DELIMITER //
CREATE PROCEDURE UpdateStock(IN prod_id INT, IN quantity INT)
BEGIN
    UPDATE Products
    SET stock = stock + quantity
    WHERE product_id = prod_id;
    SELECT 'Stock updated!' AS message;
END //
DELIMITER ;

-- 6. Check stock status
DELIMITER //
CREATE PROCEDURE CheckStockStatus(IN prod_id INT)
BEGIN
    DECLARE product_stock INT;
    
    SELECT stock INTO product_stock
    FROM Products
    WHERE product_id = prod_id;
    
    IF product_stock > 0 THEN
        SELECT 'In Stock' AS status;
    ELSE
        SELECT 'Out of Stock' AS status;
    END IF;
END //
DELIMITER ;

-- 7. Add new product
DELIMITER //
CREATE PROCEDURE AddNewProduct(
    IN prod_name VARCHAR(100),
    IN prod_price DECIMAL(10,2),
    IN prod_stock INT
)
BEGIN
    INSERT INTO Products (product_name, price, stock)
    VALUES (prod_name, prod_price, prod_stock);
    SELECT 'Product added!' AS message;
END //
DELIMITER ;
```

---

## Quick Recap

- **Stored Procedure:** Saved SQL program you can run multiple times
- **CREATE PROCEDURE:** Create a new procedure
- **CALL:** Execute a procedure
- **IN parameters:** Pass values into procedure
- **OUT parameters:** Return values from procedure
- **INOUT parameters:** Pass in and get modified back
- **DECLARE:** Create local variables
- **SET:** Assign values to variables
- **IF-ELSE:** Conditional logic
- **CASE:** Alternative conditional logic
- **WHILE:** Loop while condition is true
- **REPEAT:** Loop until condition is true
- **HANDLER:** Handle errors gracefully
- **DROP PROCEDURE:** Delete a procedure
- Use `DELIMITER` to change statement separator

## What's Next?

In **Lesson 13: User-Defined Functions**, you'll learn:
- What functions are (vs procedures)
- Creating scalar functions
- Creating table-valued functions
- Function parameters and return types
- Built-in functions review

**Continue to [Lesson 13: User-Defined Functions](13-user-defined-functions.md)**

---

**Your turn:** Try the exercises above. Stored procedures are powerful for encapsulating business logic! 💛
