from typing import List, Optional, Annotated
from fastapi import FastAPI, HTTPException, status, Depends, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="../HW/HW_5/templates")


# Модель пользователь
class User(BaseModel):
    id: int
    name: str
    email: Optional[str]
    password: str


# База данных (список) для хранения пользователей
users_db = []


@app.get('/')
async def index():
    return RedirectResponse("/users")


# Конечная точка для получения списка всех пользователей
@app.get("/users", response_class=HTMLResponse, response_model=List[User])
async def get_users(request: Request):
    title = "Список пользователей"
    return templates.TemplateResponse("users.html", {"request": request, "users": users_db, "title": title})


# Конечная точка для получения пользователя по ID
@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    if user_id < 0 or user_id >= len(users_db):
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]


# Конечная точка для создания нового пользователя
@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: Annotated[User, Depends()]):
    users_db.append(user)
    return user


# Конечная точка для обновления пользователя по ID
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: Annotated[User, Depends()]):
    if user_id < 0 or user_id >= len(users_db):
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id] = user
    return user


# Конечная точка для удаления пользователя по ID
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    if user_id < 0 or user_id >= len(users_db):
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
