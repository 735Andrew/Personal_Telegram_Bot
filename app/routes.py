from fastapi import APIRouter, HTTPException
from app.models import UserSchema, LogInSchema
from app.data.user import user_create, get_one
from app.errors import Missing, Duplicate
from typing import Dict
from passlib.context import CryptContext


router = APIRouter(prefix="/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/sign_up", status_code=201)
def user_sign_up(user: UserSchema) -> UserSchema:
    try:
        user.password = pwd_context.hash(user.password)
        return user_create(user)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("/log_in")
def user_log_in(user: LogInSchema) -> Dict:
    try:
        user = get_one(user)
        return {"access_token": "12345"}
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.get("/bot_creation")
def user_create_bot(): ...  # todo write ENDPOINT
