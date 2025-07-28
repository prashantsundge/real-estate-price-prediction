
from sqlalchemy import create_engine
from src.config.db_config import SQLALCHEMY_DATABASE_URL


engine = create_engine(SQLALCHEMY_DATABASE_URL)

