from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from lib.helpers.config import GetSettings

settings = GetSettings()

engine = create_engine(settings.DB_URL, echo=True, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def GetDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()