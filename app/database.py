from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

sync_engine = create_engine(
    # Адрес базы данных
    url=settings.DATABASE_URL_psycopg,
    echo=True, # Откл/Вкл логи "алхимии"
    # pool_size=5,
    # max_overflow=10,
)

sessionLocal = sessionmaker(sync_engine)

class Base(DeclarativeBase):
    pass

# Тесты
# создаёт новую сессию алхимии для каждого HTTP запроса,
# а после завершения запроса закрывает сессию, освобождая соединение с базой данных.
def get_db():
    db = sessionLocal()
    try:
        yield db # Передаёт сессию в эндпоинт
    finally:
        db.close() # закрываем сессию, даже если произошла ошибка