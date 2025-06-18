from app.models import UserSchema, LogInSchema
from psycopg2 import IntegrityError
from app.errors import Duplicate, Missing
from app.data.init import connection, cursor
import app.routes as r
from typing import Dict
from authx import AuthX, AuthXConfig
from config import JWT_SECRET_KEY


config = AuthXConfig()
config.JWT_SECRET_KEY = JWT_SECRET_KEY
security = AuthX(config=config)


def model_to_dict(user: UserSchema) -> dict:
    # Converts a Pydantic model into a dictionary suitable for database queries
    return user.model_dump()


def row_to_model(row: tuple) -> UserSchema:
    # Converts tuple from SQL query into a a Pydantic model
    u_id, login, password, name, auth_token = row
    return UserSchema(
        u_id=u_id, login=login, password=password, name=name, auth_token=auth_token
    )


def user_create(user: UserSchema) -> UserSchema | Duplicate:
    query = """
        INSERT INTO users
        (user_login,user_password,user_name)
        VALUES
        (%s, %s, %s);
    """

    model_dict = model_to_dict(user)
    params = (
        model_dict["login"],
        model_dict["password"],
        model_dict["name"],
    )

    try:
        cursor.execute(query, params)
    except IntegrityError:
        raise Duplicate(msg=f"User with login {user.login} already exists")
    finally:
        connection.commit()
    return user


def get_one(user: LogInSchema) -> Dict | Missing:
    query = """SELECT * FROM users WHERE user_login = %s"""
    params = (user.login,)
    cursor.execute(query, params)
    row = cursor.fetchone()

    if row is not None and r.pwd_context.verify(user.password, row[2]):
        user = row_to_model(row)
        token = security.create_access_token(uid=str(user.u_id))
        return save_user_token(user.u_id, token)
    else:
        raise Missing(msg=f"User with login {user.login} not found")


def save_user_token(user_id: int, token: str) -> Dict:
    query = """
        UPDATE users
        SET user_auth_token = %s
        WHERE user_id = %s;
    """

    params = (
        token,
        user_id,
    )

    try:
        cursor.execute(query, params)
    finally:
        connection.commit()
    return {"access_token": token}


def check_token_validity(token: str) -> UserSchema | Missing:
    query = """SELECT * FROM users WHERE user_auth_token = %s"""
    params = (token,)
    cursor.execute(query, params)
    row = cursor.fetchone()

    if row is not None:
        return row_to_model(row)
    else:
        raise Missing(msg=f"User not found")
