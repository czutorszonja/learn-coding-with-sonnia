# SQL Lesson 10: Mathematical Functions — Working with Numbers

**← Back to [Lesson 9: Date/Time Functions](09-date-time-functions.md)**

---

## What You'll Learn

In this lesson, you'll master:
- Basic arithmetic operations
- Rounding numbers (ROUND, CEILING, FLOOR)
- Absolute values
- Power and square root
- Modulo operations
- Random numbers
- Sign functions

---

## Setting Up Example Table

```sql
CREATE TABLE Products (
    product_id INT,
    product_name VARCHAR(100),
    price DECIMAL(10,2),
    cost DECIMAL(10,2),
    stock_quantity INT
);

INSERT INTO Products (product_id, product_name, price, cost, stock_quantity) VALUES
    (1, 'Laptop', 999.99, 750.00, 15),
    (2, 'Mouse', 25.50, 12.00, 50),
    (3, 'Keyboard', 75.00, 45.00, 30),
    (4, 'Monitor', 299.99, 200.00, 20),
    (5, 'Headphones', 149.99, 80.00, 25);
```

---

## Basic Arithmetic Operations

SQL supports standard math operators: `+`, `-`, `*`, `/`

### Addition

```sql
SELECT product_name, price, cost, (price + cost) AS total
FROM Products;
```

**Result:**
```
| product_name | price  | cost   | total   |
|--------------|--------|--------|---------|
| Laptop       | 999.99 | 750.00 | 1749.99 |
| Mouse        | 25.50  | 12.00  | 37.50   |
| Keyboard     | 75.00  | 45.00  | 120.00  |
| Monitor      | 299.99 | 200.00 | 499.99  |
| Headphones   | 149.99 | 80.00  | 229.99  |
```

### Subtraction (Calculate Profit)

```sql
SELECT product_name, price, cost, (price - cost) AS profit
FROM Products;
```

**Result:**
```
| product_name | price  | cost   | profit  |
|--------------|--------|--------|---------|
| Laptop       | 999.99 | 750.00 | 249.99  |
| Mouse        | 25.50  | 12.00  | 13.50   |
| Keyboard     | 75.00  | 45.00  | 30.00   |
| Monitor      | 299.99 | 200.00 | 99.99   |
| Headphones   | 149.99 | 80.00  | 69.99   |
```

### Multiplication (Calculate Total Value)

```sql
SELECT product_name, price, stock_quantity, (price * stock_quantity) AS total_value
FROM Products;
```

**Result:**
```
| product_name | price  | stock_quantity | total_value |
|--------------|--------|----------------|-------------|
| Laptop       | 999.99 | 15             | 14999.85    |
| Mouse        | 25.50  | 50             | 1275.00     |
| Keyboard     | 75.00  | 30             | 2250.00     |
| Monitor      | 299.99 | 20             | 5999.80     |
| Headphones   | 149.99 | 25             | 3749.75     |
```

### Division (Calculate Profit Margin)

```sql
SELECT product_name, price, cost, 
       ((price - cost) / price * 100) AS profit_margin_percent
FROM Products;
```

**Result:**
```
| product_name | price  | cost   | profit_margin_percent |
|--------------|--------|--------|-----------------------|
| Laptop       | 999.99 | 750.00 | 25.00                 |
| Mouse        | 25.50  | 12.00  | 52.94                 |
| Keyboard     | 75.00  | 45.00  | 40.00                 |
| Monitor      | 299.99 | 200.00 | 33.33                 |
| Headphones   | 149.99 | 80.00  | 46.67                 |
```

**Tip:** Use parentheses to control order of operations!

---

## ROUND — Round Numbers

`ROUND()` rounds a number to a specified number of decimal places.

### Round to 2 Decimal Places

```sql
SELECT product_name, price, ROUND(price, 2) AS rounded_price
FROM Products;
```

**Result:**
```
| product_name | price  | rounded_price |
|--------------|--------|---------------|
| Laptop       | 999.99 | 999.99        |
| Mouse        | 25.50  | 25.50         |
| Keyboard     | 75.00  | 75.00         |
| Monitor      | 299.99 | 299.99        |
| Headphones   | 149.99 | 149.99        |
```

### Round to Whole Number

```sql
SELECT product_name, price, ROUND(price, 0) AS rounded_price
FROM Products;
```

**Result:**
```
| product_name | price  | rounded_price |
|--------------|--------|---------------|
| Laptop       | 999.99 | 1000          |
| Mouse        | 25.50  | 26            |
| Keyboard     | 75.00  | 75            |
| Monitor      | 299.99 | 300           |
| Headphones   | 149.99 | 150           |
```

### Round Negative (Round to Tens, Hundreds)

```sql
SELECT product_name, price, ROUND(price, -2) AS rounded_to_hundreds
FROM Products;
```

**Result:**
```
| product_name | price  | rounded_to_hundreds |
|--------------|--------|---------------------|
| Laptop       | 999.99 | 1000                |
| Mouse        | 25.50  | 0                   |
| Keyboard     | 75.00  | 100                 |
| Monitor      | 299.99 | 300                 |
| Headphones   | 149.99 | 100                 |
```

**How it works:** Negative precision rounds to the left of the decimal point.

---

## CEILING and FLOOR — Round Up or Down

### CEILING — Round Up

`CEILING()` (or `CEIL()`) rounds a number UP to the nearest integer.

```sql
SELECT product_name, price, CEILING(price) AS rounded_up
FROM Products;
```

**Result:**
```
| product_name | price  | rounded_up |
|--------------|--------|------------|
| Laptop       | 999.99 | 1000       |
| Mouse        | 25.50  | 26         |
| Keyboard     | 75.00  | 75         |
| Monitor      | 299.99 | 300        |
| Headphones   | 149.99 | 150        |
```

### FLOOR — Round Down

`FLOOR()` rounds a number DOWN to the nearest integer.

```sql
SELECT product_name, price, FLOOR(price) AS rounded_down
FROM Products;
```

**Result:**
```
| product_name | price  | rounded_down |
|--------------|--------|--------------|
| Laptop       | 999.99 | 999          |
| Mouse        | 25.50  | 25           |
| Keyboard     | 75.00  | 75           |
| Monitor      | 299.99 | 299          |
| Headphones   | 149.99 | 149          |
```

### Practical Use: Calculate Minimum Units Needed

```sql
SELECT product_name, stock_quantity,
       CEILING(stock_quantity / 10.0) AS boxes_needed
FROM Products;
```

**Result:**
```
| product_name | stock_quantity | boxes_needed |
|--------------|----------------|--------------|
| Laptop       | 15             | 2            |
| Mouse        | 50             | 5            |
| Keyboard     | 30             | 3            |
| Monitor      | 20             | 2            |
| Headphones   | 25             | 3            |
```

**Why 10.0?** Dividing by `10.0` (not `10`) ensures decimal division.

---

## ABS — Absolute Value

`ABS()` returns the absolute value (distance from zero, always positive).

```sql
SELECT ABS(-5) AS positive_five, ABS(5) AS also_five;
```

**Result:**
```
| positive_five | also_five |
|---------------|-----------|
| 5             | 5         |
```

### Practical Use: Calculate Difference Regardless of Direction

```sql
SELECT product_name, price, cost,
       ABS(price - cost) AS price_difference
FROM Products;
```

**Result:**
```
| product_name | price  | cost   | price_difference |
|--------------|--------|--------|------------------|
| Laptop       | 999.99 | 750.00 | 249.99           |
| Mouse        | 25.50  | 12.00  | 13.50            |
| Keyboard     | 75.00  | 45.00  | 30.00            |
| Monitor      | 299.99 | 200.00 | 99.99            |
| Headphones   | 149.99 | 80.00  | 69.99            |
```

---

## POWER and SQRT — Exponents and Square Root

### POWER — Raise to a Power

`POWER()` raises a number to a specified exponent.

```sql
SELECT product_name, price, POWER(price, 2) AS price_squared
FROM Products;
```

**Result:**
```
| product_name | price  | price_squared  |
|--------------|--------|----------------|
| Laptop       | 999.99 | 999980.0001    |
| Mouse        | 25.50  | 650.25         |
| Keyboard     | 75.00  | 5625.00        |
| Monitor      | 299.99 | 89994.0001     |
| Headphones   | 149.99 | 22497.0001     |
```

### SQRT — Square Root

`SQRT()` returns the square root of a number.

```sql
SELECT product_name, stock_quantity, SQRT(stock_quantity) AS sqrt_stock
FROM Products;
```

**Result:**
```
| product_name | stock_quantity | sqrt_stock        |
|--------------|----------------|-------------------|
| Laptop       | 15             | 3.872983346207417 |
| Mouse        | 50             | 7.0710678118654755|
| Keyboard     | 30             | 5.477225575051661 |
| Monitor      | 20             | 4.47213595499958  |
| Headphones   | 25             | 5.0               |
```

---

## MOD — Modulo (Remainder)

`MOD()` (or `%` operator) returns the remainder after division.

### Basic MOD

```sql
SELECT product_name, stock_quantity, MOD(stock_quantity, 10) AS remainder
FROM Products;
```

**Result:**
```
| product_name | stock_quantity | remainder |
|--------------|----------------|-----------|
| Laptop       | 15             | 5         |
| Mouse        | 50             | 0         |
| Keyboard     | 30             | 0         |
| Monitor      | 20             | 0         |
| Headphones   | 25             | 5         |
```

**Meaning:** 
- Laptop: 15 ÷ 10 = 1 remainder 5
- Mouse: 50 ÷ 10 = 5 remainder 0
- etc.

### Practical Use: Find Every Nth Row

```sql
SELECT product_id, product_name, stock_quantity
FROM Products
WHERE MOD(product_id, 2) = 0;
```

**Result:** Returns products with even IDs (2, 4).

### Alternative: % Operator

```sql
SELECT product_name, stock_quantity, stock_quantity % 10 AS remainder
FROM Products;
```

Same result!

---

## RANDOM — Generate Random Numbers

`RANDOM()` generates a random number between 0 and 1.

### Basic Random

```sql
SELECT RANDOM() AS random_number;
```

**Result:**
```
| random_number      |
|--------------------|
| 0.7834521          |
```

### Random Integer in Range

```sql
SELECT product_name, FLOOR(RANDOM() * 100) AS random_stock
FROM Products;
```

**Result:**
```
| product_name | random_stock |
|--------------|--------------|
| Laptop       | 47           |
| Mouse        | 23           |
| Keyboard     | 89           |
| Monitor      | 12           |
| Headphones   | 65           |
```

**How it works:**
1. `RANDOM()` gives 0.0 to 1.0
2. Multiply by 100: 0 to 100
3. `FLOOR()` rounds down to integer

---

## SIGN — Get the Sign of a Number

`SIGN()` returns -1, 0, or 1 depending on whether the number is negative, zero, or positive.

```sql
SELECT 
    SIGN(-5) AS negative,
    SIGN(0) AS zero,
    SIGN(5) AS positive;
```

**Result:**
```
| negative | zero | positive |
|----------|------|----------|
| -1       | 0    | 1        |
```

---

## Combining Mathematical Functions

You can chain multiple functions together!

### Example: Calculate Profit with Tax

```sql
SELECT 
    product_name,
    price,
    cost,
    (price - cost) AS profit,
    ROUND((price - cost) * 0.2, 2) AS tax_20_percent,
    ROUND((price - cost) - ((price - cost) * 0.2), 2) AS profit_after_tax
FROM Products;
```

**Result:**
```
| product_name | price  | cost   | profit  | tax_20_percent | profit_after_tax |
|--------------|--------|--------|---------|----------------|------------------|
| Laptop       | 999.99 | 750.00 | 249.99  | 50.00          | 199.99           |
| Mouse        | 25.50  | 12.00  | 13.50   | 2.70           | 10.80            |
| Keyboard     | 75.00  | 45.00  | 30.00   | 6.00           | 24.00            |
| Monitor      | 299.99 | 200.00 | 99.99   | 20.00          | 79.99            |
| Headphones   | 149.99 | 80.00  | 69.99   | 14.00          | 55.99            |
```

---

## Practice Exercise

**Scenario:** You have a `Sales` table:

**Copy-paste values (AUTO_INCREMENT):**
```sql
('Laptop', 2, 999.99, 10),
('Mouse', 5, 25.50, 5),
('Keyboard', 3, 75.00, 15),
('Monitor', 1, 299.99, 0),
('Headphones', 4, 149.99, 20);
```

**Your tasks:**

1. Calculate the subtotal for each sale (quantity × unit_price)
2. Calculate the discount amount (subtotal × discount_percent / 100)
3. Calculate the final total (subtotal - discount amount)
4. Round the final total to 2 decimal places
5. Find the absolute difference between unit_price and discounted price per unit
6. Generate a random number between 1 and 100 for each sale
7. Find the square root of the quantity
8. Check if the discount_percent is positive using SIGN()

**Try it yourself first!** Then scroll down to check your answers.

---

## Solutions

```sql
-- 1. Calculate subtotal
SELECT product_name, quantity, unit_price, 
       (quantity * unit_price) AS subtotal
FROM Sales;

-- 2. Calculate discount amount
SELECT product_name, 
       (quantity * unit_price) AS subtotal,
       (quantity * unit_price * discount_percent / 100) AS discount_amount
FROM Sales;

-- 3 & 4. Calculate final total (rounded)
SELECT product_name,
       (quantity * unit_price) AS subtotal,
       (quantity * unit_price * discount_percent / 100) AS discount_amount,
       ROUND((quantity * unit_price) - (quantity * unit_price * discount_percent / 100), 2) AS final_total
FROM Sales;

-- 5. Absolute difference between unit_price and discounted price
SELECT product_name,
       unit_price,
       (unit_price * (1 - discount_percent / 100)) AS discounted_price,
       ABS(unit_price - (unit_price * (1 - discount_percent / 100))) AS price_difference
FROM Sales;

-- 6. Random number between 1 and 100
SELECT product_name, FLOOR(RANDOM() * 100) + 1 AS random_number FROM Sales;

-- 7. Square root of quantity
SELECT product_name, quantity, SQRT(quantity) AS sqrt_quantity FROM Sales;

-- 8. Check if discount is positive
SELECT product_name, discount_percent, SIGN(discount_percent) AS is_positive FROM Sales;
```

---

## Quick Recap

- **+ - * /** : Basic arithmetic operations
- **ROUND():** Round to specified decimal places
- **CEILING()/CEIL():** Round up
- **FLOOR():** Round down
- **ABS():** Absolute value (always positive)
- **POWER():** Raise to a power
- **SQRT():** Square root
- **MOD() or %:** Modulo (remainder)
- **RANDOM():** Generate random numbers
- **SIGN():** Get sign of number (-1, 0, or 1)
- Use parentheses to control order of operations
- Can combine multiple functions together

## What's Next?

In **Lesson 11: CASE Statements**, you'll learn:
- What CASE statements are
- Simple CASE expressions
- Searched CASE expressions
- CASE with WHERE and ORDER BY
- Practical use cases

**Continue to [Lesson 11: CASE Statements](11-case-statements.md)**

---

**Your turn:** Try the exercises above. Math functions are powerful for calculations and data analysis! 💛
