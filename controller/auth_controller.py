from starlette import status

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from exceptions.exception import user_credentials_exception
from model.auth_response import AuthResponse
from model.login_model import LoginModel
from model.register_model import RegisterModel
from model.user_model import User
from service import auth_service, users_service
from utils.security import pwd_context
from config.config import config

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}
)


@router.post("/signup",status_code=status.HTTP_201_CREATED)
async def create_user(user: RegisterModel, response: Response):

    try:
        created_user = await users_service.create_user(user)
        access_token = auth_service.create_access_token(created_user.username, created_user.user_id)
        response.set_cookie(
            key=config.COOKIE_NAME,
            value= access_token.jwt_token,
            httponly=config.COOKIE_HTTPONLY,
            secure=config.COOKIE_SECURE,
            samesite=config.COOKIE_SAMESITE,
            max_age=config.COOKIE_MAX_AGE
        )
        return {"message": "User created successfully"}

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))



@router.post("/login", status_code=status.HTTP_200_OK)
async def login_for_access_token(credentials : LoginModel, response: Response):
    user = await auth_service.authenticate_user(credentials)
    if not user:
        raise user_credentials_exception()
    access_token = auth_service.create_access_token(user.username, user.user_id)
    response.set_cookie(
        key=config.COOKIE_NAME,
        value=access_token.jwt_token,
        httponly=config.COOKIE_HTTPONLY,
        secure=config.COOKIE_SECURE,
        samesite=config.COOKIE_SAMESITE,
        max_age=config.COOKIE_MAX_AGE
    )
    return {"message": "Logged in successfully"}

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response : Response):
    response.delete_cookie(key = config.COOKIE_NAME)
    return {"message":"Logged out successfully!"}


