"""Initialize PostgreSQL database"""

import psycopg2 as ps
from typing import Optional
from config import POSTGRESQL_DATABASE_PASSWORD


connection: Optional = None
cursor: Optional = None


def get_db():
    global connection, cursor

    connection = ps.connect(
        host="localhost",
        dbname="Personal_Telegram_Bot",
        user="postgres",
        password=POSTGRESQL_DATABASE_PASSWORD,
    )
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users
        (
            user_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            user_login VARCHAR(32) UNIQUE NOT NULL,
            user_password TEXT NOT NULL,
            user_name TEXT NOT NULL
        );
        """
    )

    connection.commit()


get_db()
