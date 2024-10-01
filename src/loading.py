import psycopg2
from sqlalchemy import create_engine


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
        print(f"Data loaded successfully to table {table_name}")
    except Exception as e:
        print(f"Error loading data: {e}")


if __name__ == "__main__":
    # Example usage of load function
    from extraction import extract_openflights_data
    from transformation import clean_airport_data

    airports = extract_openflights_data()
    cleaned_airports = clean_airport_data(airports)
    load_data_to_postgres(cleaned_airports, "airports")
