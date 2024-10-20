from datetime import datetime, timedelta
from src.dashboard import flights_dashboard
from src.extraction import date_to_timestamp, extract_historic_aircraft_data, extract_openflights_data, extract_live_flight_data
from src.transformation import clean_airport_data, enrich_flight_data
from src.loading import load_data_to_postgres
from src.utils import log_message


def run_etl():
    # Input
    entry = input("\n\n\nIntroduce the aircraft's ICAO (hexadecimal code) and the start date (format: ICAO;YYYY-MM-DD hh:mm:ss):\n IMPORTANT: To comply with OpenSky access policies, the start date must not be more than 30 DAYS from the current time!!: ")
    parts = entry.split(';')

    def validate_date(date_str):
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            return date
        except ValueError:
            print("Start date format not valid. Must be YYYY-MM-DD hh:mm:ss")
            return None

    # Verify parts
    if len(parts) != 2:
        print("Error: Must introduce ICAO and start date in the correct format and separated by ;")
    else:
        icao = parts[0].strip() 
        begin = validate_date(parts[1].strip()).strftime("%Y-%m-%d %H:%M:%S")
        end = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # current time

        # Check dates
        if begin is not None and end is not None:
            if end < begin:
                print("Error: Start date cannot be in the future.")
            if abs(datetime.strptime(end, "%Y-%m-%d %H:%M:%S")-datetime.strptime(begin, "%Y-%m-%d %H:%M:%S")) > timedelta(days=30):
                print(f"Error: Start date is more than 30 days from the current time ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}).")

    # Extraction
    log_message("Starting extraction phase.")
    airports_df, planes_df = extract_openflights_data()
    flights_df = extract_live_flight_data()
    historic_aircraft_flights_df = extract_historic_aircraft_data(icao, date_to_timestamp(begin), date_to_timestamp(end))

    # Transformation
    log_message("Starting transformation phase.")
    cleaned_airports_df = clean_airport_data(airports_df)
    enriched_flights_df = enrich_flight_data(flights_df)

    # Loading
    log_message("Starting loading phase.")
    load_data_to_postgres(cleaned_airports_df, "airports")
    load_data_to_postgres(planes_df, "planes")
    load_data_to_postgres(historic_aircraft_flights_df, "historic_flights_aircraft")
    load_data_to_postgres(enriched_flights_df, "flights")

    # Dashboard
    log_message("Generating dashboard.")
    flights_dashboard = flights_dashboard(icao)
    load_data_to_postgres(flights_dashboard, f"flights_of_aircraft_{icao}")
    print(flights_dashboard)


if __name__ == "__main__":
    run_etl()
