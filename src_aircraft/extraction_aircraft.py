import requests
import pandas as pd



def extract_live_aircraft_data():
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
    flights = extract_live_aircraft_data()
    print(flights.head())
