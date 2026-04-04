from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.crud_stores import get_all_stores, add_store, get_store,del_store,store_update
from database import get_db
import schema
from typing import List

router=APIRouter(prefix="/stores")

@router.get("/", response_model=List[schema.store_response])
def get_stores(db: Session = Depends(get_db)):
    return get_all_stores(db)

@router.post("/", response_model=schema.store_response)
def create_store(st: schema.store_request, db: Session = Depends(get_db)):
    return add_store(db,st)

@router.get("/{id}", response_model=schema.store_response)
def get_store_by_id(id: int, db: Session= Depends(get_db)):
    res= get_store(db,id)
    if not res:
        raise HTTPException(status_code=404, detail="Store not found")
    return res

@router.patch("/{id}", response_model=schema.store_response)
def update_store_by_id(id:int, st:schema.store_update_req, db:Session=Depends(get_db)):
    res=store_update(db,id,st)
    if res is None:
        raise HTTPException(status_code=404, detail="Store not found")
    if res=="Empty update":
        raise HTTPException(status_code=400, detail="No fields provided to update")

    return res

@router.delete("/{id}")
def delete_store(id:int, db:Session =Depends(get_db)):
    res=del_store(db,id)
    if not res:
        raise HTTPException(status_code=404, detail="Store not found")
    return {"message", f"Store with id {id} has been deleted"}

