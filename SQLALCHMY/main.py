# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# PostgreSQL URL format for psycopg3:
# postgresql+psycopg://username:password@host:port/dbname
DATABASE_URL = "postgresql+psycopg://postgres:your_password@localhost:5432/your_db"

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Logs SQL queries
    pool_size=10,        # Max connections in pool
    max_overflow=5,      # Extra connections allowed
)

# Base class for ORM models
class Base(DeclarativeBase):
    pass

# Session factory
SessionLocal = sessionmaker(bind=engine)
