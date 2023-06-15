from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Text, Optional

# Init api
app = FastAPI()

# Set model of requests 
class Products(BaseModel):
    url: str

@app.post("/")
def get_product(product : Products):
    return {"url": product.url}
    
