from typing import Optional, List

import json
from repository.database import database

async def get_users():
    query="""
    SELECT * 
    FROM users
    """
    return await database.fetch_all(query)

async def create_user(first_name:str, last_name:str, email:str, age:int):
    query="""
    INSERT INTO users (first_name, last_name, email, age)
    VALUES(:first_name, :last_name, :email, :age)
    """
    values={"first_name":first_name,"last_name":last_name,"email":email,"age":age}
    await database.execute(query, values)

async def update_user(user_id:int, first_name:str, last_name:str, email:str, age:int):
    query = """
    UPDATE users
    SET first_name = :first_name, last_name = :last_name, email = :email, age = :age 
    WHERE user_id = :user_id
    """
    values={"user_id":user_id,"first_name":first_name,"last_name":last_name,"email":email,"age":age}
    await database.execute(query,values)

async def get_user_by_id(user_id:int):
    query = """
    SELECT * FROM users
    WHERE user_id = :user_id
    """
    values = {"user_id": user_id}
    result = await database.fetch_one(query,values)
    return result

async def delete_user(user_id:int):
    query = """
    DELETE FROM users
    WHERE user_id = :user_id
    """
    values = {"user_id":user_id}
    await database.execute(query,values)