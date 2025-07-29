import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()  # Load DB credentials from .env

def load_data_from_mysql(table_name: str) -> pd.DataFrame:
    """
    Load data from a specified MySQL table and return as a DataFrame.
    """
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db = os.getenv("DB_NAME")



    connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(connection_string)
    
    df = pd.read_sql(f"SELECT * FROM {table_name}", engine)
    return df

