import subprocess
import logging
import platform
import sys
import os
from src.extraction import extract_openflights_data, extract_live_flight_data
from src.transformation import clean_airport_data, enrich_flight_data
from src.loading import load_data_to_postgres
from sqlalchemy import create_engine
import psycopg2

logging.basicConfig(level=logging.INFO)

def check_postgres_status():
    """Check if PostgreSQL is running by using the pg_isready command."""
    try:
        # Check PostgreSQL status
        result = subprocess.run(["pg_isready"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            logging.info("PostgreSQL is running and accepting connections.")
            return True
        else:
            logging.warning("PostgreSQL is not running or not accepting connections.")
            return False
    except FileNotFoundError:
        logging.error("pg_isready command not found. Ensure PostgreSQL is installed.")
        return False

def start_postgresql():
    """Attempt to start PostgreSQL based on the platform (macOS/Linux/Windows)"""
    try:
        os_platform = platform.system()
        if os_platform == "Darwin":  # macOS
            logging.info("Attempting to start PostgreSQL on macOS using brew...")
            subprocess.run(["brew", "services", "start", "postgresql"])
        elif os_platform == "Linux":
            logging.info("Attempting to start PostgreSQL on Linux using pg_ctl...")
            subprocess.run(["pg_ctl", "start", "-D", "/usr/local/var/postgres"])
        elif os_platform == "Windows":
            logging.info("Attempting to start PostgreSQL on Windows...")
            subprocess.run(["net", "start", "postgresql-x64-14"])  # Adjust if necessary
        else:
            logging.warning(f"Automatic start for PostgreSQL not supported on {os_platform}.")
            logging.warning("Please start PostgreSQL manually.")
            return False
        return True
    except Exception as e:
        logging.error(f"Failed to start PostgreSQL: {e}")
        return False

def create_database_if_not_exists():
    """Create the database if it doesn't exist"""
    try:
        db_user = "david_cardo"
        db_password = "CarGom57"
        db_host = "localhost"
        db_port = "5432"
        db_name = "airlife_db"
        conn = psycopg2.connect(user=db_user, password=db_password, host=db_host, port=db_port, database="postgres")
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {db_name};")
            logging.info(f"Database {db_name} created successfully.")
        else:
            logging.info(f"Database {db_name} already exists.")
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error creating database: {e}")
        sys.exit(1)

def run_etl():
    """Run the full ETL pipeline."""
    try:
        logging.info("Starting extraction phase.")
        airports_df = extract_openflights_data()
        flights_df = extract_live_flight_data()

        logging.info("Starting transformation phase.")
        cleaned_airports_df = clean_airport_data(airports_df)
        enriched_flights_df = enrich_flight_data(flights_df)

        logging.info("Starting loading phase.")
        load_data_to_postgres(cleaned_airports_df, "airports")
        load_data_to_postgres(enriched_flights_df, "flights")

        logging.info("ETL process completed successfully.")
    except Exception as e:
        logging.error(f"ETL pipeline failed: {e}")

if __name__ == "__main__":
    # Step 1: Check if PostgreSQL is running
    if not check_postgres_status():
        logging.info("PostgreSQL is not running. Attempting to start it...")
        if not start_postgresql():
            logging.error("PostgreSQL could not be started automatically.")
            sys.exit(1)

    # Step 2: Ensure the database exists
    create_database_if_not_exists()

    # Step 3: Run the ETL pipeline if PostgreSQL is running
    run_etl()
