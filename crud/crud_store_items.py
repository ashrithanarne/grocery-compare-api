from sqlalchemy.orm import Session
from models import store_items_table, raw_store_table, price_entry, canonical_item, Stores
import schema

def get_sitems(db: Session):
    return db.query(store_items_table).all()

def add_sitems(db: Session, st: schema.sitems_req):
    new_s_item=store_items_table(**st.model_dump())
    db.add(new_s_item)
    db.commit()
    db.refresh(new_s_item)
    return new_s_item

def get_by_id(db: Session, id: int):
    res=db.query(store_items_table).filter(store_items_table.si_id == id).first()
    if not res:
        return None
    return res

def update_item(db: Session,id: int,st: schema.sitems_update_req):
    res=db.query(store_items_table).filter(store_items_table.si_id == id).first()
    if not res:
        return None
    update_data=st.model_dump(exclude_unset=True)

    if "c_id" in update_data:
        exists = db.query(canonical_item).filter(canonical_item.canonical_id == update_data["c_id"]).first()
        if not exists:
            return "INVALID_C_ID"

    if "store_id" in update_data:
        exists = db.query(Stores).filter(Stores.store_id == update_data["store_id"]).first()
        if not exists:
            return "INVALID_STORE_ID"

    if "raw_id" in update_data:
        exists = db.query(raw_store_table).filter(raw_store_table.raw_id == update_data["raw_id"]).first()
        if not exists:
            return "INVALID_RAW_ID"
        
    for key,val in update_data.items():
        setattr(res,key,val)

    db.commit()
    db.refresh(res)
    return res

def delete_item(db: Session,id:int):
    item=db.query(store_items_table).filter(store_items_table.si_id == id).first()
    if not item:
        return None

    has_price_entry=db.query(price_entry).filter(price_entry.si_id==id).first()
    if has_price_entry:
        return "HAS_DEPENDENTS"
    db.delete(item)
    db.commit()
    return True

def match_raw_item(db: Session, raw_id: int, c_id: int):
    raw_item = db.query(raw_store_table).filter(raw_store_table.raw_id == raw_id).first()
    if not raw_item:
        return None
    
    if raw_item.matched:
        return "ALREADY_MATCHED"

    new_s_item = store_items_table(
        c_id=c_id,
        store_id=raw_item.store_id,
        raw_id=raw_item.raw_id
    )
    db.add(new_s_item)

    raw_item.matched = True

    db.commit()
    db.refresh(new_s_item)

    new_price_entry=price_entry(
        si_id=new_s_item.si_id,
        price=raw_item.raw_price
    )
    db.add(new_price_entry)
    db.commit()
    db.refresh(new_price_entry)
    return new_s_item

def relink(db: Session, raw_id: int, si_id: int):
    raw_item = db.query(raw_store_table).filter(raw_store_table.raw_id == raw_id).first()
    if not raw_item:
        return None

    if raw_item.matched:
        return "ALREADY_MATCHED"

    si_item = db.query(store_items_table).filter(store_items_table.si_id == si_id).first()
    if not si_item:
        return "SI_NOT_FOUND"
    
    new_price_entry=price_entry(
            si_id=si_id,
            price=raw_item.raw_price
        )
    db.add(new_price_entry)
    raw_item.matched = True
    db.commit()
    db.refresh(new_price_entry)
    return new_price_entry