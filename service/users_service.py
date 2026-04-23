from fastapi import HTTPException
from sqlalchemy.util import await_only
from starlette import status
from typing import Optional, List
from jose import jwt
from datetime import datetime,timedelta

from model.register_model import RegisterModel
from model.user_response_model import UserResponse
from utils.security import pwd_context
from model.login_model import LoginModel
from model.user_model import User
from repository import users_repository

async def get_users():
    return await users_repository.get_users()

async def get_user_by_id(user_id:int):
    return await users_repository.get_user_by_id(user_id)

async def get_user_by_username(username)-> UserResponse:
    return await users_repository.get_user_by_username(username)

async def create_user(user:RegisterModel):
    hashed_password = pwd_context.hash(user.password)
    hashed_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        age=user.age,
        email=user.email,
        phone=user.phone,
        address=user.address,
        username=user.username,
        hashed_password=hashed_password
    )
    return await users_repository.create_user(hashed_user)

async def verify_password(password:str, hashed_password:str):
    return pwd_context.verify(password, hashed_password)

async def update_user(user_id:int, first_name:str, last_name:str, email:str, age:int):
    user_check = await get_user_by_id(user_id)
    if not user_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return await users_repository.update_user(user_id,first_name,last_name,email,age)

async def delete_user(user_id:int):
    user_check = await get_user_by_id(user_id)
    if not user_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return await users_repository.delete_user(user_id)
