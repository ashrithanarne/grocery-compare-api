from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Database_url="sqlite:///./test.db"

engine= create_engine(Database_url)

SessionLocal= sessionmaker(bind=engine)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()