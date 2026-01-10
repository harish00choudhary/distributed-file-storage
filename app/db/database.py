from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Change username, password, host if needed
DATABASE_URL = "mysql+pymysql://root:Harish%401234@localhost:3306/distributed_storage"


engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
