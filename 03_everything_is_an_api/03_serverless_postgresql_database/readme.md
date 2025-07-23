# Using Serverless Neon Postgres Database with Python

We will use [Neon Serverless Postgres](https://neon.tech/docs/guides/python) as our database and use [SQLAlchemy](https://www.sqlalchemy.org/) as our ORM. We will follow these tutorials:

https://neon.tech/docs/guides/sqlalchemy

https://docs.sqlalchemy.org/en/20/tutorial/

https://www.sqlalchemy.org/

SqlAlchemy is a popular Object-Relational Mapping (ORM) library in Python that provides a way to interact with databases using Python objects rather than writing raw SQL queries. 

However, I can provide you with a general explanation of the advantages of using SQLAlchemy or any ORM in a Python project, which can be applied to various databases.

## Advantages of using SQLAlchemy or any ORM in a Python project:

1. Abstraction of Database Complexity: ORMs like SQLAlchemy abstract away the underlying database complexities. Developers can work with Python classes and objects, which are more intuitive and familiar than writing SQL queries directly. This abstraction makes it easier to work with databases, especially for developers who are not SQL experts.

2. Portability: ORMs provide a level of database independence. You can write code using SQLAlchemy, and with minimal changes, switch between different database systems (e.g., SQLite, PostgreSQL, MySQL) without having to rewrite your entire database access layer.

3. Object-Oriented Approach: ORMs allow you to work with databases using object-oriented programming principles. Database tables are typically represented as Python classes, and rows in those tables become instances of those classes. This approach can make the code more organized and maintainable.

4. Improved Readability and Maintainability: Code that uses an ORM tends to be more readable and maintainable than raw SQL queries. It's easier to understand and debug Python code that manipulates objects and attributes rather than dealing with complex SQL statements.

5. Security: ORMs help prevent SQL injection attacks by automatically escaping and sanitizing input data. This can enhance the security of your application.

6. Query Building: ORMs provide a high-level API for building database queries. This can simplify complex queries and joins, as well as make it easier to filter, sort, and aggregate data.

7. Middleware and Hooks: ORMs often provide hooks and middleware for database interactions, allowing you to add custom logic, validation, or auditing to your database operations.

8. Testing: ORM-based code is often easier to test because you can work with in-memory databases or fixtures, making it simpler to set up and tear down test data.

9. Integration with Frameworks: Many web frameworks (e.g., Flask, Django) have built-in support or plugins for popular ORMs like SQLAlchemy, making it seamless to integrate database operations into web applications.

10. Community and Ecosystem: Popular ORMs like SQLAlchemy have active communities and extensive documentation. You can find many resources, tutorials, and plugins to help you work with databases effectively.



---

## SQLAlchemy: Connection vs. Session


SQLAlchemy provides a powerful and flexible way to interact with databases in Python. At its heart, it differentiates between managing the **physical connection** to the database and managing the **transactional scope** of your operations. This is where `Connection` and `Session` come into play.

### The `Engine`

Before diving into `Connection` and `Session`, it's crucial to understand the `Engine`. The `Engine` is the starting point for any SQLAlchemy application. It's responsible for managing a pool of database connections and providing a way to acquire them.

```python
from sqlalchemy import create_engine

# An Engine for connecting to a SQLite database in memory
engine = create_engine('sqlite:///:memory:')
```

The `Engine` is typically created once per application and acts as a central factory for `Connection` objects.

-----

## `Connection` (SQLAlchemy Core)

The `Connection` object is a low-level construct provided by SQLAlchemy Core. It represents a **single, active connection to the database**. When you use a `Connection`, you are directly interacting with the database at a more fundamental level, executing SQL statements and managing transactions explicitly.

### Key Characteristics of `Connection`:

  * **Direct Database Interaction:** `Connection` allows you to execute raw SQL queries using methods like `execute()`.
  * **Manual Transaction Management:** You are responsible for explicitly beginning, committing, or rolling back transactions using `begin()`, `commit()`, and `rollback()`.
  * **Stateless:** `Connection` does not keep track of the state of your Python objects or map them to database rows. It's purely for executing SQL.
  * **Context Manager Support:** `Connection` objects are typically used within a `with` statement, ensuring proper closing and resource management.

### When to Use `Connection`:

  * **Executing DDL (Data Definition Language) statements:** Creating tables, altering schemas, etc.
  * **Performing bulk operations:** When you need to insert or update many rows efficiently without the overhead of ORM mapping.
  * **Executing stored procedures or highly optimized SQL:** For scenarios where the ORM might introduce unnecessary overhead.
  * **Low-level database administration tasks.**

### Example Usage:

```python
from sqlalchemy import text

with engine.connect() as connection:
    # Begin a transaction
    with connection.begin():
        # Execute a DDL statement
        connection.execute(text("CREATE TABLE users (id INTEGER, name VARCHAR)"))
        print("Table 'users' created.")

        # Insert data
        connection.execute(
            text("INSERT INTO users (id, name) VALUES (:id, :name)"),
            [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        )
        print("Data inserted.")

        # Query data
        result = connection.execute(text("SELECT id, name FROM users"))
        for row in result:
            print(f"User ID: {row.id}, Name: {row.name}")

    # Transaction automatically committed here if no exceptions, rolled back otherwise
```

-----

## `Session` (SQLAlchemy ORM)

The `Session` object is the cornerstone of the SQLAlchemy ORM (Object Relational Mapper). It provides a high-level interface for interacting with your database by **mapping Python objects to database rows**. The `Session` manages the **lifecycle of your objects**, tracks changes, and orchestrates database operations within a **transactional context**.

### Key Characteristics of `Session`:

  * **Object-Relational Mapping:** `Session` allows you to work with Python objects (instances of your mapped classes) instead of raw SQL rows. It handles the translation between objects and database records.
  * **Unit of Work Pattern:** The `Session` acts as a "unit of work." You make changes to your Python objects, and the `Session` tracks these changes. When you call `commit()`, all pending changes are flushed to the database in a single transaction.
  * **Identity Map:** The `Session` maintains an "identity map" to ensure that for a given primary key, there's only one Python object instance within that session. This prevents data inconsistencies.
  * **Automatic Transaction Management (Implicit):** While you explicitly call `commit()` or `rollback()`, the `Session` internally manages the underlying `Connection`'s transaction. It often acquires a `Connection` from the `Engine` when needed and releases it.
  * **Lazy Loading:** `Session` supports lazy loading of relationships, fetching related data only when it's accessed.
  * **Session Scope:** A `Session` is typically short-lived, representing a single logical transaction or a unit of work. It should be created, used, and closed for each request or operation.

### When to Use `Session`:

  * **When using the SQLAlchemy ORM:** This is the primary way to interact with your mapped classes.
  * **Managing the lifecycle of your application objects:** Creating, reading, updating, and deleting records as Python objects.
  * **Leveraging relationships between objects:** Easily navigate related data (e.g., a user's posts).
  * **Building complex application logic where object state is important.**

### Example Usage:

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Define your base for declarative models
Base = declarative_base()

# Define a User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Create an engine
engine = create_engine('sqlite:///:memory:')

# Create all tables (based on defined models)
Base.metadata.create_all(engine)

# Create a Session factory
Session = sessionmaker(bind=engine)

# Create a session instance
with Session() as session:
    # Create new users
    new_user1 = User(id=1, name="Alice")
    new_user2 = User(id=2, name="Bob")

    session.add(new_user1)
    session.add(new_user2)
    print("Users added to session.")

    # Query users
    users = session.query(User).all()
    print("Users from session:")
    for user in users:
        print(user)

    # Update a user
    user_to_update = session.query(User).filter_by(name="Alice").first()
    if user_to_update:
        user_to_update.name = "Alicia"
        print(f"User updated: {user_to_update}")

    # Delete a user
    user_to_delete = session.query(User).filter_by(name="Bob").first()
    if user_to_delete:
        session.delete(user_to_delete)
        print(f"User deleted: {user_to_delete}")

    # Commit all changes to the database
    session.commit()
    print("Changes committed to database.")

    # Verify changes in a new session (important for seeing committed data)
    with Session() as new_session:
        remaining_users = new_session.query(User).all()
        print("Users after commit (from new session):")
        for user in remaining_users:
            print(user)
```

-----

### Key Differences Summarized

| Feature             | `Connection` (SQLAlchemy Core)                 | `Session` (SQLAlchemy ORM)                       |
| :------------------ | :--------------------------------------------- | :----------------------------------------------- |
| **Level** | Low-level database interaction                 | High-level ORM interaction                       |
| **Purpose** | Execute SQL statements, manage raw connections | Map Python objects to database, manage object state |
| **Object Mapping** | None                                           | Yes, manages mapped Python objects               |
| **Transaction** | Explicitly managed (`begin()`, `commit()`)     | Implicitly managed (via `session.commit()`)      |
| **State** | Stateless                                      | Stateful (identity map, unit of work)            |
| **Use Cases** | DDL, bulk operations, raw SQL, admin           | CRUD operations with ORM, object relationships   |
| **Lifecycle** | Short-lived, acquired for specific operations  | Short-lived, per-request/per-transaction         |
| **Resource Mgmt.** | Must be closed explicitly or via context mgr.  | Handles underlying connection acquisition/release |
| **Primary Access** | `engine.connect()`                             | `sessionmaker(bind=engine)()`                    |

-----

### Choosing Between `Connection` and `Session`

  * **For most application development using the ORM:** You'll primarily use `Session`. It provides a much more intuitive and Pythonic way to interact with your database by working with objects.
  * **For administrative tasks, complex migrations, or highly optimized bulk data operations that don't fit well with the ORM:** `Connection` is the appropriate choice. It gives you direct control over the database.

It's common to use both within a larger application. For instance, you might use `Connection` for initial database setup or schema migrations, while `Session` handles the day-to-day data manipulation through your ORM models.

-----

### Best Practices

  * **Always use `with` statements:** Whether you're using `engine.connect()` or a `Session` instance, using `with` ensures that resources are properly acquired and released (connections are returned to the pool, sessions are closed).
  * **Keep `Session` short-lived:** A `Session` should typically correspond to a single logical unit of work (e.g., an HTTP request in a web application). Avoid long-lived sessions that might accumulate too much state or hold onto connections unnecessarily.
  * **Separate concerns:** Design your application so that database interaction logic is encapsulated, whether it uses `Connection` or `Session`.
  * **Understand transaction boundaries:** Be clear about when your changes are committed to the database. For `Session`, changes are flushed and committed only when `session.commit()` is called. If an error occurs, `session.rollback()` should be used.
