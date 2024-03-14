# Install all the dependencies from pyproject.toml using:

    poetry install

# We have cover following in this step:

    * Class Hero is created along with it's table in DB
    * DB connection string setup
    * Create Database and tables through create_db_and_tables() function
    * FastAPI instance created i.e app
    * Insert the data into the Database using post request
    * Read the data from the Database using get request

# Run the server using:

    poetry run uvicorn create_db_table.main:app --host 0.0.0.0 --port 8000 --reload

# Swagger UI:

    http://127.0.0.1:8000/docs

--reload flag:
It will restart the server every time you make a change to the code.

# Why we use SQLModel and what are it's advantages?

- SQLModel is a Python library used to interact with databases using the SQL
- SQLModel class models be both SQLAlchemy models (help us to create a session and database queries) and Pydantic models (helps us in automatic validation and conversion from JSON request to an object i.e instance of Hero class here) at the same time.
- We use the same class model to define the request body that will be received by our API

## Analogy of SQLModel:
Imagine you're building a house. You have a blueprint that outlines every detail of how your house will be built, from the number of rooms to the types of windows. SQLModel works like that blueprint for your database. It allows you to clearly define the structure of your data, like what kind of information each table will hold and how different pieces of information are related to each other.
