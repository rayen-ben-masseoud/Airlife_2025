import pytest


def test_etl_pipeline():
    from src.extraction import extract_openflights_data
    from src.transformation import clean_airport_data
    from src.loading import load_data_to_postgres

    # Extraction
    airports_df = extract_openflights_data()

    # Transformation
    cleaned_airports_df = clean_airport_data(airports_df)

    # Loading
    try:
        load_data_to_postgres(cleaned_airports_df, "test_airports_table")
    except Exception as e:
        pytest.fail(f"ETL pipeline failed at loading phase: {e}")
