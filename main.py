from src.extraction import extract_openflights_data, extract_live_flight_data
from src.transformation import clean_airport_data, enrich_flight_data
from src.loading import load_data_to_postgres
from src.utils import log_message


def run_etl():
    # Extraction
    log_message("Starting extraction phase.")
    airports_df = extract_openflights_data()
    flights_df = extract_live_flight_data()

    # Transformation
    log_message("Starting transformation phase.")
    cleaned_airports_df = clean_airport_data(airports_df)
    enriched_flights_df = enrich_flight_data(flights_df)

    # Loading
    log_message("Starting loading phase.")
    load_data_to_postgres(cleaned_airports_df, "airports")
    load_data_to_postgres(enriched_flights_df, "flights")


if __name__ == "__main__":
    run_etl()
