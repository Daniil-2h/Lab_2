from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Пустые значения нужны для избежания предупреждений от компилятора
    DB_HOST: str = ""
    DB_PORT: int = 5432
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = ""
    # Пагинация
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100

    @property
    def DATABASE_URL_psycopg(self):
        # Нижняя строка подключения называется DSN
        # postgresql+psycopg://USER:PASSWORD@localhost:5432/sa
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
