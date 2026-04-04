from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud.crud_items import get_all_items, add_raw_item, del_item_by_id, get_item_by_id, update_raw_item
import schema
from typing import List

router=APIRouter(prefix="/items")

@router.get("/", response_model=List[schema.raw_item_res])
def get_items(db: Session = Depends(get_db)):
    return get_all_items(db)

@router.post("/", response_model=schema.raw_item_res)
def create_raw_item(st:schema.raw_item_req, db: Session = Depends(get_db)):
    return add_raw_item(db,st)

@router.get("/{id}", response_model=schema.raw_item_res)
def fetch_item_by_id(id:int, db:Session=Depends(get_db)):
    res=get_item_by_id(db,id)
    if not res:
        raise HTTPException(status_code=404, detail="Item does not exist")
    return res

@router.patch("/{id}", response_model=schema.raw_item_res)
def update_item(id:int, st:schema.raw_item_update_req, db: Session=Depends(get_db)):
    res=update_raw_item(db,id,st)
    if not res:
        raise HTTPException(status_code=404, detail="Item not found")
    return res

@router.delete("/{id}")
def delete_item_by_id(id:int, db:Session=Depends(get_db)):
    res=del_item_by_id(db,id)
    if not res:
        raise HTTPException(status_code=404, detail="Item Not Found")
    return {"message": f"Item with id {id} has been deleted"}