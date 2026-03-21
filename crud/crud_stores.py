from sqlalchemy.orm import Session

from database import SessionLocal
from models import Stores
import schema



def get_all_stores(db: Session):
    return db.query(Stores).all()

def add_store(db: Session, st: schema.store_request):
    new_store=Stores(store_name= st.name)
    db.add(new_store)
    db.commit()
    db.refresh(new_store)
    return new_store

def get_store(db:Session, id:int):
    store= db.query(Stores).filter(Stores.store_id == id).first()
    if not store:
        return None
    return store

def del_store(db:Session, id: int):
    store= db.query(Stores).filter(Stores.store_id == id).first()
    if not store:
        return None
    
    db.delete(store)
    db.commit()
    return store