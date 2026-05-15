from typing import Optional, List

from fastapi import APIRouter, HTTPException, Header
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status
from model.order_request import OrderRequest
from config.config import Config
from service import order_product_service
import jwt

router = APIRouter(
    prefix="/order_product",
    tags=["order_product"]
)

@router.get("/",status_code=status.HTTP_200_OK)
async def get_order_products():
    try:
        return await order_product_service.get_order_products()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
