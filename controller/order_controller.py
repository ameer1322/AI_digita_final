from typing import Optional, List

from fastapi import APIRouter, HTTPException, Header
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status
from model.order_request import OrderRequest
from config.config import Config
from service import order_service
import jwt

router = APIRouter(
    prefix="/order",
    tags=["order"]
)

config = Config()

@router.get("/",status_code=status.HTTP_200_OK)
async def get_orders():
    return await order_service.get_orders()

@router.put("/",status_code=status.HTTP_201_CREATED)
async def handle_order(order : OrderRequest, authorization: str= Header()):
    token = authorization.replace("Bearer ","")
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms = [config.ALGORITHM])
        user_id = payload["id"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")
    return await order_service.handle_order(order, user_id)

@router.delete("/{order_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id : int):
    return await order_service.delete_order(order_id)
