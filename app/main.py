import json
import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
from dotenv import load_dotenv
from auth import auth_scheme
import http.client

load_dotenv()
app = FastAPI()

@app.get("/")
def main():
    return {"message": "Hi from FastAPI!"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products/" )
def create_product(name: str, description: str, price: float, db: Session = Depends(get_db)):
    new_product = models.Product(name=name, description=description, price=price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Protected endpoint
@app.get("/products/")
def get_products(db: Session = Depends(get_db) ,user: dict = Depends(auth_scheme)):
    products = db.query(models.Product).all()
    return products

@app.get("/get-token/")
def get_token(db: Session = Depends(get_db)):
    conn = http.client.HTTPSConnection(os.getenv('AUTH0_DOMAIN'))
    client_id = os.getenv('AUTH0_CLIENT_ID')
    client_secret = os.getenv('AUTH0_CLIENT_SECRET')
    audience = os.getenv('AUTH0_AUDIENCE')

    payload = {"client_id" :client_id, 'client_secret': client_secret, 'audience': audience, 'grant_type': 'client_credentials'}
    payload = json.dumps( payload)
    headers = { 'content-type': "application/json" }
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")