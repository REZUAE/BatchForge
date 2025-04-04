from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from batchforge.models import Base

DATABASE_URL = "postgresql://batchforge:password123@db:5432/batchforge_db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
