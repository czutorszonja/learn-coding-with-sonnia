# Python Lesson 15: Advanced Database Operations — Relationships and Joins 🔗

**← Back to [Lesson 14: Working with Databases](14-working-with-databases.md)**

---

## What are Database Relationships?

**Plain English:** Relationships connect data in different tables, like linking authors to their books.

**Real-world analogy:** Think of a school:
- Students table — List of all students
- Courses table — List of all courses
- Enrollments table — Connects students to courses (relationships!)

Relationships prevent data duplication and keep everything organized!

---

## Types of Relationships

### One-to-Many (Most Common)
One author → Many books

```sql
-- Authors table
CREATE TABLE authors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Books table (has author_id as foreign key)
CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES authors(id)
);
```

---

## JOIN Queries

**JOIN** combines data from multiple tables:

```python
import sqlite3

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Get all books with their authors
cursor.execute('''
    SELECT books.title, authors.name
    FROM books
    JOIN authors ON books.author_id = authors.id
''')

results = cursor.fetchall()
for title, author in results:
    print(f"{title} by {author}")

conn.close()
```

---

## Practice Exercise

**Scenario:** You're building a movie database system for a film club!

**Your task:**
1. Create a database file called `movies.db`
2. Create these tables:
   - `directors` (id, name, birth_year)
   - `movies` (id, title, release_year, director_id, rating)
   - `actors` (id, name, birth_year)
   - `movie_actors` (movie_id, actor_id) — junction table
3. Create functions:
   - `add_director(name, birth_year)` — Add a director
   - `add_movie(title, release_year, director_id, rating)` — Add a movie
   - `add_actor(name, birth_year)` — Add an actor
   - `link_actor_to_movie(movie_id, actor_id)` — Link actor to movie
   - `get_movie_with_director(movie_id)` — Return movie with director name
   - `get_actors_in_movie(movie_id)` — Return all actors in a movie
   - `get_movies_by_director(director_id)` — Return all movies by a director
4. Test with sample data (at least 2 directors, 4 movies, 5 actors)

**Example usage:**
```python
spielberg_id = add_director("Steven Spielberg", 1946)
inception_id = add_movie("Inception", 2010, spielberg_id, 8.8)
dicaprio_id = add_actor("Leonardo DiCaprio", 1974)
link_actor_to_movie(inception_id, dicaprio_id)

movie = get_movie_with_director(inception_id)
print(f"{movie['title']} directed by {movie['director_name']}")

actors = get_actors_in_movie(inception_id)
for actor in actors:
    print(f"  - {actor['name']}")
```

**Try it yourself first!** Solution below.

---

## Solution

```python
# movie_database.py

import sqlite3


def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect('movies.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    """Create all tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS directors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            birth_year INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            release_year INTEGER,
            director_id INTEGER,
            rating REAL,
            FOREIGN KEY (director_id) REFERENCES directors(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS actors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            birth_year INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movie_actors (
            movie_id INTEGER,
            actor_id INTEGER,
            FOREIGN KEY (movie_id) REFERENCES movies(id),
            FOREIGN KEY (actor_id) REFERENCES actors(id)
        )
    ''')
    
    conn.commit()
    conn.close()


def add_director(name, birth_year):
    """Add a director."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO directors (name, birth_year) VALUES (?, ?)
    ''', (name, birth_year))
    
    director_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return director_id


def add_movie(title, release_year, director_id, rating):
    """Add a movie."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO movies (title, release_year, director_id, rating)
        VALUES (?, ?, ?, ?)
    ''', (title, release_year, director_id, rating))
    
    movie_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return movie_id


def add_actor(name, birth_year):
    """Add an actor."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO actors (name, birth_year) VALUES (?, ?)
    ''', (name, birth_year))
    
    actor_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return actor_id


def link_actor_to_movie(movie_id, actor_id):
    """Link an actor to a movie."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO movie_actors (movie_id, actor_id) VALUES (?, ?)
    ''', (movie_id, actor_id))
    
    conn.commit()
    conn.close()


def get_movie_with_director(movie_id):
    """Get movie with director name."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT movies.title, movies.release_year, movies.rating,
               directors.name as director_name
        FROM movies
        JOIN directors ON movies.director_id = directors.id
        WHERE movies.id = ?
    ''', (movie_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    return dict(result) if result else None


def get_actors_in_movie(movie_id):
    """Get all actors in a movie."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT actors.name
        FROM actors
        JOIN movie_actors ON actors.id = movie_actors.actor_id
        WHERE movie_actors.movie_id = ?
    ''', (movie_id,))
    
    results = cursor.fetchall()
    conn.close()
    
    return [dict(actor) for actor in results]


def get_movies_by_director(director_id):
    """Get all movies by a director."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT title, release_year, rating
        FROM movies
        WHERE director_id = ?
        ORDER BY release_year DESC
    ''', (director_id,))
    
    results = cursor.fetchall()
    conn.close()
    
    return [dict(movie) for movie in results]


# Test the functions
if __name__ == '__main__':
    create_tables()
    spielberg_id = add_director("Steven Spielberg", 1946)
    inception_id = add_movie("Inception", 2010, spielberg_id, 8.8)
    dicaprio_id = add_actor("Leonardo DiCaprio", 1974)
    link_actor_to_movie(inception_id, dicaprio_id)
    
    movie = get_movie_with_director(inception_id)
    print(f"{movie['title']} directed by {movie['director_name']}")
    
    actors = get_actors_in_movie(inception_id)
    for actor in actors:
        print(f"  - {actor['name']}")
```

---

## Quick Recap

- **Relationships** — Connect data across tables
- **Foreign keys** — Link tables together
- **One-to-Many** — One record relates to many others
- **Many-to-Many** — Requires junction table
- **JOIN** — Combine data from multiple tables
- **Junction tables** — Handle many-to-many relationships

---

## What's Next?

Ready for more? Continue to **[Lesson 16: Authentication and Security](16-authentication-and-security.md)**! 🚀

---

**Your turn:** Try the movie database exercise! Add features like searching by actor or getting top-rated movies! 🔗💛
