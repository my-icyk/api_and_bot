from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from app.config.settings import settings


# What is all of setings
engine = create_engine(
    settings.mssql_url,
    # echo=settings.DEBUG,
    fast_executemany=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# # Test connection
# with engine.connect() as connection:
#     result = connection.execute(text("SELECT 1 AS test"))
#     for row in result:
#         print("Test query result:", row.test)
