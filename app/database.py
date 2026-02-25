# from sqlalchemy import create_client
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# URL de la base de datos SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///../apiData.db"

# El argumento 'check_same_thread' es necesario solo para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()