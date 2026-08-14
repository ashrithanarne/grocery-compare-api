import uvicorn
from fastapi import FastAPI
from database import engine
from models import Base
from routers import router_raw_items, router_stores,router_canonical_items, router_store_items, router_price_entry
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
app.include_router(router_raw_items.router)
app.include_router(router_canonical_items.router)
app.include_router(router_store_items.router)
app.include_router(router_price_entry.router)
