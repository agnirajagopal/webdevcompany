from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routes import category, product


from app.models import Category, Product


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Category & Product API")

app.include_router(category.router)
app.include_router(product.router)

@app.get("/")
def read_root():
    return {"message": "Category & Product API is running"}