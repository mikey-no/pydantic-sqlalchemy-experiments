from typing import List, Optional

# from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

engine = create_engine("sqlite://", echo=False) # this does not work in FastAPI BTW, in memory sqlite db does not work

create_now = datetime.utcnow() # fake created time - making testing consistency easier
modified_now = datetime.utcnow() # fake last modified time

# show extra print statements
__SHOW__ = False


"""
Sqlalchemy using declarative style model definitions and pydantic 
without pydantic_sqlachemy
"""

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    created = Column(DateTime(timezone=True), default=create_now) # func.now() instead of create_now
    modified = Column(DateTime(timezone=True), onupdate=modified_now)

    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete, delete-orphan"
    )


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="addresses")


# PydanticUser = sqlalchemy_to_pydantic(User)
# PydanticAddress = sqlalchemy_to_pydantic(Address)

class PydanticUser(BaseModel):
    id: int
    name: str
    fullname: str
    nickname: str
    created: datetime
    modified: Optional[datetime]

    class Config:
        orm_mode = True


class PydanticUserUpdate(BaseModel):
    id: Optional[int]
    name: Optional[str]
    fullname: Optional[str]
    nickname: Optional[str]
    created: Optional[datetime]

    class Config:
        orm_mode = True


class PydanticAddress(BaseModel):
    id: int
    email_address: str
    user_id: int

    class Config:
        orm_mode = True


class PydanticUserWithAddresses(PydanticUser):
    addresses: List[PydanticAddress] = []


Base.metadata.create_all(engine)

LocalSession = sessionmaker(bind=engine)

db: Session = LocalSession()

ed_user = User(name="ed", fullname="Ed Jones", nickname="edsnickname")

address = Address(email_address="ed@example.com")
address2 = Address(email_address="eddy@example.com")
ed_user.addresses = [address, address2]
db.add(ed_user)
db.commit()


def test_normal_orm():
    user = db.query(User).first()
    pydantic_user = PydanticUser.from_orm(user)
    data = pydantic_user.dict()
    assert data == {
        "fullname": "Ed Jones",
        "id": 1,
        "name": "ed",
        "nickname": "edsnickname",
        "created": create_now,
        "modified": None
    }
    pydantic_user_with_addresses = PydanticUserWithAddresses.from_orm(user)
    data = pydantic_user_with_addresses.dict()
    assert data == {
        "created": create_now,
        "fullname": "Ed Jones",
        "id": 1,
        "name": "ed",
        "nickname": "edsnickname",
        "modified": None,
        "addresses": [
            {"email_address": "ed@example.com", "id": 1, "user_id": 1},
            {"email_address": "eddy@example.com", "id": 2, "user_id": 1},
        ],
    }


def demo():
    user = db.query(User).first()
    pydantic_user = PydanticUser.from_orm(user)
    data = pydantic_user.dict()
    print(data)


def test_user_update():
    """ Based on the FastAPI sqlalchemy demo app that does not include the update operation :( """
    print('\n')
    # make the query for the relevant record (needed later)
    user_query = db.query(User)
    # get the existing data
    user_stored = user_query.first()
    pydantic_user_stored = PydanticUser.from_orm(user_stored)
    user_data = pydantic_user_stored.dict()
    if __SHOW__: print(f'existing user: {user_data}')
    assert user_data == {
        "fullname": "Ed Jones",
        "id": 1,
        "name": "ed",
        "nickname": "edsnickname",
        "created": create_now,
        "modified": None
    }

    # make the pydantic update model (done in router.py normally)
    user_updates_pydantic = PydanticUserUpdate(name='fred', nickname='python')
    user_updates_data = user_updates_pydantic.dict(exclude_unset=True)

    # add in the modified datetime
    user_updates_data["modified"] = modified_now

    # create the merged dict with new updates overwriting existing data
    updated_user_data = pydantic_user_stored.copy(update=user_updates_data)
    if __SHOW__: print(f'updated_user_data: {updated_user_data.dict()}')

    # add the update to the db - re-use the same query
    user_query.update(updated_user_data)
    db.commit()
    db.refresh(user_stored)

    # load the result back from the db and and test it has taken the results and not lost unchanging values
    user_stored_res = db.query(User).first()
    pydantic_user_stored_res = PydanticUser.from_orm(user_stored_res)
    pydantic_user_stored_res_dict = pydantic_user_stored_res.dict()
    if __SHOW__: print(f're-read from the db the updated user object: {pydantic_user_stored_res_dict}')
    assert pydantic_user_stored_res_dict == {
        'created': create_now,
        'modified': modified_now,
        'fullname': 'Ed Jones',
        'id': 1,
        'name': 'fred',
        'nickname': 'python'
    }


if __name__ == "__main__":
    test_user_update() # when you do not want to call via pytest
