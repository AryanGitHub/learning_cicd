from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import config

#postgresql://username:password@localhost:port/database_name
POSTGRES_CONNECTION_URL = config.settings.db_protocol+config.settings.db_username+ ":" + config.settings.db_password + "@" + config.settings.db_hostname + ":" + str(config.settings.db_port) + "/" + config.settings.db_name

engine = create_engine(POSTGRES_CONNECTION_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()