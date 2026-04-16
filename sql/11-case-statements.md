# SQL Lesson 11: CASE Statements — Conditional Logic

**← Back to [Lesson 10: Mathematical Functions](10-mathematical-functions.md)**

---

## What You'll Learn

In this lesson, you'll master:
- What CASE statements are
- Simple CASE expressions
- Searched CASE expressions
- CASE with WHERE and ORDER BY
- NULL handling in CASE
- Practical use cases

---

## What is a CASE Statement?

**Plain English:** A CASE statement is like an IF-THEN-ELSE statement in programming. It lets you apply conditional logic in your SQL queries.

**Real-world analogy:** Imagine a vending machine:
- IF you press A1 → you get chips
- IF you press B2 → you get soda
- IF you press C3 → you get candy
- ELSE → return your money

A CASE statement works the same way — it checks conditions and returns different values based on what's true.

---

## Setting Up Example Table

```sql
CREATE TABLE Employees (
    employee_id INT,
    name VARCHAR(100),
    department VARCHAR(100),
    salary DECIMAL(10,2),
    years_employed INT
);

INSERT INTO Employees (employee_id, name, department, salary, years_employed) VALUES
    (1, 'Szonja', 'Engineering', 95000, 5),
    (2, 'Arthur', 'Engineering', 85000, 3),
    (3, 'Maria', 'Sales', 70000, 2),
    (4, 'David', 'Sales', 60000, 1),
    (5, 'Emma', 'HR', 75000, 4),
    (6, 'Liam', 'Engineering', 90000, 6);
```

---

## Simple CASE Expression

A simple CASE checks one column against multiple values.

### Basic Syntax

```sql
CASE column_name
    WHEN value1 THEN result1
    WHEN value2 THEN result2
    ELSE default_result
END
```

### Example: Department Nicknames

```sql
SELECT 
    name,
    department,
    CASE department
        WHEN 'Engineering' THEN 'Tech Team'
        WHEN 'Sales' THEN 'Revenue Team'
        WHEN 'HR' THEN 'People Team'
        ELSE 'Other'
    END AS team_name
FROM Employees;
```

**Result:**
```
| name   | department  | team_name    |
|--------|-------------|--------------|
| Szonja | Engineering | Tech Team    |
| Arthur | Engineering | Tech Team    |
| Maria  | Sales       | Revenue Team |
| David  | Sales       | Revenue Team |
| Emma   | HR          | People Team  |
| Liam   | Engineering | Tech Team    |
```

**How it works:**
1. SQL checks the `department` column
2. If it matches 'Engineering', return 'Tech Team'
3. If it matches 'Sales', return 'Revenue Team'
4. If it matches 'HR', return 'People Team'
5. If nothing matches, return 'Other'

---

## Searched CASE Expression

A searched CASE uses full conditions (not just equality checks).

### Basic Syntax

```sql
CASE
    WHEN condition1 THEN result1
    WHEN condition2 THEN result2
    ELSE default_result
END
```

### Example: Salary Categories

```sql
SELECT 
    name,
    salary,
    CASE
        WHEN salary >= 90000 THEN 'Senior'
        WHEN salary >= 70000 THEN 'Mid-level'
        WHEN salary >= 50000 THEN 'Junior'
        ELSE 'Entry-level'
    END AS level
FROM Employees;
```

**Result:**
```
| name   | salary | level     |
|--------|--------|-----------|
| Szonja | 95000  | Senior    |
| Arthur | 85000  | Mid-level |
| Maria  | 70000  | Mid-level |
| David  | 60000  | Junior    |
| Emma   | 75000  | Mid-level |
| Liam   | 90000  | Senior    |
```

**Important:** CASE evaluates conditions in order and stops at the first TRUE condition!

### Example: Experience Levels

```sql
SELECT 
    name,
    years_employed,
    CASE
        WHEN years_employed >= 5 THEN '5+ years'
        WHEN years_employed >= 3 THEN '3-4 years'
        WHEN years_employed >= 1 THEN '1-2 years'
        ELSE 'Less than 1 year'
    END AS experience
FROM Employees;
```

**Result:**
```
| name   | years_employed | experience     |
|--------|----------------|----------------|
| Szonja | 5              | 5+ years       |
| Arthur | 3              | 3-4 years      |
| Maria  | 2              | 1-2 years      |
| David  | 1              | 1-2 years      |
| Emma   | 4              | 3-4 years      |
| Liam   | 6              | 5+ years       |
```

---

## CASE with Multiple Conditions

You can use AND, OR, NOT in CASE conditions.

### Example: Bonus Eligibility

```sql
SELECT 
    name,
    department,
    years_employed,
    CASE
        WHEN years_employed >= 5 AND department = 'Engineering' THEN 'Eligible for 20% bonus'
        WHEN years_employed >= 3 AND department = 'Engineering' THEN 'Eligible for 15% bonus'
        WHEN years_employed >= 3 THEN 'Eligible for 10% bonus'
        ELSE 'Not eligible yet'
    END AS bonus_status
FROM Employees;
```

**Result:**
```
| name   | department  | years_employed | bonus_status              |
|--------|-------------|----------------|---------------------------|
| Szonja | Engineering | 5              | Eligible for 20% bonus    |
| Arthur | Engineering | 3              | Eligible for 15% bonus    |
| Maria  | Sales       | 2              | Not eligible yet          |
| David  | Sales       | 1              | Not eligible yet          |
| Emma   | HR          | 4              | Eligible for 10% bonus    |
| Liam   | Engineering | 6              | Eligible for 20% bonus    |
```

---

## CASE in WHERE Clause

You can use CASE to filter results dynamically.

### Example: Filter by Senior Employees Only

```sql
SELECT name, department, salary
FROM Employees
WHERE CASE
    WHEN salary >= 90000 THEN 1
    ELSE 0
END = 1;
```

**Result:**
```
| name   | department  | salary |
|--------|-------------|--------|
| Szonja | Engineering | 95000  |
| Liam   | Engineering | 90000  |
```

**How it works:**
- CASE returns 1 for salaries >= 90000, 0 otherwise
- WHERE keeps only rows where CASE returns 1

### Better Alternative (Direct Condition)

```sql
SELECT name, department, salary
FROM Employees
WHERE salary >= 90000;
```

Same result, cleaner! Use CASE in WHERE only when you need complex logic.

---

## CASE in ORDER BY

You can sort results based on custom logic.

### Example: Sort by Department Priority

```sql
SELECT name, department, salary
FROM Employees
ORDER BY CASE department
    WHEN 'Engineering' THEN 1
    WHEN 'HR' THEN 2
    WHEN 'Sales' THEN 3
    ELSE 4
END;
```

**Result:**
```
| name   | department  | salary |
|--------|-------------|--------|
| Szonja | Engineering | 95000  |
| Arthur | Engineering | 85000  |
| Liam   | Engineering | 90000  |
| Emma   | HR          | 75000  |
| Maria  | Sales       | 70000  |
| David  | Sales       | 60000  |
```

**How it works:**
- Engineering gets priority 1 (sorted first)
- HR gets priority 2
- Sales gets priority 3
- Others get priority 4

### Example: Sort Senior Employees First

```sql
SELECT name, years_employed, salary
FROM Employees
ORDER BY CASE
    WHEN years_employed >= 5 THEN 1
    ELSE 2
END, years_employed DESC;
```

**Result:**
```
| name   | years_employed | salary |
|--------|----------------|--------|
| Liam   | 6              | 90000  |
| Szonja | 5              | 95000  |
| Emma   | 4              | 75000  |
| Arthur | 3              | 85000  |
| Maria  | 2              | 70000  |
| David  | 1              | 60000  |
```

---

## NULL Handling in CASE

NULL values need special handling because NULL = NULL is FALSE in SQL.

### Example: Handle NULL Salaries

```sql
CREATE TABLE Contractors (
    name VARCHAR(100),
    hourly_rate DECIMAL(10,2)
);

INSERT INTO Contractors (name, hourly_rate) VALUES
    ('Szonja', 150.00),
    ('Arthur', 125.00),
    ('Maria', NULL);
```

### Wrong Way (NULL won't match)

```sql
SELECT name, hourly_rate,
       CASE hourly_rate
           WHEN NULL THEN 'Rate not set'
           ELSE 'Rate is set'
       END AS status
FROM Contractors;
```

**Result:**
```
| name   | hourly_rate | status    |
|--------|-------------|-----------|
| Szonja | 150.00      | Rate is set|
| Arthur | 125.00      | Rate is set|
| Maria  | NULL        | Rate is set|  ← Wrong!
```

### Right Way (Use IS NULL)

```sql
SELECT name, hourly_rate,
       CASE
           WHEN hourly_rate IS NULL THEN 'Rate not set'
           ELSE 'Rate is set'
       END AS status
FROM Contractors;
```

**Result:**
```
| name   | hourly_rate | status      |
|--------|-------------|-------------|
| Szonja | 150.00      | Rate is set |
| Arthur | 125.00      | Rate is set |
| Maria  | NULL        | Rate not set|
```

**Key lesson:** Use `IS NULL` or `IS NOT NULL` in searched CASE, not simple CASE!

---

## CASE with Calculations

You can perform calculations inside CASE statements.

### Example: Calculate Bonus Amount

```sql
SELECT 
    name,
    salary,
    years_employed,
    CASE
        WHEN years_employed >= 5 THEN salary * 0.20
        WHEN years_employed >= 3 THEN salary * 0.15
        ELSE salary * 0.10
    END AS bonus_amount
FROM Employees;
```

**Result:**
```
| name   | salary | years_employed | bonus_amount |
|--------|--------|----------------|--------------|
| Szonja | 95000  | 5              | 19000.00     |
| Arthur | 85000  | 3              | 12750.00     |
| Maria  | 70000  | 2              | 7000.00      |
| David  | 60000  | 1              | 6000.00      |
| Emma   | 75000  | 4              | 11250.00     |
| Liam   | 90000  | 6              | 18000.00     |
```

---

## Practical Use Cases

### Use Case 1: Data Categorization

```sql
SELECT 
    name,
    salary,
    CASE
        WHEN salary >= 90000 THEN 'High'
        WHEN salary >= 70000 THEN 'Medium'
        ELSE 'Low'
    END AS salary_category
FROM Employees;
```

### Use Case 2: Status Labels

```sql
SELECT 
    name,
    years_employed,
    CASE
        WHEN years_employed = 0 THEN 'Probation'
        WHEN years_employed BETWEEN 1 AND 2 THEN 'Junior'
        WHEN years_employed BETWEEN 3 AND 5 THEN 'Senior'
        ELSE 'Expert'
    END AS status
FROM Employees;
```

### Use Case 3: Dynamic Sorting

```sql
SELECT name, department, salary
FROM Employees
ORDER BY CASE
    WHEN department = 'Engineering' THEN salary * 1.0
    WHEN department = 'HR' THEN salary * 1.1
    WHEN department = 'Sales' THEN salary * 1.2
    ELSE salary
END DESC;
```

---

## Practice Exercise

**Scenario:** You have a `Students` table:

**Copy-paste values (AUTO_INCREMENT):**
```sql
('Emma Wilson', 'A', 92),
('Liam Brown', 'B', 85),
('Olivia Davis', 'A', 88),
('Noah Martinez', 'C', 72),
('Ava Johnson', 'F', 45);
```

**Your tasks:**

1. Convert letter grades to grade points (A=4, B=3, C=2, D=1, F=0)
2. Categorize students as "Pass" or "Fail" based on their grade (F = Fail)
3. Add a comment based on score: >= 90 "Excellent", >= 80 "Good", >= 70 "Average", else "Needs Improvement"
4. Sort students by grade priority (A first, then B, C, D, F)
5. Calculate whether each student is eligible for honors (score >= 85 AND grade != 'F')

**Try it yourself first!** Then scroll down to check your answers.

---

## Solutions

```sql
-- 1. Convert letter grades to grade points
SELECT name, grade,
       CASE grade
           WHEN 'A' THEN 4
           WHEN 'B' THEN 3
           WHEN 'C' THEN 2
           WHEN 'D' THEN 1
           WHEN 'F' THEN 0
           ELSE NULL
       END AS grade_points
FROM Students;

-- 2. Categorize as Pass or Fail
SELECT name, grade,
       CASE grade
           WHEN 'F' THEN 'Fail'
           ELSE 'Pass'
       END AS status
FROM Students;

-- 3. Add comment based on score
SELECT name, score,
       CASE
           WHEN score >= 90 THEN 'Excellent'
           WHEN score >= 80 THEN 'Good'
           WHEN score >= 70 THEN 'Average'
           ELSE 'Needs Improvement'
       END AS comment
FROM Students;

-- 4. Sort by grade priority
SELECT name, grade
FROM Students
ORDER BY CASE grade
    WHEN 'A' THEN 1
    WHEN 'B' THEN 2
    WHEN 'C' THEN 3
    WHEN 'D' THEN 4
    WHEN 'F' THEN 5
    ELSE 6
END;

-- 5. Check honors eligibility
SELECT name, score, grade,
       CASE
           WHEN score >= 85 AND grade != 'F' THEN 'Eligible'
           ELSE 'Not Eligible'
       END AS honors_status
FROM Students;
```

---

## Quick Recap

- **CASE statement:** Conditional logic in SQL (like IF-THEN-ELSE)
- **Simple CASE:** `CASE column WHEN value THEN result`
- **Searched CASE:** `CASE WHEN condition THEN result`
- CASE evaluates conditions in order, stops at first TRUE
- Can use AND, OR, NOT in CASE conditions
- CASE works in SELECT, WHERE, ORDER BY, HAVING
- Handle NULL with `IS NULL` in searched CASE
- Can perform calculations inside CASE
- Use CASE for categorization, labels, dynamic sorting

## What's Next?

In **Lesson 12: Stored Procedures**, you'll learn:
- What stored procedures are
- Creating and executing procedures
- Parameters (IN, OUT, INOUT)
- Variables in procedures
- Control flow (IF, WHILE, LOOP)

**Continue to [Lesson 12: Stored Procedures](12-stored-procedures.md)**

---

**Your turn:** Try the exercises above. CASE statements are powerful for adding logic to your queries! 💛
