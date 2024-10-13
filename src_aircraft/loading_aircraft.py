import psycopg2
from sqlalchemy import create_engine
import pandas as pd

def load_data_to_postgres(df, table_name):
    try:
        # Replace with your actual credentials
        db_user = "noura_post"
        db_password = "noura"
        db_host = "localhost"
        db_port = "5432"
        db_name = "aircraft_db"

        # Connect to PostgreSQL using SQLAlchemy
        engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data loaded successfully to table {table_name}")
    except Exception as e:
        print(f"Error loading data: {e}")

