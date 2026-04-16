
from pydantic import BaseSettings

class LoginModel(BaseSettings):
    username:str
    password:str