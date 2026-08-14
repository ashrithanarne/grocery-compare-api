from sqlalchemy.orm import Session
from models import canonical_item
import schema

def add_canonicalitem(db: Session,st: schema.canonical_req):
    new_entry=canonical_item(**st.model_dump())
    existing=db.query(canonical_item).filter(canonical_item.product_name==st.product_name, canonical_item.varient==st.varient, canonical_item.size==st.size, canonical_item.size_unit==st.size_unit).first()
    if existing:
        return None
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

def get_all_citems(db: Session):
    return db.query(canonical_item).all()

def fetch_citem_by_id(id: int, db: Session):
    return db.query(canonical_item).filter(canonical_item.canonical_id==id).first()

def update_citem(db: Session, id: int, st: schema.update_canonical_req):
    item=db.query(canonical_item).filter(canonical_item.canonical_id==id).first()
    if not item:
        return None
    update_data=st.model_dump(exclude_unset=True)
    for key,value in update_data.items():
        setattr(item,key,value)

    db.commit()
    db.refresh(item)
    return item

def delte_c_item(db: Session, id:int):
    item=db.query(canonical_item).filter(canonical_item.canonical_id==id).first()
    if not item:
        return None
    db.delete(item)
    db.commit()
    return item