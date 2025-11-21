from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name=Column(String,nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    mobile_number=Column(String,unique=True, index=True, nullable=False)
    password=Column(String, nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    
    categories = relationship("Category", back_populates='owner',cascade='all,delete')
    products=relationship("Product",back_populates='owner',cascade='all, delete')

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    user_id=Column(Integer, ForeignKey("users.id"),nullable=False)
    
    owner = relationship("User", back_populates="Categories")
    products = relationship("Product", back_populates="category", cascade="all, delete")
    
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))
    user_id=Column(Integer, ForeignKey("users.id"), nullable=False)
    
    
    category = relationship("Category", back_populates="products")
    owner = relationship("User", back_populates="products")