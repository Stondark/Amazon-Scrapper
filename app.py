from fastapi import FastAPI
from schema import ProductsModel
from controllers.scrapper import Scrapper 

# Init api
app = FastAPI()

@app.post("/product")
def get_product(product: ProductsModel):
    try:
        product_scrapp = Scrapper(product.url)
        return product_scrapp.scrape_product_info()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
