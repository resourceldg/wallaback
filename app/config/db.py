from sqlalchemy import create_engine, MetaData

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

#production mode
#SQLALCHEMY_DATABASE_URL = "postgresql://username:password@db:5432/database"
#dev mode
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://lucas:zen777@localhost:5432/wallaback"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
conn = engine.connect()
SessionLocal = sessionmaker(bind=engine)
meta = MetaData()
