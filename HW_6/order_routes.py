from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from HW_6.market_db import database, users, products, orders
from datetime import datetime
from typing import List

router = APIRouter()


class OrderIn(BaseModel):
    date: datetime = Field(default=datetime.now(), tittle="Order_Date")
    status: bool = Field(default=False, tittle="Order_Status")


class Order(BaseModel):
    date: datetime = Field(..., tittle="Order_Date")
    status: bool = Field(default=False, tittle="Order_Status")


@router.post("/new_order/")
async def create_order(order: OrderIn, user_id: int, product_id: int):
    """
      Create a new order.
    """
    # Проверка существования пользователя и продукта
    user_exists_query = users.select().where(users.c.id == user_id)
    product_exists_query = products.select().where(products.c.id == product_id)

    user_exists_result = await database.fetch_one(user_exists_query)
    product_exists_result = await database.fetch_one(product_exists_query)

    if user_exists_result is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} does not exist")

    if product_exists_result is None:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} does not exist")

    # Создание нового заказа
    current_time = datetime.now()
    query = orders.insert().values(
        user_id=user_id,
        product_id=product_id,
        date=current_time,
        status=order.status
    )
    last_record_id = await database.execute(query)
    return {
        "id": last_record_id,
        "user_id": user_id,
        "product_id": product_id,
        "date": current_time,
        "status": order.status
    }


@router.get("/orders/", response_model=List[Order])
async def get_orders():
    """
    Get all orders.
    """
    query = orders.select()
    return await database.fetch_all(query)


@router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int):
    """
    Get a single order by ID.
    """
    query = orders.select().where(orders.c.id == order_id)
    order = await database.fetch_one(query)
    if order is None:
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")
    return order


@router.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, order: OrderIn):
    """
    Update an order by ID.
    """
    query = orders.update().where(orders.c.id == order_id).values(
        date=order.date,
        status=order.status
    )
    await database.execute(query)
    return {**order.dict(), "id": order_id}


@router.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    """
    Delete an order by ID.
    """
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {"message": f"Order with ID {order_id} deleted successfully"}
