from sqlalchemy.orm import Session
import uvicorn
from fastapi import FastAPI
#from typing import List 
#from pydantic import BaseModel
from database import engine,SessionLocal
from models import Base
from routers import router_stores,router_items, router_canonical_items
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app=FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_stores.router)
app.include_router(router_items.router)
app.include_router(router_canonical_items.router)
