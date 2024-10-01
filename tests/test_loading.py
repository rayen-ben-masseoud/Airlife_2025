import pytest
import pandas as pd
from src.loading import load_data_to_postgres


@pytest.fixture
def test_data():
    data = {
        "AirportID": [1, 2],
        "Name": ["Test Airport 1", "Test Airport 2"],
        "City": ["City 1", "City 2"],
        "Country": ["Country 1", "Country 2"],
        "IATA": ["T1", "T2"],
        "ICAO": ["TEST1", "TEST2"],
        "Latitude": [0.0, 1.1],
        "Longitude": [0.0, 1.1],
        "Altitude": [1000, 2000],
        "Timezone": [0, 1],
        "DST": ["E", "E"],
        "TzDatabaseTimezone": ["Timezone 1", "Timezone 2"],
        "Type": ["Type 1", "Type 2"],
        "Source": ["Source 1", "Source 2"]
    }
    return pd.DataFrame(data)


def test_load_data_to_postgres(test_data):
    try:
        load_data_to_postgres(test_data, "test_table")
    except Exception as e:
        pytest.fail(f"Loading data failed: {e}")
