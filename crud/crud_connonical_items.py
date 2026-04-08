from sqlalchemy.orm import Session
from models import cannonical_item
import schema

def add_cannonicalitem(db: Session,st: schema.cannonical_req):
    new_entry=cannonical_item(**st.model_dump())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

def get_all_citems(db: Session):
    return db.query(cannonical_item).all()

def fetch_citem_by_id(id: int, db: Session):
    return db.query(cannonical_item).filter(cannonical_item.cannonical_id==id).first()