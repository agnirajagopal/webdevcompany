from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str | None = None  
    
class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int
    class Config:
        from_attributes = True
        
        
class ProductBase(BaseModel):
    name: str
    price: float
    category_id: int
    
class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    class Config:
        from_attributes = True