from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    mobile_number: str
    
class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if len(v) > 128:  # Reasonable character limit
            raise ValueError('Password must be less than 128 characters')
        return v
    
class UserOut(UserBase):
    id: int
    
    class Config:
        from_attributes = True
        
# ... rest of your schemas remain the same ...
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    
class TokenData(BaseModel):
    user_id: Optional[int]=None

class CategoryBase(BaseModel):
    name: str
    description: str | None = None  
    
class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int
    user_id:int
    class Config:
        from_attributes = True
        
class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
        
        
class ProductBase(BaseModel):
    name: str
    price: float
    category_id: int
    
class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True
        
class ProductUpdate(BaseModel):
    name: str| None = None
    price: float | None = None
    category_id: int | None = None