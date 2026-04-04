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

def update_raw_item(db:Session, id:int, st: schema.raw_item_update_req):
    item=db.query(raw_store_table).filter(raw_store_table.raw_id==id).first()
    if not item:
        return None
    #exclde_unset=True, makes it such that only the keys given by the user is updated , the rest remain unchanged
    #items() is a python dictionary method, and it returns key-value pairs
    update_data=st.model_dump(exclude_unset=True)
    for key,value in update_data.items():
        setattr(item,key,value)
    
    db.commit()
    db.refresh(item)
    return item

def del_item_by_id(db:Session, id:int):
    item=db.query(raw_store_table).filter(raw_store_table.raw_id==id).first()
    if not item:
        return None
    db.delete(item)
    db.commit()
    return item