import uvicorn as uvicorn
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import logging
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


user_1 = User(id=0, name='name_0', email='mail_0', password='password_0')
user_2 = User(id=1, name='name_1', email='mail_1', password='password_1')
user_3 = User(id=2, name='name_2', email='mail_2', password='password_2')

users = [user_1, user_2, user_3]


@app.get('/users')
async def get_users():
    logger.info('Обработан запрос для users')
    return users


@app.post('/users/')
def create_user(user: User):
    users.append(user)
    logger.info('Отработал POST запрос')
    return user


@app.put('/users/{id_users}')
def update_user(id_users: int, user: User):
    for i in range(len(users)):
        if users[i].id == id_users:
            users[i] = user
    logger.info('Отработал PUT запрос')
    return user


@app.delete('/users/{id_users}')
def delete_user(id_users: int):
    for i in range(len(users)):
        if users[i].id == id_users:
            logger.info('Отработал DELETE запрос')
            return {'id_users': users.pop(i)}
        return HTTPException(status_code=404, detail="Movies not found")


@app.get("/users/", response_class=HTMLResponse)
async def read_users(request: Request):
    logger.info('Обработан запрос для users')
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


if __name__ == '__main__':
    uvicorn.run('task_01:app', port=8000)
