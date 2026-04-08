from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
import schema
from crud.crud_connonical_items import add_cannonicalitem, get_all_citems, fetch_citem_by_id
from typing import List

router=APIRouter(prefix="/cannonical")

@router.post("/", response_model=schema.cannonical_res)
def create_cannonical_item(st:schema.cannonical_req, db: Session=Depends(get_db)):
    return add_cannonicalitem(db,st)

@router.get("/",response_model=List[schema.cannonical_res])
def get_all_cannpnical_items(db: Session =Depends(get_db)):
    return get_all_citems(db)

@router.get("/{id}", response_model=schema.cannonical_res)
def get_citem_by_id(id: int, db: Session = Depends(get_db)):
    res=fetch_citem_by_id(id,db)
    if not res:
        raise HTTPException(status_code=400, detail="Item does not exist")
    return res