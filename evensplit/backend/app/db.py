"""Database-agnostic SQLAlchemy setup. Swap DATABASE_URL for Postgres/MySQL/etc.
without touching the rest of the app."""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Default SQLite file lives under the user's home directory rather than the
# project folder: SQLite needs real file locking, which doesn't work
# reliably on some network/bridge-mounted filesystems. Override with
# DATABASE_URL to point at Postgres/MySQL/etc. instead -- the rest of the
# app is database-agnostic (SQLAlchemy Core/ORM only).
_default_dir = os.path.join(os.path.expanduser("~"), ".evensplit")
os.makedirs(_default_dir, exist_ok=True)
_default_path = os.path.join(_default_dir, "evensplit.db")

DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{_default_path}")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
