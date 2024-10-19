import pandas as pd


def clean_airport_data(airports_df):
    # Remove rows with missing latitude or longitude
    airports_df = airports_df.dropna(subset=['Latitude', 'Longitude'])
    # Convert latitude and longitude to float
    airports_df['Latitude'] = airports_df['Latitude'].astype(float)
    airports_df['Longitude'] = airports_df['Longitude'].astype(float)
    return airports_df


def enrich_flight_data(flights_df):
    # Filter out rows where the plane is on the ground
    flights_df = flights_df[flights_df['on_ground'] == False]
    # Add a new column 'is_high_altitude' if altitude > 10,000 meters
    flights_df.loc[:, 'is_high_altitude'] = flights_df['baro_altitude'] > 10000
    return flights_df


if __name__ == "__main__":
    # Example usage of transformation functions
    from extraction import extract_openflights_data, extract_live_flight_data

    airports = extract_openflights_data()
    cleaned_airports = clean_airport_data(airports)
    print(cleaned_airports.head())

    flights = extract_live_flight_data()
    enriched_flights = enrich_flight_data(flights)
    print(enriched_flights.head())