from fastapi import HTTPException
from sqlalchemy.util import await_only
from starlette import status
from typing import Optional, List
from jose import jwt
from datetime import datetime,timedelta

from model.user_response_model import UserResponse
from utils.security import pwd_context
from model.login_model import LoginModel
from model.user_model import User
from repository import users_repository

async def get_users():
    try:
        return await users_repository.get_users()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

async def get_user_by_id(user_id:int):
    try:
        return await users_repository.get_user_by_id(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

async def get_user_by_username(username)-> UserResponse:
    try:
        return await users_repository.get_user_by_username(username)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

async def create_user(user:User):
    try:
        return await users_repository.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

async def verify_password(password:str, hashed_password:str):
    return pwd_context.verify(password, hashed_password)

async def update_user(user_id:int, first_name:str, last_name:str, email:str, age:int):
    user_check = await get_user_by_id(user_id)
    if not user_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    try:
        return await users_repository.update_user(user_id,first_name,last_name,email,age)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def delete_user(user_id:int):
    user_check = await get_user_by_id(user_id)
    if not user_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    try:
        return await users_repository.delete_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
