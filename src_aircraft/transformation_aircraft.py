import pandas as pd





def enrich_aircraft_data(aircrafts_df):
    # Filter out rows where the plane is on the ground
    #flights_df = flights_df[flights_df['on_ground'] == False]
    # Add a new column 'is_high_altitude' if altitude > 10,000 meters
    aircrafts_df.loc[:, 'is_high_altitude'] = aircrafts_df['baro_altitude'] > 10000
    # Add a new column 'is_high_altitude' if altitude > 10,000 meters  
        # Add columns if they don't exist


     
    return aircrafts_df


if __name__ == "__main__":
    # Example usage of transformation functions
    from extraction_aircraft import  extract_live_aircraft_data


    aircrafts = extract_live_aircraft_data()
    enriched_aircrafts = enrich_aircraft_data(aircrafts)
    print(enriched_aircrafts.head())
