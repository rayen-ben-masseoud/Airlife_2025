import requests
import pandas as pd


def extract_openflights_data():
    airports_url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"
    airports_cols = ['AirportID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Latitude', 'Longitude', 'Altitude',
                     'Timezone', 'DST', 'TzDatabaseTimezone', 'Type', 'Source']
    airports_df = pd.read_csv(airports_url, header=None, names=airports_cols)
    return airports_df


def extract_live_flight_data():
    opensky_url = "https://opensky-network.org/api/states/all"
    response = requests.get(opensky_url)
    if response.status_code == 200:
        columns = ['icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 'longitude', 'latitude',
                   'baro_altitude', 'on_ground', 'velocity', 'true_track', 'vertical_rate', 'sensors', 'geo_altitude',
                   'squawk', 'spi', 'position_source']
        flights_df = pd.DataFrame(response.json()['states'], columns=columns)
        return flights_df
    else:
        raise Exception(f"Error fetching data: {response.status_code}")


if __name__ == "__main__":
    airports = extract_openflights_data()
    print(airports.head())
    flights = extract_live_flight_data()
    print(flights.head())
