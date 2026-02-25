from fastapi import FastAPI
from fastapi import FastAPI
from pydantic import BaseModel

from models import Product

app = FastAPI()

@app.get("/")
def main():
    return {"message": "Hi from FastAPI!"}

@app.get("/products/")
def get_products():
    return {"message": "Hi, these are the products"}

@app.post("/products/")
def create_product(product: Product):
    return {"status": "Recibido", "data": product}