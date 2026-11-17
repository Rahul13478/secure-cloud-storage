#connecting database with Fast api 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import setting

engine = create_engine(setting.DATABASE_URL)

SessionLocal = sessionmaker(bind=engine , autoflush=False , autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    
    