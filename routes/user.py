from fastapi import APIRouter, Response
from config.db import conn
from schemas.user import userEntity, usersEntity
from models.user import User
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT, HTTP_202_ACCEPTED

user = APIRouter()


@user.get('/users')
def get_users():
    return usersEntity(conn.local.user.find())

@user.get('/users/{id}')
def find_user(id: str):
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))

@user.delete('/users/{id}')
def delete_user(id: str):
    userEntity(conn.local.user.find_one_and_delete({"_id": ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)
@user.post('/users')
def create_user(user: User):
    new_user = dict(user)
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])
    del new_user["id"]
    id = conn.local.user.insert_one(new_user).inserted_id

    user = conn.local.user.find_one({"_id":id})
    return userEntity(user)

