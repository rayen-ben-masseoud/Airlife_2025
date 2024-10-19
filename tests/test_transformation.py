import pytest
from src.transformation import clean_airport_data
from src.extraction import extract_openflights_data
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

def test_clean_airport_data():
    airports = extract_openflights_data()
    cleaned_airports = clean_airport_data(airports)
    assert 'Latitude' in cleaned_airports.columns
    assert not cleaned_airports['Latitude'].isnull().any()

if __name__ == "__main__":
    pytest.main()
