from pydantic import BaseModel

class FavoriteRequest(BaseModel):
    product_name:str