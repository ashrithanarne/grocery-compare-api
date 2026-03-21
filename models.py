from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Boolean
from datetime import datetime
from database import Base

class Stores(Base):
    __tablename__="store"
    store_id= Column(Integer, primary_key=True)
    store_name=Column(String, nullable=False)

class raw_store_table(Base):
    __tablename__="raw_store_table"
    raw_id= Column(Integer, primary_key=True, autoincrement=True)
    store_id= Column(Integer, ForeignKey("store.store_id")) 
    raw_name= Column(String)
    raw_brand= Column(String)
    raw_size= Column(String)
    raw_price= Column(Integer)
    scrapped_at = Column(DateTime(timezone=True), server_default=func.now())
    matched= Column(Boolean, default=False)