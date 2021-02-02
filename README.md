#Simple test Application to test using SQLAlchemy and Pydantic (database update)

This application started here [pydantic-sqlalchemy](https://github.com/tiangolo/pydantic-sqlalchemy).
I am not fully satisfied with the comments I have added to the test_update function. I wanted to provide clear 
information about what is going on.

## Purpose of this application is to:
- Improve my understanding of SQLAlchemy and Pydantic
- Help work out the details of database partial update
- To record how to do this for future reference in a number of [FastAPI](https://fastapi.tiangolo.com/) applications  I am writing
- To provide a basis for further work and experiments
- Might help someone else - the lack of update in the [FastAPI SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/) demo application was/is a problem for me   


## Features of the application:
- Has pytest
- Uses an in memory sqlite database [1]
- Uses the SQLAlchemy declarative model definition, not the imperative definition as used by [Mr-Manna FastAPI CRUD](https://github.com/Mr-Manna/FastAPI-CRUD)
- It just uses pip (simple as can be)

# To setup

Clone the repository

```commandline
python -m venv venv
venv\scripts\activate.bat
pip install -r requirements
```

# To run

```commandline
python main.py
```

# To test

```commandline
pytest main.py
```

## Notes

[1] This does not work in a FastAPI application (I could not make this work). This same functionality is difficult to achieve. 
I used [timhuges - in memory database running test](https://github.com/timhughes/example-fastapi-sqlachemy-pytest) 
to enable this functionality, but this is not included here (yet?).
