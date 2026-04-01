from typing import Optional, List

from fastapi import APIRouter, HTTPException
from starlette import status
from model.user_model import User

from service import users_service

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/",status_code=status.HTTP_200_OK)
async def get_users():
    try:
        return await users_service.get_users()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    try:
        return await users_service.create_user(user.first_name,user.last_name,user.email,user.age)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.put("/{user_id}",status_code=status.HTTP_200_OK)
async def update_user(user_id:int, user:User):
    try:
        return await users_service.update_user(user_id,user.first_name,user.last_name,user.email,user.age)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id:int):
    try:
        return await users_service.delete_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
