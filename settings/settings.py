__ALL__ = ["Settings"]

from decouple import config


class Storage:
    BUCKED_BOOKS: str = config('BUCKET_BOOKS')


class DB:
    DATABASE: str = config('DB_DATABASE')
    HOST: str = config('DB_HOST')
    PASSWORD: str = config('DB_PASSWORD')
    PORT: int = config('DB_PORT')
    USER: str = config('DB_USER')


class Postgres(DB):
    def get_conn_string(self) -> str:
        db_url = f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"
        return db_url


class Server:
    HOST: str = config('HOST')
    PORT: int = config('PORT')


class Settings:
    DB: Postgres = Postgres()
    Server: Server = Server()
    Storage: Storage = Storage()
    DEBUG: bool = config('DEBUG', default=False, cast=bool)
