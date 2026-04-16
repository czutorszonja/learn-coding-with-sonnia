# SQL Lesson 1: What is a Database?

**← Back to [SQL Setup Guide](README.md)**

---

## What is a Database?

**Plain English:** A database is like a digital filing cabinet where you store organised information.

**Real-world analogy:** Imagine a library:
- Books are organised by category (fiction, science, history)
- Each book has a title, author, ISBN, and location
- You can search for books by title, author, or topic
- The librarian helps you find exactly what you need

A database works the same way — it stores data in organised tables, and you can ask it questions.

## What is SQL?

**SQL** = Structured Query Language

**Plain English:** SQL is the language you use to talk to a database.

**Real-world analogy:** If the database is the librarian, SQL is the words you use to ask for books.

## Creating a Database

Before you can store anything, you need to create a database.

```sql
CREATE DATABASE my_first_db;
```

**What this means:**
- `CREATE DATABASE` = "make a new database"
- `my_first_db` = the name you're giving it (you choose!)

**Tip:** Database naming varies by convention:
- Some use `lowercase_with_underscores` (my_first_db)
- Some use `PascalCase` (FoodOrdering, Customers)
- Both work! Follow your team's or class's convention.

## Using a Database

Once you have a database, you need to tell SQL which one to work with.

```sql
USE my_first_db;
```

**What this means:**
- `USE` = "switch to this database"
- `my_first_db` = the database name

Think of it like opening the right filing cabinet before you start working.

## Creating a Table

Now let's make a table to store data:

```sql
CREATE TABLE users (
    id INT,
    name VARCHAR(100),
    email VARCHAR(100),
    age INT
);
```

**What this means:**
- `CREATE TABLE` = "make a new table"
- `users` = the table name
- Inside the parentheses: the columns and their types
  - `INT` = whole numbers (like 1, 2, 3)
  - `VARCHAR(100)` = text up to 100 characters

## Adding Data with INSERT

Now that you have a table, let's add some data!

```sql
INSERT INTO users (id, name, email, age) VALUES (1, 'Szonja', 'szonja@email.com', 30);
```

**What this means:**
- `INSERT INTO` = "add data to"
- `users` = the table name
- `(id, name, email, age)` = which columns we're filling
- `VALUES` = "here's the data"
- `(1, 'Szonja', 'szonja@email.com', 30)` = the actual values

**Important:** Text values need quotes (`'`), numbers don't.

### Adding Multiple Rows at Once

You can add several rows in one go:

```sql
INSERT INTO users (id, name, email, age) VALUES
    (1, 'Szonja', 'szonja@email.com', 30),
    (2, 'Arthur', 'arthur@email.com', 35),
    (3, 'Maria', 'maria@email.com', 28);
```

## Tables — Where Data Lives

Data in a database is stored in **tables**. Think of a table like a spreadsheet:

```
| id | name     | email                  | age |
|----|----------|------------------------|-----|
| 1  | Szonja   | szonja@email.com       | 30  |
| 2  | Arthur   | arthur@email.com       | 35  |
| 3  | Maria    | maria@email.com        | 28  |
```

**Key parts:**
- **Table name:** `users` (in this case)
- **Columns:** id, name, email, age (the categories of data)
- **Rows:** Each person is one row (a complete record)
- **Cell:** One piece of data (like "Szonja" in the name column)

## Your First SQL Query

The most common SQL command is `SELECT` — it gets data from a table.

```sql
SELECT * FROM users;
```

**What this means:**
- `SELECT` = "get me data"
- `*` = "everything" (all columns)
- `FROM users` = "from the users table"

**Result:** You get back the entire table above.

## Selecting Specific Columns

You don't always want all the data. To get just names and emails:

```sql
SELECT name, email FROM users;
```

**Result:**
```
| name   | email                  |
|--------|------------------------|
| Szonja | szonja@email.com       |
| Arthur | arthur@email.com       |
| Maria  | maria@email.com        |
```

## Filtering with WHERE

To get only specific rows, use `WHERE`:

```sql
SELECT * FROM users WHERE age = 30;
```

**Result:**
```
| id | name   | email            | age |
|----|--------|------------------|-----|
| 1  | Szonja | szonja@email.com | 30  |
```

## Practice Exercise

**Scenario:** You're building a movie collection database from scratch.

**Your tasks:**

1. Create a database called `movie_collection`
2. Use that database
3. Create a table called `movies` with these columns:
   - `id` (INT)
   - `title` (VARCHAR(200))
   - `director` (VARCHAR(100))
   - `year` (INT)
4. Insert the following movies:
   - Inception, Christopher Nolan, 2010
   - Pulp Fiction, Quentin Tarantino, 1994
   - The Matrix, Lana Wachowski, 1999
   - Interstellar, Christopher Nolan, 2014
5. Write a query to get ALL movies
6. Write a query to get only the `title` and `year` columns
7. Write a query to get only movies directed by "Christopher Nolan"

**Try it yourself first!** Then scroll down to check your answers.

---

## Solutions

```sql
-- 1. Create the database
CREATE DATABASE movie_collection;

-- 2. Use the database
USE movie_collection;

-- 3. Create the movies table
CREATE TABLE movies (
    id INT,
    title VARCHAR(200),
    director VARCHAR(100),
    year INT
);

-- 4. Insert the movie data
INSERT INTO movies (id, title, director, year) VALUES
    (1, 'Inception', 'Christopher Nolan', 2010),
    (2, 'Pulp Fiction', 'Quentin Tarantino', 1994),
    (3, 'The Matrix', 'Lana Wachowski', 1999),
    (4, 'Interstellar', 'Christopher Nolan', 2014);

-- 5. Get all movies
SELECT * FROM movies;

-- 6. Get only title and year
SELECT title, year FROM movies;

-- 7. Get only Christopher Nolan movies
SELECT * FROM movies WHERE director = 'Christopher Nolan';
```

## Quick Recap

- Database = organised storage (like a filing cabinet)
- SQL = the language to talk to databases
- `CREATE DATABASE` = make a new database
- `USE` = switch to a database
- `CREATE TABLE` = make a new table with columns
- Table = where data lives (rows + columns)
- `INSERT INTO` = add data to a table
- `SELECT` = get data
- `FROM` = which table
- `WHERE` = filter results

## What's Next?

In Lesson 2, we'll learn about **different ways to filter and sort your data** — like finding movies from a certain year, or sorting by title!

**Continue to [Lesson 2: Filtering and Sorting](02-filtering-and-sorting.md)**

---

**Your turn:** Try the exercises above. If you get stuck or have questions, just ask! 💛
