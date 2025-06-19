"""Initialize PostgreSQL database"""

import psycopg2 as ps
from typing import Optional
from config import POSTGRESQL_DATABASE_URL
from time import  sleep

connection: Optional = None
cursor: Optional = None


def get_db():
    global connection, cursor

    sleep(5)
    connection = ps.connect(POSTGRESQL_DATABASE_URL)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users
        (
            user_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            user_login VARCHAR(32) UNIQUE NOT NULL,
            user_password TEXT NOT NULL,
            user_name TEXT NOT NULL,
            user_auth_token TEXT 
        );
        """
    )

    connection.commit()


get_db()
