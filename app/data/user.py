from app.models import UserSchema, LogInSchema
from psycopg2 import IntegrityError
from app.errors import Duplicate, Missing
from app.data.init import connection, cursor
import app.routes as r


def model_to_dict(user: UserSchema) -> dict:
    # Converts a Pydantic model into a dictionary suitable for database queries
    return user.model_dump()


def row_to_model(row: tuple) -> UserSchema:
    # Converts tuple from SQL query into a a Pydantic model
    u_id, login, password, name = row
    return UserSchema(u_id=u_id, login=login, password=password, name=name)


def user_create(user: UserSchema) -> UserSchema | Duplicate:
    query = """
        INSERT INTO users
        (user_login,user_password,user_name)
        VALUES
        (%s, %s, %s);
    """

    model_dict = model_to_dict(user)
    params = [v for k, v in model_dict.items() if k != "u_id"]

    try:
        cursor.execute(query, params)
    except IntegrityError:
        raise Duplicate(msg=f"User with login {user.login} already exists")
    finally:
        connection.commit()
    return user


def get_one(user: LogInSchema) -> LogInSchema | Missing:
    query = """SELECT * FROM users WHERE user_login = %s"""
    params = (user.login,)

    cursor.execute(query, params)
    row = cursor.fetchone()

    if row is not None and r.pwd_context.verify(user.password, row[2]):
        return row_to_model(row)
    else:
        raise Missing(msg=f"User with login {user.login} not found")
