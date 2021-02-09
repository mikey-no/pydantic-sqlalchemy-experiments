# Simple test Application to test using SQLAlchemy and Pydantic (database update)

## Purpose of this application is to:
- Improve my understanding of SQLAlchemy and Pydantic
- Help work out the details of database partial update
- To record how to do this for future reference in a number of [FastAPI](https://fastapi.tiangolo.com/) apps
- To provide a basis for further work and experiments
- Might help someone else - the lack of update in the [FastAPI SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/) demo application was/is a problem for me but this  
[New pull request may help](https://github.com/tiangolo/fastapi/pull/2665) from akihiro-inui


## Features of the application:
- It tested with pytest [1]
- Uses an in memory sqlite database [2]
- Uses the SQLAlchemy declarative model definition, not the imperative definition as used by [Mr-Manna FastAPI CRUD](https://github.com/Mr-Manna/FastAPI-CRUD)
- It just uses pip (simple as can be)
- Automatically works out the name of each attribute to be updated

### Feature: test_user_update() - using pydantic
- uses pydantic to merge the two dictionaries
- bit complicated

### Feature: test_user_update_2() - using setattr(db_user, var, value)
- uses the python `setattr` function [w3schools setattr](https://www.w3schools.com/python/ref_func_setattr.asp)
- simpler
- **preferred**

### Feature: demonstrate a bug, use function test_user_update_3()
- calls a function with the bug (would have to be uncommented to run)
- pytest calls this method and 2 tests pass (as above), but the test associated with this bug fails


This application started here [pydantic-sqlalchemy](https://github.com/tiangolo/pydantic-sqlalchemy). I was looking for
a simple way to update a sqlalchemy model.

I am not fully satisfied with the comments I have added to the test_user_update function. I wanted to provide clear 
information about what is going on.

# To setup

Clone the repository

```commandline
python -m venv venv
venv\scripts\activate.bat
pip install -r requirements.txt
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

- [1] pytest has better methods to initiate and clean up before and after each test. I have used none of them to 
ensure this remains a single page application.
- [2] This does not work in a FastAPI application (I could not make this work). This same functionality is difficult to achieve. 
I used [timhuges - in memory database running test](https://github.com/timhughes/example-fastapi-sqlachemy-pytest) 
to enable this functionality, but this is not included here (yet?).
