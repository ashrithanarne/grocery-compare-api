from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from crud.crud_store_items import get_sitems, add_sitems, get_by_id, update_item, delete_item, match_raw_item, relink
import schema
from typing import List

router=APIRouter(prefix="/sitem")

@router.get("/", response_model=List[schema.sitems_res])
def get_sitem(db: Session=Depends(get_db)):
    return get_sitems(db)

@router.post("/", response_model=schema.sitems_res)
def add_s_item(st: schema.sitems_req, db: Session=Depends(get_db)):
    return add_sitems(db,st)

@router.get("/{id}", response_model=schema.sitems_res)
def get_sitem_byid(id: int, db: Session=Depends(get_db)):
    res=get_by_id(db,id);
    if not res:
        raise HTTPException(status_code=404,detail="Store Item not found")
    return res

@router.patch("/{id}",response_model=schema.sitems_res)
def update_sitem(id : int, st: schema.sitems_update_req, db: Session=Depends(get_db)):
    res=update_item(db,id,st)
    if res == "INVALID_C_ID":
        raise HTTPException(status_code=404, detail="canonical_id does not exist")
    if res == "INVALID_STORE_ID":
        raise HTTPException(status_code=404, detail="store_id does not exist")
    if res == "INVALID_RAW_ID":
        raise HTTPException(status_code=404, detail="raw_id does not exist")
    if not res:
        raise HTTPException(status_code=404,detail="Store Item not found")
    return res

@router.delete("/{id}")
def delete_sitem(id: int, db: Session=Depends(get_db)):
    res=delete_item(db,id)
    if res=="HAS_DEPENDENTS":
        raise HTTPException(status_code=409, detail="Cannot be deleted: Store item has price entry linked to it")
    if not res:
        raise HTTPException(status_code=404, detail="Store Item does not exist")
    return {"message": f"Store_item with id {id} has been deleted"}

@router.post("/match/{raw_id}", response_model=schema.sitems_res)
def match_store_item(raw_id: int, st:schema.match_req, db: Session=Depends(get_db)):
    res=match_raw_item(db, raw_id, st.c_id)
    if res == "ALREADY_MATCHED":
        raise HTTPException(status_code=409, detail="This raw item has already been matched")
    if not res:
        raise HTTPException(status_code=404, detail="raw_id not found")
    return res

@router.post('/relink/{raw_id}', response_model=schema.price_res)
def si_relink(raw_id: int, st:schema.relink_req, db: Session=Depends(get_db)):
    res=relink(db, raw_id, st.si_id)
    if res=="SI_NOT_FOUND":
            raise HTTPException(status_code=404, detail="si_id not found")
    if res == "ALREADY_MATCHED":
            raise HTTPException(status_code=409, detail="This raw item has already been matched")
    if not res:
        raise HTTPException(status_code=404, detail="raw_id not found")
    return res