import pandas as pd

# Load routes data
routes = pd.read_csv('OpenFlights_data/routes.dat', header=None)

# Load airports data
airports = pd.read_csv('OpenFlights_data/airports.dat', header=None)

# Load airlines data
airlines = pd.read_csv('OpenFlights_data/airlines.dat', header=None)

# Load countries data
countries = pd.read_csv('OpenFlights_data/countries.dat', header=None)

# OpenSky API
