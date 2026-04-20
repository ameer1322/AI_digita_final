
from pydantic import BaseModel

class UserResponse(BaseModel):
    user_id: int
    first_name:str
    last_name:str
    age:int
    email:str
    phone:str
    address:str
    username:str
    hashed_password:str
