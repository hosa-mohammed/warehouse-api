from pydantic import BaseModel
from typing import List, Optional


# --- Product Schemas ---
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 0
    category_id: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    category_id: Optional[int] = None

class ProductResponse(ProductCreate):
    id: int
    class Config:
        from_attributes = True


# --- Category Schemas ---
class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: Optional[str] = None

class CategoryResponse(CategoryCreate):
    id: int
    products: List[ProductResponse] = []
    class Config:
        from_attributes = True


# --- Order Schemas ---
class OrderItem(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    customer_name: str
    items: List[OrderItem]

class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None

class OrderResponse(OrderUpdate):
    id: int
    total_price: float
    products: List[ProductResponse] = []
    class Config:
        from_attributes = True


# --- User Schemas ---
class UserCreate(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str


# --- Auth / Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None