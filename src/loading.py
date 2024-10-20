import pandas as pd
from sqlalchemy import create_engine
import logging

def load_data_to_postgres(df, table_name):
    try:
        # Replace with your actual credentials
        db_user = "david_cardo"
        db_password = "CarGom57"
        db_host = "localhost"
        db_port = "5432"
        db_name = "airlife_db"

        # Connect to PostgreSQL using SQLAlchemy
        engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logging.info(f"Data loaded successfully to table {table_name}")
    except Exception as e:
        logging.error(f"Error loading data to {table_name}: {e}")
        raise