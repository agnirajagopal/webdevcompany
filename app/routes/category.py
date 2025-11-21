from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas
from ..auth import get_current_user
from ..models import User

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=schemas.CategoryOut)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_category(db=db, category=category, user_id=current_user.id)

@router.get("/", response_model=list[schemas.CategoryOut])
def read_categories(db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    return crud.get_categories(db=db, user_id=current_user.id)

@router.get("/{category_id}", response_model=schemas.CategoryOut)
def read_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    category = crud.get_category(db=db, category_id=category_id,user_id=current_user.id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=schemas.CategoryOut)
def update_category(
    category_id: int,
    category: schemas.CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_category = crud.update_category(db=db, category_id=category_id, category=category, user_id=current_user.id)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

@router.patch("/{category_id}", response_model=schemas.CategoryOut)
def partial_update_category(
    category_id: int,
    category: schemas.CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_category = crud.update_category(db=db, category_id=category_id, category=category, user_id=current_user.id)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), current_user:User=Depends(get_current_user)):
    deleted = crud.delete_category(db=db, category_id=category_id,user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted"}