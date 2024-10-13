import time
from sqlalchemy import create_engine, Column, String, Float,text, select, insert, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import numpy as np
import geopy.distance
from src_aircraft.extraction_aircraft import  extract_live_aircraft_data
from src_aircraft.transformation_aircraft import  enrich_aircraft_data
from src_aircraft.loading_aircraft import load_data_to_postgres
from src_aircraft.utils import log_message
# Database credentials
db_user = "noura_post"
db_password = "noura"
db_host = "localhost"
db_port = "5432"
db_name = "aircraft_db"

# Create a connection to the PostgreSQL database
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')


Base = declarative_base()

# Define the aircraft_metrics table
class AircraftMetrics(Base):
    __tablename__ = 'aircraft_metrics'
    
    icao24 = Column(String(6), primary_key=True)
    previous_latitude = Column(Float)
    previous_longitude = Column(Float)
    cumulative_distance = Column(Float)
    cumulative_carbon_footprint = Column(Float)
    origin_country = Column(String(100))

# Create the table in the database if it doesn't exist
Base.metadata.create_all(engine)

def insert_new_aircraft_if_not_exists(metrics_table, session, aircraft_id, origin_country, current_latitude, current_longitude):
        update_query = text("""
            UPDATE aircraft_metrics
            SET previous_latitude = :current_lat, 
            previous_longitude = :current_lon, 
            cumulative_distance = :new_cumulative_distance,
            cumulative_carbon_footprint = :new_cumulative_carbon_footprint,
            origin_country = :origin_country
            WHERE icao24 = :aircraft_id;
        """)
        params = {
            'current_lat': current_latitude,  
            'current_lon': current_longitude,  
            'new_cumulative_distance':0,  
            'new_cumulative_carbon_footprint':0,  
            'origin_country': origin_country,  
            'aircraft_id': aircraft_id 
        }

        session.execute(update_query, params)






# Function to update aircraft metrics
def update_aircraft_metrics(session):
    current_query = "SELECT icao24, origin_country, latitude AS current_latitude, longitude AS current_longitude,on_ground FROM aircrafts;"
    current_data = pd.read_sql(current_query, engine)

    metrics_query = "SELECT icao24, origin_country, previous_latitude, previous_longitude, cumulative_distance, cumulative_carbon_footprint FROM aircraft_metrics;"
    metrics_data = pd.read_sql(metrics_query, engine)

    # If metrics_data is empty, initialize aircraft_metrics with current_data
    # Insert new aircraft if not already in the metrics table
    
    if metrics_data.empty:
        for index, row in current_data.iterrows():
            new_entry = AircraftMetrics(
                icao24=row['icao24'],
                
                previous_latitude=row['current_latitude'],
                previous_longitude=row['current_longitude'],
                cumulative_distance=0.0,
                cumulative_carbon_footprint=0.0,
                origin_country=row['origin_country']
            )
            session.add(new_entry)
        session.commit()
        print("Aircraft metrics initialized with current data.")
        return
    for index, row in current_data.iterrows():
        #print(index)
        #print(row)
        aircraft_id=row['icao24']
        current_lat=float(row['current_latitude'])
        current_lon=float(row['current_longitude'])
        origin_country=current_data['origin_country'].iloc[0]


        metrics_row = metrics_data.loc[metrics_data['icao24']==aircraft_id]
        #print(metrics_row)
         # Insert new aircraft if not already in the metrics table
         

        # Reflect the existing table
        aircraft_exists = metrics_data[metrics_data['icao24'] == aircraft_id]
    
        if aircraft_exists.empty:  # If aircraft_id doesn't exist in the DataFrame
            insert_new_aircraft_if_not_exists(metrics_data,session, aircraft_id, origin_country, current_lat, current_lon)
        elif not metrics_row.empty: 
            metrics_row = metrics_row.iloc[0]


            if not pd.isna(row['current_latitude']) and not pd.isna(row['current_longitude']) and \
                 not pd.isna(metrics_row['previous_latitude']) and not pd.isna(metrics_row['previous_longitude']):
                previous_lat=float(metrics_row['previous_latitude'])
                previous_lon=float(metrics_row['previous_longitude'])
                # Compute the distance using the previous coordinates
                coords_1 = (previous_lat, previous_lon)
                coords_2 = (current_lat, current_lon)

                distance=geopy.distance.geodesic(coords_1, coords_2).km
                #distance=20
                float_value = float(metrics_row['cumulative_distance'])
                new_cumulative_distance=float_value+distance


                
            elif row['on_ground']:
                new_cumulative_distance=float(metrics_row['cumulative_distance'])


            cumulative_carbon_footprint=float(metrics_row['cumulative_carbon_footprint'])+20
            # Update the aircraft_metrics table
            update_query = text("""
                    UPDATE aircraft_metrics
                    SET previous_latitude = :current_lat, 
                    previous_longitude = :current_lon, 
                    cumulative_distance = :new_cumulative_distance,
                    cumulative_carbon_footprint = :new_cumulative_carbon_footprint,
                    origin_country = :origin_country
                    WHERE icao24 = :aircraft_id;
                    """)
            params = {

                'current_lat': row['current_latitude'],  # Single value
                'current_lon': row['current_longitude'],  # Single value
                'new_cumulative_distance':new_cumulative_distance,  # Single value
                'new_cumulative_carbon_footprint': cumulative_carbon_footprint,  # Single value
                'origin_country': origin_country,  # Single value
                'aircraft_id': row['icao24']  # Single value
                    }
            session.execute(update_query, params)
            #print(f"Aircraft {aircraft_id} already exists in aircraft_metrics.")
            session.commit()
    print("Aircraft metrics updated successfully.")


def run_etl():
    # Extraction
    log_message("Starting extraction phase.")
    flights_df = extract_live_aircraft_data()

    # Transformation
    log_message("Starting transformation phase.")
    enriched_flights_df = enrich_aircraft_data(flights_df)

    # Loading
    log_message("Starting loading phase.")
    load_data_to_postgres(enriched_flights_df, "aircrafts")



if __name__ == "__main__":
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()


    try:
        while True:
            run_etl()
            update_aircraft_metrics(session)
            time.sleep(60)  # Sleep for 60 seconds
    except KeyboardInterrupt:
        print("Process interrupted. Exiting...")
    finally:
        session.close()
