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
    store_id= Column(Integer, ForeignKey("store.store_id"), nullable=False) 
    raw_name= Column(String, nullable=False)
    raw_brand= Column(String, nullable=False)
    raw_size= Column(String, nullable=False)
    raw_price= Column(Integer, nullable=False)
    scrapped_at = Column(DateTime(timezone=True), server_default=func.now())
    matched= Column(Boolean, default=False)

class canonical_item(Base):
    __tablename__="canonical_item"
    canonical_id= Column(Integer, primary_key=True, autoincrement=True)
    product_name= Column(String, nullable=False)
    varient= Column(String)
    size= Column(Integer)
    size_unit= Column(String)

class store_items_table(Base):
    __tablename__="store_items"
    si_id= Column(Integer, primary_key=True, autoincrement=True)
    c_id= Column(Integer, ForeignKey("canonical_item.canonical_id"),nullable=False)
    store_id= Column(Integer, ForeignKey("store.store_id"),nullable=False) 
    raw_id= Column(Integer, ForeignKey(raw_store_table.raw_id),nullable=False)

class price_entry(Base):
    __tablename__="price_entry"
    price_id=Column(Integer, primary_key=True, autoincrement=True)
    si_id= Column(Integer, ForeignKey("store_items.si_id"),nullable=False)
    price= Column(Integer,nullable=False)
    timestamp= Column(DateTime(timezone=True), server_default=func.now())