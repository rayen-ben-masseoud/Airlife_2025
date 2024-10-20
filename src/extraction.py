import requests
import pandas as pd
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath('./opensky_api/python'))
from opensky_api import OpenSkyApi

def extract_openflights_data():
    # Airports
    airports_url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"
    airports_cols = ['airportID', 'name', 'city', 'country', 'iata', 'icao', 'latitude', 'longitude', 'altitude',
                     'timezone', 'dst', 'tzDatabaseTimezone', 'type', 'source']
    airports_df = pd.read_csv(airports_url, header=None, names=airports_cols)

    # Planes
    planes_url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/planes.dat"
    planes_cols = ['name', 'iata', 'icao']
    planes_df = pd.read_csv(planes_url, header=None, names=planes_cols)

    return airports_df, planes_df

def extract_live_flight_data():
    opensky_url = "https://opensky-network.org/api/states/all"
    response = requests.get(opensky_url)
    if response.status_code == 200:
        columns = ['icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 'longitude', 'latitude',
                   'baro_altitude', 'on_ground', 'velocity', 'true_track', 'vertical_rate', 'sensors', 'geo_altitude',
                   'squawk', 'spi', 'position_source']
        flights_df = pd.DataFrame(response.json()['states'], columns=columns)

        # Convert last and first seen to date format
        flights_df['time_position'] = pd.to_numeric(flights_df['time_position'], errors='coerce')
        flights_df['time_position'] = pd.to_datetime(flights_df['time_position'], unit='s')
        flights_df['last_contact'] = pd.to_numeric(flights_df['last_contact'], errors='coerce')
        flights_df['last_contact'] = pd.to_datetime(flights_df['last_contact'], unit='s')
        
        return flights_df
    else:
        raise Exception(f"Error fetching data: {response.status_code}")

# Converts a date to Unix date format
def date_to_timestamp(date):
    dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S") # example: "2024-10-19 12:00:00". Last 30 days max
    timestamp = int(dt.timestamp())
    return timestamp

def timestamp_to_date(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
def extract_historic_aircraft_data(icao, begin, end):
    api = OpenSkyApi("allonch", "airlife2025")
    raw_data = api.get_flights_by_aircraft(icao, begin, end)
    data = [list(f.keys) for f in raw_data]
    columns = ['icao24', 'first_seen', 'est_departure_airport', 'last_seen', 'est_arrival_airport', 
                'callsign', 'est_departure_airport_horiz_distance', 'est_departure_airport_vert_distance', 
                'est_arrival_airport_horiz_distance', 'est_arrival_airport_vert_distance', 
                'departure_airport_candidates_count', 'arrival_airport_candidates_count']
    historic_flights_df = pd.DataFrame(data, columns=columns)

    # Convert last and first seen to date format
    historic_flights_df['first_seen'] = pd.to_numeric(historic_flights_df['first_seen'], errors='coerce')
    historic_flights_df['first_seen'] = pd.to_datetime(historic_flights_df['first_seen'], unit='s')
    historic_flights_df['last_seen'] = pd.to_numeric(historic_flights_df['last_seen'], errors='coerce')
    historic_flights_df['last_seen'] = pd.to_datetime(historic_flights_df['last_seen'], unit='s')

    # If there is no estimated arrival airport, the flight might be still in the air
    historic_flights_df['on_ground'] = historic_flights_df['est_arrival_airport'].notna()
    
    return historic_flights_df


if __name__ == "__main__":
    begin = "2024-10-13 12:00:00"
    end = "2024-10-19 12:00:00" # 7 days max time span to request from current time
    # icao = "a2b47e" # This corresponds to a Delta Air Lines aircraft (a Boeing 737)
    icao = "3c675a"
    # 3c675a;2024-10-13 12:00:00
    
    airports = extract_openflights_data()
    print(airports.head())
    flights = extract_live_flight_data()
    print(flights.head())
    historic_aircraft_flights_df = extract_historic_aircraft_data(icao, date_to_timestamp(begin), date_to_timestamp(end))
    print(historic_aircraft_flights_df.head())
