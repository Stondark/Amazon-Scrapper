from pydantic import BaseModel
from typing import Text
# Set model of requests 
class ProductsModel(BaseModel):
    url: str