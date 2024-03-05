from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from HW_6.market_db import database, products
from typing import Annotated, List

router = APIRouter()


class ProductIn(BaseModel):
    title: str = Field(..., tittle="Product_Name", max_length=100)
    description: str = Field(default=None, title="Product_Description", max_length=1000)
    price: float = Field(..., tittle="Price", ge=0, le=100000)


class Product(BaseModel):
    id: int
    title: str = Field(..., tittle="Product_Name", max_length=100)
    description: str = Field(default=None, title="Product_Description", max_length=1000)
    price: float = Field(..., tittle="Price", ge=0, le=100000)


@router.post("/new_product/")
async def create_product(product: Annotated[ProductIn, Depends()]):
    """
        Create a new product.
    """
    query = products.insert().values(**product.dict())
    last_record_id = await database.execute(query)
    return {**product.dict(), "id": last_record_id}


@router.get("/products/", response_model=List[Product])
async def get_products():
    """
    Get all products.
    """
    query = products.select()
    return await database.fetch_all(query)


@router.get("/product/{product_id}", response_model=Product)
async def get_product(product_id: int):
    """
    Get a single product by its ID.
    """
    query = products.select().where(products.c.id == product_id)
    product = await database.fetch_one(query)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/product/{product_id}")
async def update_product(product_id: int, product: ProductIn):
    """
    Update a product by its ID.
    """
    query = products.update().where(products.c.id == product_id).values(**product.dict())
    await database.execute(query)
    return {"message": "Product updated successfully"}


@router.delete("/product/{product_id}")
async def delete_product(product_id: int):
    """
    Delete a product by its ID.
    """
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {"message": "Product deleted successfully"}
