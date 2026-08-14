from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from crud.crud_price_entry import get_all_prices,add_new_price, get_price, update_price,delete_price,latest_price
import schema
from typing import List

router=APIRouter(prefix="/price")

@router.get("/", response_model=List[schema.price_res])
def getAllPrices(db: Session =Depends(get_db)):
    return get_all_prices(db)

@router.post("/",response_model=schema.price_res)
def addNewPriceEntry(st: schema.price_req, db: Session=Depends(get_db)):
    res=add_new_price(db,st)
    if not res:
         raise HTTPException(status_code=404, detail="Store_item ID not found")
    return res

@router.get("/{id}",response_model=schema.price_res)
def getPrice(id: int, db: Session=Depends(get_db) ):
    res=get_price(db,id)
    if not res:
        raise HTTPException(status_code=404, detail="Price ID not found")
    return res

@router.patch("/{id}",response_model=schema.price_res)
def updatePrice(id: int, st: schema.price_update, db: Session=Depends(get_db)):
    res=update_price(db,id,st)
    if res=="Invalid si_id":
        raise HTTPException(status_code=400, detail="Given si_id does not exist")
    if not res:
        raise HTTPException(status_code=404, detail="Price ID not found")
    return res

@router.delete("/{id}")
def deletePrice(id: int, db:Session=Depends(get_db)):
    res=delete_price(db,id)
    if not res:
        raise HTTPException(status_code=404, detail="Price ID not found")
    return {f"Price with Id {id} has been deleted"}

@router.get("/latest/{si_id}",response_model=schema.price_res)
def latestPrice(si_id: int, db:Session=Depends(get_db)):
    res=latest_price(db,si_id)
    if res=="Invalid si_id":
        raise HTTPException(status_code=404, detail="si_id does not exist")
    if not res:
        raise HTTPException(status_code=404, detail="Price does not exist for given si_id")
    return res
