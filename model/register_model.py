from pydantic import BaseModel

class RegisterModel(BaseModel):
    first_name:str
    last_name:str
    age:int
    email:str
    phone:str
    address:str
    username:str
    password:str
