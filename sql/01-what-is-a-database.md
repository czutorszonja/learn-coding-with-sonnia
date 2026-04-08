# SQL Lesson 1: What is a Database?

## What is a Database?

**Plain English:** A database is like a digital filing cabinet where you store organized information.

**Real-world analogy:** Imagine a library:
- Books are organized by category (fiction, science, history)
- Each book has a title, author, ISBN, and location
- You can search for books by title, author, or topic
- The librarian helps you find exactly what you need

A database works the same way — it stores data in organized tables, and you can ask it questions.

## What is SQL?

**SQL** = Structured Query Language

**Plain English:** SQL is the language you use to talk to a database.

**Real-world analogy:** If the database is the librarian, SQL is the words you use to ask for books.

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

**Scenario:** You have a database table called `movies`:

```
| id | title           | director        | year |
|----|-----------------|-----------------|------|
| 1  | Inception       | Christopher Nolan | 2010 |
| 2  | Pulp Fiction    | Quentin Tarantino | 1994 |
| 3  | The Matrix      | Lana Wachowski   | 1999 |
| 4  | Interstellar    | Christopher Nolan | 2014 |
```

**Your tasks:**
1. Write a query to get ALL movies
2. Write a query to get only the `title` and `year` columns
3. Write a query to get only movies directed by "Christopher Nolan"

**Try it yourself first!** Then scroll down to check your answers.

---

## Solutions

```sql
-- 1. Get all movies
SELECT * FROM movies;

-- 2. Get only title and year
SELECT title, year FROM movies;

-- 3. Get only Christopher Nolan movies
SELECT * FROM movies WHERE director = 'Christopher Nolan';
```

## Quick Recap

- Database = organized storage (like a filing cabinet)
- SQL = the language to talk to databases
- Table = where data lives (rows + columns)
- `SELECT` = get data
- `FROM` = which table
- `WHERE` = filter results

## What's Next?

In Lesson 2, we'll learn about **different ways to filter and sort your data** — like finding movies from a certain year, or sorting by title!

---

**Your turn:** Try the exercises above. If you get stuck or have questions, just ask! 💛
