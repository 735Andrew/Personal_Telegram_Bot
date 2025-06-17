from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

POSTGRESQL_DATABASE_PASSWORD = os.environ.get("POSTGRESQL_DATABASE_PASSWORD")
