# Airlife ETL Pipeline

Airlife allows users to track the lifetime history of airplanes, including total distance flown, estimated carbon footprint, and most recent location. The ETL pipeline extracts, transforms, and loads data from OpenFlights (airport data) and the OpenSky Network (live flight data) into a PostgreSQL database.

## Prerequisites

1. **Python 3.11+** installed.
2. **PostgreSQL** installed and running.
   - Ensure PostgreSQL is running on the default port `5432`.
3. **Virtual environment** for isolating dependencies.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/airlife_2025.git
   cd airlife_2025
Create and Activate the Virtual Environment:

On macOS/Linux:
bash
Copiar código
python3 -m venv virtualenv
source virtualenv/bin/activate