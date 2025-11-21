from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas
from ..auth import get_current_user
from ..models import User

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    created_product=crud.create_product(db=db, product=product,user_id=current_user.id)
    if not created_product:
        raise HTTPException(status_code=400, detail="Category not found or doesn't belong to you")
    return created_product

@router.get("/", response_model=list[schemas.ProductOut])
def read_products(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return crud.get_products(db=db, user_id=current_user.id)

@router.get("/{product_id}", response_model=schemas.ProductOut)
def read_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = crud.get_product(db=db, product_id=product_id,user_id=current_user.id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(
    product_id: int, 
    product: schemas.ProductUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_product = crud.update_product(db=db, product_id=product_id, product=product, user_id=current_user.id)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found or category doesn't belong to you")
    return updated_product

@router.patch("/{product_id}", response_model=schemas.ProductOut)
def partial_update_product(
    product_id: int, 
    product: schemas.ProductUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_product = crud.update_product(db=db, product_id=product_id, product=product, user_id=current_user.id)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found or category doesn't belong to you")
    return updated_product


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    deleted = crud.delete_product(db=db, product_id=product_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}