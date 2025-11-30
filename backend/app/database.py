import os
import logging
from urllib.parse import quote_plus
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# DB ENV VARIABLES
# ---------------------------------------------------------

DB_HOST = os.getenv("DB_HOST")            # Public or private endpoint
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# ---------------------------------------------------------
# SQLAlchemy Database URL
# ---------------------------------------------------------

def get_database_url():
    encoded_user = quote_plus(DB_USER)
    encoded_password = quote_plus(DB_PASSWORD)

    return (
        f"postgresql://{encoded_user}:{encoded_password}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


# ---------------------------------------------------------
# SQLAlchemy Engine + Session
# ---------------------------------------------------------

try:
    DATABASE_URL = get_database_url()
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=150
    )

    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    logger.info("Database engine created successfully (direct connection).")

except Exception as e:
    logger.error(f"Database connection failed: {e}")
    raise


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
