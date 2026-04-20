from starlette import status

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from exceptions.exception import user_credentials_exception
from model.auth_response import AuthResponse
from model.login_model import LoginModel
from model.register_model import RegisterModel
from model.user_model import User
from service import auth_service, users_service
from service.auth_service import authenticate_user, create_access_token
from utils.security import pwd_context

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}
)


@router.post("/signup",status_code=status.HTTP_201_CREATED)
async def create_user(user: RegisterModel):
    hashed_password = pwd_context.hash(user.password)
    hashed_user=User(
        first_name=user.first_name,
        last_name=user.last_name,
        age=user.age,
        email=user.email,
        phone=user.phone,
        address=user.address,
        username=user.username,
        hashed_password=hashed_password
    )

    try:
        return await users_service.create_user(hashed_user)
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))



@router.post("/login", status_code=status.HTTP_200_OK, response_model=AuthResponse)
async def login_for_access_token(credentials : LoginModel):
    user = await auth_service.authenticate_user(credentials)
    if not user:
        raise user_credentials_exception()
    return auth_service.create_access_token(user.username, user.user_id)



