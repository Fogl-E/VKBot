from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config.config import config

db = create_engine(config.database_url)
SessionLocal  = sessionmaker(db)

def con():
    cn = SessionLocal()
    try:
        yield cn
    finally:
        cn.close()
