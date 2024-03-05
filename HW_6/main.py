from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from HW_6.user_routes import router as user_router
from HW_6.product_routes import router as product_router
from HW_6.order_routes import router as order_router
from HW_6.market_db import database

app = FastAPI()

app.include_router(user_router, prefix="/user")
app.include_router(product_router, prefix="/product")
app.include_router(order_router, prefix="/order")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Глобальная обработка ошибок
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )
