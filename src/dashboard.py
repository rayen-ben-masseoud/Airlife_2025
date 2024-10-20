import psycopg2
import pandas as pd

def generate_flights_dashboard(icao24_code):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="airlife_db",
        user="",
        password="",
        host="localhost",
        port="5432"
    )
    
    try:
        # Crear un cursor para ejecutar la consulta
        cursor = conn.cursor()
        
        # Consulta SQL para obtener la información del dashboard
        query = """
        SELECT 
            h.icao24 AS plane_icao24,
            p.name AS plane_name,
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
            h.first_seen,
            h.last_seen,

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
            planes p ON h.icao24 = p.icao
        JOIN 
            airports d ON h.est_departure_airport = d.icao
        LEFT JOIN 
            airports ar ON h.est_arrival_airport = ar.icao
        LEFT JOIN 
            flights f ON h.icao24 = f.icao24
        ORDER BY 
            h.last_seen DESC;
        """

        # Ejecutar la consulta
        cursor.execute(query, (icao24_code,))
        
        # Recuperar los resultados
        results = cursor.fetchall()
        
        # Convertir los resultados a un DataFrame de pandas
        columns = [
            'Aircraft ICAO24', 'Aircraft Name', 'Aircraft Callsign', 'On_ground', 'Departure Airport ICAO', 'Departure Airport Name', 
            'Departure Airport City', 'Departure Airport Country', 'Arrival Airport ICAO',
            'Arrival Airport Name', 'Arrival City', 
            'Arrival Airport Country', 'first_seen', 'last_seen', 'longitude', 'latitude', 'baro_altitude', 'velocity', 'vertical_rate', 'is_high_altitude'
        ]
        flight_dashboard = pd.DataFrame(results, columns=columns)

        return flight_dashboard

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cerrar la conexión
        cursor.close()
        conn.close()

# Uso de la función
# icao24_code = 'A0C7D4'  # Reemplaza con el ICAO24 que deseas consultar
# dashboard_df = fetch_flight_dashboard(icao24_code)
# print(dashboard_df)
