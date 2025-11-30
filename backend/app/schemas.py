from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Product schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    category: Optional[str] = None
    stock: int = 0

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    rating: float
    review_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Cart schemas
class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemCreate(CartItemBase):
    pass

class CartItemResponse(CartItemBase):
    id: int
    user_id: int
    product: ProductResponse
    created_at: datetime
    
    class Config:
        from_attributes = True

# Order schemas
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderItemResponse(OrderItemBase):
    id: int
    product: ProductResponse
    
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    shipping_address: str

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    user_id: int
    total_amount: float
    status: str
    created_at: datetime
    order_items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

