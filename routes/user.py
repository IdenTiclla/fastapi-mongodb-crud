from fastapi import APIRouter
from config.db import conn
from schemas.user import userEntity, usersEntity
from models.user import User

user = APIRouter()


@user.get('/users')
def get_users():
    return usersEntity(conn.local.user.find())

@user.post('/users')
def create_user(user: User):
    new_user = dict(user)
    del new_user["id"]
    id = conn.local.user.insert_one(new_user).inserted_id

    user = conn.local.user.find_one({"_id":id})
    return userEntity(user)

