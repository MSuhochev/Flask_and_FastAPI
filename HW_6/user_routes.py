from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import update, delete
from HW_6.market_db import database, users
from typing import Annotated

router = APIRouter()


class UserIn(BaseModel):
    name: str = Field(..., tittle="User_Name", max_length=50)
    surname: str = Field(default=None, title="User_Surname", max_length=50)
    email: str = Field(..., tittle="User_email", max_length=70)
    password: str = Field(..., tittle="User_Password", min_length=6)


class User(BaseModel):
    id: int
    name: str = Field(..., tittle="User_Name", max_length=50)
    surname: str = Field(default=None, title="User_Surname", max_length=50)
    email: str = Field(..., tittle="User_email", max_length=70)
    password: str = Field(..., tittle="User_Password", min_length=6)


@router.post("/new_user/")
async def create_user(user: Annotated[UserIn, Depends()]):
    """
      Create a new user.
    """
    query = users.insert().values(**user.dict())
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@router.get("/users/")
async def get_users():
    """
    Get all users.
    """
    query = users.select()
    return await database.fetch_all(query)


@router.get("/user/{user_id}")
async def get_user(user_id: int):
    """
    Get user by ID.
    """
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/user/{user_id}")
async def update_user(user_id: int, user: Annotated[UserIn, Depends()]):
    """
    Update user by ID.
    """
    query = (
        update(users)
        .where(users.c.id == user_id)
        .values(
            name=user.name,
            surname=user.surname,
            email=user.email,
            password=user.password
        )
    )
    await database.execute(query)
    return {"message": "User updated successfully"}


@router.delete("/user/{user_id}")
async def delete_user(user_id: int):
    """
    Delete user by ID.
    """
    query = delete(users).where(users.c.id == user_id)
    await database.execute(query)
    return {"message": "User deleted successfully"}
