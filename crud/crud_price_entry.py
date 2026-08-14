from sqlalchemy.orm import Session
from models import price_entry,store_items_table
import schema

def get_all_prices(db: Session):
    return db.query(price_entry).all()

def add_new_price(db: Session, st: schema.price_req):
    store_item=db.query(store_items_table).filter(store_items_table.si_id==st.si_id).first()
    if not store_item:
        return None
    new_item=price_entry(**st.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def get_price(db: Session, id: int):
    res=db.query(price_entry).filter(price_entry.price_id==id).first()
    if not res:
        return None
    return res

def update_price(db: Session, id: int, st: schema.price_update):
    item=db.query(price_entry).filter(price_entry.price_id==id).first()
    if not item:
        return None

    update_data = st.model_dump(exclude_unset=True)

    if "si_id" in update_data:
        store_item = db.query(store_items_table).filter(store_items_table.si_id == update_data["si_id"]).first()
        if not store_item:
            return "Invalid si_id"
        
    for key, value in update_data.items():
        setattr(item,key,value)

    db.commit()
    db.refresh(item)
    return item    

def delete_price(db:Session, id:int):
    item=db.query(price_entry).filter(price_entry.price_id==id).first()
    if not item:
        return None
    db.delete(item)
    db.commit()
    return item

def latest_price(db:Session, si_id:int):
    si_item = db.query(store_items_table).filter(store_items_table.si_id == si_id).first()
    if not si_item:
        return "Invalid si_id   "

    latest = (
        db.query(price_entry)
        .filter(price_entry.si_id == si_id)
        .order_by(price_entry.timestamp.desc())
        .first()
    )
    return latest