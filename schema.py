from typing import Optional
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class item_request(BaseModel):
    name: str =Field(min_length=2, max_length=50)

class item_response(BaseModel):
    name: str =Field(min_length=2, max_length=50)
    price: Optional[int] = None

class count_return(BaseModel):
    count:int =Field(ge=0)

# Store schema
class store_request(BaseModel):
    name: str =Field(min_length=2, max_length=50)

class store_response(BaseModel):
    id: int =Field(gt=0, alias="store_id")
    name: str = Field(alias="store_name")
    class Config:
        from_attributes = True

class store_update_req(BaseModel):
    name: Optional[str]=None

# Store items schema
class raw_item_req(BaseModel):
    store_id: int
    raw_name: str =Field(min_length=2, max_length=50)
    raw_brand: str
    raw_size: str
    raw_price: int= Field(gt=0)

class raw_item_res(BaseModel):
    raw_id: int
    store_id: int
    raw_name: str
    raw_brand: str
    raw_size: str
    raw_price: int
    scrapped_at: datetime
    matched: bool

    class Config:
        from_attributes= True

class raw_item_update_req(BaseModel):
    store_id: Optional[int]= None
    raw_name: Optional[str]= None
    raw_brand: Optional[str]= None
    raw_size: Optional[str]= None
    raw_price: Optional[int]= None

#Canonical items schema definitions
class canonical_req(BaseModel):
    product_name: str
    varient: Optional[str]=None
    size: Optional[int] = Field(default=None, gt=0)
    size_unit: Optional[str]=None

class canonical_res(BaseModel):
    canonical_id:int
    product_name: str
    varient: str
    size: int
    size_unit: str
    
    class Config:
        from_attributes= True

class update_canonical_req(BaseModel):
    product_name: Optional[str]=None
    varient: Optional[str]=None
    size: Optional[int]=None
    size_unit: Optional[str]=None

#Store items table schema

class sitems_req(BaseModel):
    c_id: int
    store_id: int
    raw_id: int

class sitems_res(BaseModel):
    si_id: int
    c_id: int
    store_id: int
    raw_id: int

class sitems_update_req(BaseModel):
    c_id: Optional[int]=None
    store_id: Optional[int]=None
    raw_id: Optional[int]=None

class match_req(BaseModel):
    c_id: int

class relink_req(BaseModel):
    si_id: int

#price_entry schema
class price_res(BaseModel):
    price_id: int
    si_id: int
    price: int
    timestamp: datetime

class price_req(BaseModel):
    si_id: int
    price: int =Field(gt=0)

class price_update(BaseModel):
    si_id: Optional[int]=None
    price: Optional[int] = Field(default=None, gt=0)