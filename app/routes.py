from fastapi import APIRouter, HTTPException, Header
from app.models import UserSchema, LogInSchema, BotTokenSchema
from app.data.user import user_create, get_one, check_token_validity
from app.errors import Missing, Duplicate
from app.bot import main
from typing import Dict
import asyncio
from functools import wraps
from passlib.context import CryptContext


def sync_to_async(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(f, *args, **kwargs)

    return wrapper


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
        return get_one(user)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


check_token_validity_async = sync_to_async(check_token_validity)


@router.post("/bot_connect")
async def user_create_bot(
    bot_token: BotTokenSchema,
    auth_token: str = Header(alias="auth_token"),
):
    try:
        user = await check_token_validity_async(auth_token)
        asyncio.create_task(main(bot_token.bot_token))
        return {"bot_connection": "success"}
    except Missing as exc:
        raise HTTPException(status_code=401, detail=exc.msg)
