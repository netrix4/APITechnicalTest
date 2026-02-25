from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
from dotenv import load_dotenv

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

def get_current_user():
 pass

# @app.post("/products/" dependencies=[Depends(get_current_user)])
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

@app.get("/products/")
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products