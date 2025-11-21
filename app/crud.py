from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash, verify_password


def create_user(db: Session, user: schemas.UserCreate):
    
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise ValueError("Email already registered")
    
    
    existing_mobile = db.query(models.User).filter(models.User.mobile_number == user.mobile_number).first()
    if existing_mobile:
        raise ValueError("Mobile number already registered")
    
    try:
        
        db_user = models.User(
            name=user.name,
            email=user.email,
            mobile_number=user.mobile_number,
            password=user.password  
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise e

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    
    
    if user.password != password:
        return False
    return user


def create_category(db: Session, category: schemas.CategoryCreate, user_id: int):
    db_category = models.Category(**category.dict(), user_id=user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, user_id: int):
    return db.query(models.Category).filter(models.Category.user_id == user_id).all()

def get_category(db: Session, category_id: int, user_id: int):
    return db.query(models.Category).filter(
        models.Category.id == category_id, 
        models.Category.user_id == user_id
    ).first()

def delete_category(db: Session, category_id: int, user_id: int):
    category = get_category(db, category_id, user_id)
    if category:
        db.delete(category)
        db.commit()
    return category

def update_category(db: Session, category_id: int, category: schemas.CategoryUpdate, user_id: int):
    db_category = get_category(db, category_id, user_id)
    if db_category:
        update_data = category.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_category, field, value)
        db.commit()
        db.refresh(db_category)
    return db_category





def create_product(db: Session, product: schemas.ProductCreate, user_id: int):
    
    category = get_category(db, product.category_id, user_id)
    if not category:
        return None
    
    db_product = models.Product(**product.dict(), user_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, user_id: int):
    return db.query(models.Product).filter(models.Product.user_id == user_id).all()

def get_product(db: Session, product_id: int, user_id: int):
    return db.query(models.Product).filter(
        models.Product.id == product_id, 
        models.Product.user_id == user_id
    ).first()
    
def delete_product(db: Session, product_id: int, user_id: int):
    product = get_product(db, product_id, user_id)
    if product:
        db.delete(product)
        db.commit()
    return product

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate, user_id: int):
    db_product = get_product(db, product_id, user_id)
    if db_product:
        update_data = product.dict(exclude_unset=True)
        
        
        if 'category_id' in update_data:
            category = get_category(db, update_data['category_id'], user_id)
            if not category:
                return None
        
        for field, value in update_data.items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
    return db_product