from sqlalchemy.orm import Session
import uvicorn
from fastapi import Body, Depends, FastAPI, HTTPException
#from typing import List 
#from pydantic import BaseModel
import schema
from typing import List
from database import engine,SessionLocal
from models import Base
from routers import router_stores,router_items

Base.metadata.create_all(bind=engine)
app=FastAPI()

app.include_router(router_stores.router)
app.include_router(router_items.router)
