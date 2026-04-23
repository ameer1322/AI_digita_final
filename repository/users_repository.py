from typing import Optional, List

import json

from model.user_model import User
from model.user_response_model import UserResponse
from repository.database import database


async def get_users()->List[UserResponse]:
    query="""
    SELECT * 
    FROM users
    """
    result = await database.fetch_all(query)
    return [UserResponse(**row) for row in result]

async def create_user(user:User):
    query="""
    INSERT INTO users (first_name, last_name, age, email, phone, address, username, hashed_password)
    VALUES(:first_name, :last_name, :age, :email, :phone, :address, :username, :hashed_password)
    """
    values={"first_name":user.first_name, "last_name":user.last_name, "age":user.age, "email":user.email, "phone":user.phone, "address":user.address, "username":user.username, "hashed_password":user.hashed_password}
    await database.execute(query, values)

async def update_user(user_id:int, first_name:str, last_name:str, email:str, age:int):
    query = """
    UPDATE users
    SET first_name = :first_name, last_name = :last_name, email = :email, age = :age 
    WHERE user_id = :user_id
    """
    values={"user_id":user_id,"first_name":first_name,"last_name":last_name,"email":email,"age":age}
    await database.execute(query,values)

async def get_user_by_username(username:str)-> Optional[UserResponse]:
    query = """
    SELECT * FROM users
    WHERE username = :username
    """
    values = {"username": username}
    result = await database.fetch_one(query,values)
    if result:
        return UserResponse(**dict(result))
    else:
        raise ValueError("User not found")

async def get_user_by_id(user_id:int)->User:
    query = """
    SELECT * FROM users
    WHERE user_id = :user_id
    """
    values = {"user_id": user_id}
    result = await database.fetch_one(query,values)
    return User(**result)

async def delete_user(user_id:int):
    query = """
    DELETE FROM users
    WHERE user_id = :user_id
    """
    values = {"user_id":user_id}
    await database.execute(query,values)