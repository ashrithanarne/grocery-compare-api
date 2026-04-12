from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
import schema
from crud.crud_cononical_items import add_canonicalitem, get_all_citems, fetch_citem_by_id, update_citem,delte_c_item
from typing import List

router=APIRouter(prefix="/canonical")

@router.post("/", response_model=schema.canonical_res)
def create_canonical_item(st:schema.canonical_req, db: Session=Depends(get_db)):
    return add_canonicalitem(db,st)

@router.get("/",response_model=List[schema.canonical_res])
def get_all_canpnical_items(db: Session =Depends(get_db)):
    return get_all_citems(db)

@router.get("/{id}", response_model=schema.canonical_res)
def get_citem_by_id(id: int, db: Session = Depends(get_db)):
    res=fetch_citem_by_id(id,db)
    if not res:
        raise HTTPException(status_code=400, detail="Item does not exist")
    return res

@router.patch("/{id}",response_model=schema.canonical_res)
def update_canonical_item(st:schema.update_canonical_req,id: int, db: Session=Depends(get_db)):
    res=update_citem(db,id,st)
    if not res:
        return HTTPException(status_code=404, detail="Item not found")
    return res

@router.delete("/{id}")
def delete_canonical_item(id:int, db: Session = Depends(get_db)):
    res=  delte_c_item(db,id)
    if not res:
        return HTTPException(status_code=404, detail="Item not found")
    return {"message":f"Item with id {id} has been deleted"}