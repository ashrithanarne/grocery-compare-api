from sqlalchemy.orm import Session
from models import raw_store_table
import schema

def get_all_items(db: Session):
    return db.query(raw_store_table).all()

def get_item_by_id(db: Session, id:int):
    item=db.query(raw_store_table).filter(raw_store_table.raw_id==id).first()
    if not item:
        return None
    return item

def add_raw_item(db: Session, st:schema.raw_item_req):
    try:

        new_item=raw_store_table(**st.model_dump())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except Exception as e:
        db.rollback()
        raise e

def del_item_by_id(db:Session, id:int):
    item=db.query(raw_store_table).filter(raw_store_table.raw_id==id).first()
    if not item:
        return None
    db.delete(item)
    db.commit()
    return item