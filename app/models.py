from sqlalchemy import Column, Integer, String, Numeric
from database import Base

class Product(Base):
    __tablename__ = "Product"

    id = Column(Integer, nullable=False, unique=True, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Numeric)
