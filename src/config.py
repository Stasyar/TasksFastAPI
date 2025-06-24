import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(".tasks_env"))


class Settings:
    MODE: str = os.environ.get("MODE")

    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: int = os.environ.get("DB_PORT")
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASS: str = os.environ.get("POSTGRES_PASSWORD")
    DB_NAME: str = os.environ.get("POSTGRES_DB")

    RABBITMQ_URL: str = os.environ.get("RABBITMQ_URL")

    DB_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


settings = Settings()
