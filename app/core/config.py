import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask / JWT
    SECRET_KEY = os.getenv("SECRET_KEY")

    # MySQL / SQLAlchemy
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")

    # SQLAlchemy database URI
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}/{MYSQL_DB}"
    )
