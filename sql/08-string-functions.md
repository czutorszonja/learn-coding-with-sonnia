# SQL Lesson 8: String Functions — Working with Text

**← Back to [Lesson 7: Set Operations](07-set-operations.md)**

---

## What You'll Learn

In this lesson, you'll master:
- Concatenating strings
- Changing case (upper/lower)
- Extracting substrings
- Finding string length
- Trimming whitespace
- Replacing text
- Finding position of text
- Left and right functions

---

## Setting Up Example Table

**Employees table:**
```
| employee_id | first_name | last_name | email                    | phone      |
|-------------|------------|-----------|--------------------------|------------|
| 1           | Szonja     | Smith     | szonja.smith@email.com   | 555-1234   |
| 2           | Arthur     | Johnson   | arthur.johnson@email.com | 555-5678   |
| 3           | Maria      | Williams  | maria.williams@email.com | 555-9012   |
| 4           | David      | Brown     | david.brown@email.com    | 555-3456   |
```

---

## CONCAT — Join Strings Together

`CONCAT()` combines two or more strings into one.

### Basic CONCAT

```sql
SELECT CONCAT(first_name, ' ', last_name) AS full_name
FROM Employees;
```

**Result:**
```
| full_name         |
|-------------------|
| Szonja Smith      |
| Arthur Johnson    |
| Maria Williams    |
| David Brown       |
```

**How it works:**
- First argument: `first_name`
- Second argument: `' '` (a space)
- Third argument: `last_name`
- All joined together in order

### CONCAT with Multiple Columns

```sql
SELECT CONCAT(first_name, ' ', last_name, ' - ', email) AS contact_info
FROM Employees;
```

**Result:**
```
| contact_info                          |
|---------------------------------------|
| Szonja Smith - szonja.smith@email.com |
| Arthur Johnson - arthur.johnson@email.com |
| Maria Williams - maria.williams@email.com |
| David Brown - david.brown@email.com   |
```

### CONCAT with Different Data Types

SQL automatically converts numbers to strings:

```sql
SELECT CONCAT(employee_id, ': ', first_name) AS id_and_name
FROM Employees;
```

**Result:**
```
| id_and_name      |
|------------------|
| 1: Szonja        |
| 2: Arthur        |
| 3: Maria         |
| 4: David         |
```

### CONCAT Alternative: || Operator

Some databases (PostgreSQL, SQLite, Oracle) support the `||` operator:

```sql
SELECT first_name || ' ' || last_name AS full_name
FROM Employees;
```

**Result:** Same as CONCAT!

**Tip:** `CONCAT()` is more universally supported across different SQL databases.

---

## UPPER and LOWER — Change Case

### UPPER — Convert to Uppercase

```sql
SELECT UPPER(first_name) AS upper_name
FROM Employees;
```

**Result:**
```
| upper_name |
|------------|
| SZONJA     |
| ARTHUR     |
| MARIA      |
| DAVID      |
```

### LOWER — Convert to Lowercase

```sql
SELECT LOWER(email) AS lower_email
FROM Employees;
```

**Result:**
```
| lower_email                  |
|------------------------------|
| szonja.smith@email.com       |
| arthur.johnson@email.com     |
| maria.williams@email.com     |
| david.brown@email.com        |
```

### Practical Use: Case-Insensitive Comparison

```sql
SELECT * FROM Employees
WHERE LOWER(first_name) = 'szonja';
```

**Result:**
```
| employee_id | first_name | last_name | email                  | phone      |
|-------------|------------|-----------|------------------------|------------|
| 1           | Szonja     | Smith     | szonja.smith@email.com | 555-1234   |
```

**Why this matters:** The `LOWER()` converts `first_name` to lowercase for comparison, so it matches `'szonja'` even though the stored value is `'Szonja'`. The result shows the **original** value (`Szonja`), not the lowercased version.

**To return the lowercased value:**
```sql
SELECT LOWER(first_name) AS first_name FROM Employees
WHERE LOWER(first_name) = 'szonja';
```

**Result:**
```
| first_name |
|------------|
| szonja     |
```

---

## LENGTH — Count Characters

`LENGTH()` (or `LEN()` in SQL Server) returns the number of characters in a string.

```sql
SELECT first_name, LENGTH(first_name) AS name_length
FROM Employees;
```

**Result:**
```
| first_name | name_length |
|------------|-------------|
| Szonja     | 6           |
| Arthur     | 6           |
| Maria      | 5           |
| David      | 5           |
```

### Practical Use: Find Long Names

```sql
SELECT first_name, last_name
FROM Employees
WHERE LENGTH(last_name) > 6;
```

**Result:**
```
| first_name | last_name |
|------------|-----------|
| Arthur     | Johnson   |
| Maria      | Williams  |
```

**Explanation:**
- Smith: 5 characters (not > 6)
- Johnson: 7 characters (> 6) ✓
- Williams: 8 characters (> 6) ✓
- Brown: 5 characters (not > 6)

---

## SUBSTRING — Extract Part of a String

`SUBSTRING()` extracts a portion of a string.

### Basic SUBSTRING

```sql
SELECT email, SUBSTRING(email, 1, 6) AS first_part
FROM Employees;
```

**Result:**
```
| email                    | first_part |
|--------------------------|------------|
| szonja.smith@email.com   | szonja     |
| arthur.johnson@email.com | arthur     |
| maria.williams@email.com | maria.     |
| david.brown@email.com    | david.     |
```

**Note:** "maria" and "david" are only 5 characters, so the 6th character (the dot `.`) is included!

**How it works:**
- First argument: the string
- Second argument: starting position (1-based!)
- Third argument: number of characters to extract

### SUBSTRING to End of String

Omit the length to get everything from the start position to the end:

```sql
SELECT email, SUBSTRING(email, 7) AS rest_of_email
FROM Employees;
```

**Result:**
```
| email                    | rest_of_email    |
|--------------------------|------------------|
| szonja.smith@email.com   | .smith@email.com |
| arthur.johnson@email.com | .johnson@email.com |
| maria.williams@email.com | .williams@email.com |
| david.brown@email.com    | .brown@email.com |
```

### Practical Use: Extract Domain from Email

```sql
SELECT email, 
       SUBSTRING(email, POSITION('@' IN email) + 1) AS domain
FROM Employees;
```

**Result:**
```
| email                    | domain       |
|--------------------------|--------------|
| szonja.smith@email.com   | email.com    |
| arthur.johnson@email.com | email.com    |
| maria.williams@email.com | email.com    |
| david.brown@email.com    | email.com    |
```

---

## POSITION — Find Where Text Appears

`POSITION()` finds the position of a substring within a string.

```sql
SELECT email, POSITION('@' IN email) AS at_symbol_position
FROM Employees;
```

**Result:**
```
| email                    | at_symbol_position |
|--------------------------|-------------------|
| szonja.smith@email.com   | 12                |
| arthur.johnson@email.com | 14                |
| maria.williams@email.com | 15                |
| david.brown@email.com    | 11                |
```

**Meaning:** In Szonja's email, the `@` symbol is at position 12.

### Alternative: STRPOS (PostgreSQL)

Some databases use `STRPOS()` instead:

```sql
SELECT STRPOS(email, '@') AS at_symbol_position
FROM Employees;
```

Same result!

---

## TRIM — Remove Whitespace

`TRIM()` removes leading and trailing whitespace.

### Basic TRIM

```sql
SELECT TRIM('   Hello World   ') AS trimmed;
```

**Result:**
```
| trimmed     |
|-------------|
| Hello World |
```

### LTRIM and RTRIM

- `LTRIM()` — remove leading (left) whitespace only
- `RTRIM()` — remove trailing (right) whitespace only

```sql
SELECT 
    LTRIM('   Hello World   ') AS left_trimmed,
    RTRIM('   Hello World   ') AS right_trimmed,
    TRIM('   Hello World   ') AS both_trimmed;
```

**Result:**
```
| left_trimmed   | right_trimmed  | both_trimmed   |
|----------------|----------------|----------------|
| Hello World    |    Hello World | Hello World    |
```

### Practical Use: Clean User Input

```sql
SELECT first_name, TRIM(first_name) AS clean_name
FROM Employees;
```

**Why this matters:** Users might accidentally add spaces when entering data. `TRIM()` cleans it up!

---

## REPLACE — Substitute Text

`REPLACE()` finds and replaces all occurrences of a substring.

### Basic REPLACE

```sql
SELECT email, REPLACE(email, 'email.com', 'company.com') AS new_email
FROM Employees;
```

**Result:**
```
| email                    | new_email                     |
|--------------------------|-------------------------------|
| szonja.smith@email.com   | szonja.smith@company.com      |
| arthur.johnson@email.com | arthur.johnson@company.com    |
| maria.williams@email.com | maria.williams@company.com    |
| david.brown@email.com    | david.brown@company.com       |
```

### REPLACE to Remove Characters

Replace with empty string to remove characters:

```sql
SELECT phone, REPLACE(phone, '-', '') AS phone_no_dashes
FROM Employees;
```

**Result:**
```
| phone      | phone_no_dashes |
|------------|-----------------|
| 555-1234   | 5551234         |
| 555-5678   | 5555678         |
| 555-9012   | 5559012         |
| 555-3456   | 5553456         |
```

---

## LEFT and RIGHT — Extract from Ends

### LEFT — Get First N Characters

```sql
SELECT first_name, LEFT(first_name, 3) AS first_three
FROM Employees;
```

**Result:**
```
| first_name | first_three |
|------------|-------------|
| Szonja     | Szo         |
| Arthur     | Art         |
| Maria      | Mar         |
| David      | Dav         |
```

### RIGHT — Get Last N Characters

```sql
SELECT email, RIGHT(email, 4) AS extension
FROM Employees;
```

**Result:**
```
| email                    | extension |
|--------------------------|-----------|
| szonja.smith@email.com   | .com      |
| arthur.johnson@email.com | .com      |
| maria.williams@email.com | .com      |
| david.brown@email.com    | .com      |
```

---

## Combining String Functions

You can nest string functions together!

### Example: Create Username from Email

```sql
SELECT email,
       LOWER(SUBSTRING(email, 1, POSITION('@' IN email) - 1)) AS username
FROM Employees;
```

**Result:**
```
| email                    | username      |
|--------------------------|---------------|
| szonja.smith@email.com   | szonja.smith  |
| arthur.johnson@email.com | arthur.johnson|
| maria.williams@email.com | maria.williams|
| david.brown@email.com    | david.brown   |
```

**How it works:**
1. `POSITION('@' IN email)` finds where `@` is
2. Subtract 1 to get the position before `@`
3. `SUBSTRING(email, 1, ...)` extracts from start to that position
4. `LOWER()` converts to lowercase

---

## Practice Exercise

**Scenario:** You have a `Products` table:

**Products table:**
```
| product_id | product_name        | price |
|------------|---------------------|-------|
| 1          | Laptop Pro          | 999   |
| 2          | Wireless Mouse      | 25    |
| 3          | USB-C Cable         | 15    |
| 4          | 4K Monitor          | 300   |
| 5          | Mechanical Keyboard | 75    |
```

**Copy-paste values (AUTO_INCREMENT):**
```sql
('Laptop Pro', 999),
('Wireless Mouse', 25),
('USB-C Cable', 15),
('4K Monitor', 300),
('Mechanical Keyboard', 75);
```

**Your tasks:**

1. Get product names in UPPERCASE
2. Get product names in lowercase
3. Extract the first 5 characters of each product name
4. Find the position of the letter "o" in each product name
5. Replace all spaces in product names with hyphens
6. Get the length of each product name
7. Create a SKU by combining first 3 letters of product name with price (e.g., "Lap999")
8. Extract everything after the first space in the product name

**Try it yourself first!** Then scroll down to check your answers.

---

## Solutions

```sql
-- 1. Product names in UPPERCASE
SELECT UPPER(product_name) AS upper_name FROM Products;

-- 2. Product names in lowercase
SELECT LOWER(product_name) AS lower_name FROM Products;

-- 3. First 5 characters
SELECT product_name, LEFT(product_name, 5) AS first_five FROM Products;

-- 4. Position of letter "o"
SELECT product_name, POSITION('o' IN product_name) AS o_position FROM Products;

-- 5. Replace spaces with hyphens
SELECT product_name, REPLACE(product_name, ' ', '-') AS sku_friendly FROM Products;

-- 6. Length of product name
SELECT product_name, LENGTH(product_name) AS name_length FROM Products;

-- 7. Create SKU (first 3 letters + price)
SELECT CONCAT(LEFT(product_name, 3), price) AS sku FROM Products;

-- 8. Everything after first space
SELECT product_name, 
       SUBSTRING(product_name, POSITION(' ' IN product_name) + 1) AS after_space
FROM Products;
```

---

## Quick Recap

- **CONCAT():** Join strings together
- **UPPER():** Convert to uppercase
- **LOWER():** Convert to lowercase
- **LENGTH():** Count characters
- **SUBSTRING():** Extract part of a string
- **POSITION():** Find where text appears
- **TRIM():** Remove leading/trailing whitespace
- **LTRIM()/RTRIM():** Remove left or right whitespace only
- **REPLACE():** Find and replace text
- **LEFT()/RIGHT():** Extract from beginning or end
- Can combine multiple string functions together
- String positions are 1-based (not 0-based!)

## What's Next?

In **Lesson 9: Date/Time Functions**, you'll learn:
- Getting current date and time
- Extracting parts of dates
- Formatting dates
- Adding and subtracting time
- Calculating differences between dates

**Continue to [Lesson 9: Date/Time Functions](09-date-time-functions.md)**

---

**Your turn:** Try the exercises above. String functions are essential for cleaning and formatting text data! 💛
