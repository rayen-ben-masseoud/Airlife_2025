import psycopg2
import pandas as pd

def generate_flights_dashboard(icao24_code):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="airlife_db",
        user="allonch",
        password="Allonchmajo00%",
        host="localhost",
        port="5432"
    )
    
    try:
        # Create a cursor to execute the query
        cursor = conn.cursor()
        
        # SQL query to retrieve dashboard information
        query = """
        SELECT 
            h.icao24 AS plane_icao24,
            h.callsign,
            h.on_ground,
            d.icao AS departure_airport_icao,
            d.name AS departure_airport_name,
            d.city AS departure_airport_city,
            d.country AS departure_airport_country,
            d.longitude AS departure_airport_longitude,
            d.latitude AS departure_airport_latitude,
            d.altitude AS departure_airport_altitude,
            CASE 
                WHEN h.on_ground THEN ar.icao
                ELSE NULL
            END AS arrival_airport_icao,
            CASE 
                WHEN h.on_ground THEN ar.name
                ELSE NULL
            END AS arrival_airport_name,
            CASE 
                WHEN h.on_ground THEN ar.city
                ELSE NULL
            END AS arrival_airport_city,
            CASE 
                WHEN h.on_ground THEN ar.country
                ELSE NULL
            END AS arrival_airport_country,
            CASE 
                WHEN h.on_ground THEN ar.longitude
                ELSE NULL
            END AS arrival_airport_longitude,
            CASE 
                WHEN h.on_ground THEN ar.latitude
                ELSE NULL
            END AS arrival_airport_latitude,
            CASE 
                WHEN h.on_ground THEN ar.altitude
                ELSE NULL
            END AS arrival_airport_altitude,
            h."firstSeen",
            h."lastSeen",

            CASE 
                WHEN NOT h.on_ground THEN f.longitude
                ELSE NULL
            END AS longitude,
            
            CASE 
                WHEN NOT h.on_ground THEN f.latitude
                ELSE NULL
            END AS latitude,
            
            CASE 
                WHEN NOT h.on_ground THEN f.baro_altitude
                ELSE NULL
            END AS baro_altitude,
            
            CASE 
                WHEN NOT h.on_ground THEN f.velocity
                ELSE NULL
            END AS velocity,
            
            CASE 
                WHEN NOT h.on_ground THEN f.vertical_rate
                ELSE NULL
            END AS vertical_rate,
            
            CASE 
                WHEN NOT h.on_ground THEN f.is_high_altitude
                ELSE NULL
            END AS is_high_altitude
            
        FROM
            historic_flights_aircraft h
        JOIN 
            airports d ON h."estDepartureAirport" = d.icao
        LEFT JOIN 
            airports ar ON h."estArrivalAirport" = ar.icao
        LEFT JOIN 
            flights f ON h.icao24 = f.icao24
        ORDER BY 
            h."lastSeen" DESC;
        """

        # Execute the query
        cursor.execute(query, (icao24_code,))
        
        # Retrieve the results
        results = cursor.fetchall()
        
        # Convert the results into a pandas DataFrame
        columns = [
            'plane_icao24', 'callsign', 'on_ground', 'departure_airport_icao', 'departure_airport_name', 'departure_airport_city', 'departure_airport_country',
            'departure_airport_longitude', 'departure_airport_latitude', 'departure_airport_altitude',
            'arrival_airport_icao', 'arrival_airport_name', 'arrival_airport_city', 'arrival_airport_country', 'arrival_airport_longitude', 'arrival_airport_latitude', 'arrival_airport_altitude'
            'firstSeen', 'lastSeen', 'longitude', 'latitude', 'baro_altitude', 'velocity', 'vertical_rate', 'is_high_altitude'
        ]
        data = []
        for elem in range(len(results)):
            d = {}
            i = 0
            for key in columns:
                d[key] = results[elem][i]
                i = i + 1
            data.append(d)

        flight_dashboard = pd.DataFrame(data)

        return flight_dashboard

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the connection
        cursor.close()
        conn.close()