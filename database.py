from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def createNewSession():
    DATABASE_URL = "sqlite:///./database.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    return session
