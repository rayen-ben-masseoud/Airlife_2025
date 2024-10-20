import pytest
from src.extraction import extract_openflights_data
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


def test_extract_openflights_data():
    df = extract_openflights_data()
    assert not df.empty
    assert 'Name' in df.columns


if __name__ == "__main__":
    pytest.main()
