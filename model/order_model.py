import datetime

from pydantic import BaseModel

class Order(BaseModel):
    user_id : int
    item_id : int
    quantity: int