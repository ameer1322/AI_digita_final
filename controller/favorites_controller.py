from typing import Optional, List

from fastapi import APIRouter, HTTPException, Header
from starlette import status
from model.favorites_request_model import FavoriteRequest
from config.config import Config
from service import favorites_service
import jwt


router = APIRouter(
    prefix="/favorites",
    tags=["favorites"]
)

config = Config()

@router.put("/handle_favorites",status_code=status.HTTP_200_OK)
async def handle_favorites(request: FavoriteRequest, authorization:str = Header()):
    token = authorization.replace("Bearer: ","")
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        user_id = payload["id"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")
    return await favorites_service.handle_favorites(user_id,request.product_name)


@router.get("/get_user_favorites",status_code=status.HTTP_200_OK)
async def get_user_favorites(authorization: str = Header()):
    token = authorization.replace("Bearer: ", "")
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        user_id = payload["id"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")
    return await favorites_service.get_user_favorites(user_id)