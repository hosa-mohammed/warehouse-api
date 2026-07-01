from pydantic import BaseModel
from typing import Optional

# Schema for creating a new product
class ProductCreate(BaseModel):
    name: str
    quantity: int
    price: float

# Schema for updating an existing product
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None

# Schema for the response after a product is created/fetched
class ProductResponse(ProductCreate):
    id: int

    class Config:
        # This allows Pydantic to read data from ORM objects
        from_attributes = True
