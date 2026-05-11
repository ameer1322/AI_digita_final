from typing import Optional, List

from fastapi import APIRouter, HTTPException, Header
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status
from model.order_request import OrderRequest
from config.config import Config
from model.remove_from_order_request import RemoveFromOrderRequest
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

@router.get("/get_order_by_user",status_code=status.HTTP_200_OK)
async def get_order_id_by_user(authorization: str = Header()):
    token = authorization.replace("Bearer: ","")
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms= [config.ALGORITHM])
        user_id = payload["id"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")
    return await order_service.get_order_id_by_user(user_id)

@router.put("/",status_code=status.HTTP_201_CREATED)
async def handle_order(order : OrderRequest, authorization: str= Header()):
    token = authorization.replace("Bearer: ","")
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms= [config.ALGORITHM])
        user_id = payload["id"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")
    try:
        return await order_service.handle_order(order, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))

@router.delete("/{order_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id : int):
    return await order_service.delete_order(order_id)

@router.get("/get_user_unconfirmed_order",status_code=status.HTTP_200_OK)
async def get_user_unconfirmed_order(authorization: str = Header()):
    token = authorization.replace("Bearer: ","")
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms= [config.ALGORITHM])
        user_id = payload["id"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")
    try:
        return await order_service.get_user_unconfirmed_order(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/get_user_confirmed_orders",status_code=status.HTTP_200_OK)
async def get_user_confirmed_orders(authorization:str = Header()):
    token = authorization.replace("Bearer: ","")
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        user_id = payload["id"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")
    try:
        return await order_service.get_user_confirmed_orders(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/remove_from_order",status_code=status.HTTP_200_OK)
async def remove_from_order(remove_request : RemoveFromOrderRequest,authorization : str = Header()):
    token = authorization.replace("Bearer: ", "")
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        user_id = payload["id"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")
    try:
        return await order_service.remove_from_order(remove_request.product_name,remove_request.amount,user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/confirm_order",status_code=status.HTTP_200_OK)
async def confirm_order(authorization:str = Header()):
    token = authorization.replace("Bearer: ", "")
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        user_id = payload["id"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")
    try:
        return await order_service.confirm_order(user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))