# Airlife_2025
-Create an evironment in your local depository (instead of myen_etl):

Navigate to your desired folder
cd /path/to/your/current/folder


Create a new environment in the current folder
conda create --prefix ./myenv python=3.9

Activate the environment
conda activate ./myenv

Install packages from the requirements file
pip install -r requirements.txt


### change database credentials
--change #database credentials (starting from line 12 in update_metrics.py) and in (src_aircraft/loading_aircraft.py starting from line 7 ) 

### create manually the database aircraft_db
-This demo is not fully automated but computes the cumulative distance from the time we launch the update_metrics.py until we kill it:
On the terminal execute the following commands:

--1) sudo su -l postgres  

--2)psql -h localhost -p 5432 -U "user_name" -d postgres # change your credentials as mentioned above

--3)CREATE DATABASE aircraft_db;

### run the update_metrics.py

--4)run update_metrics.py


--run update_metrics.py (it will create a new table aircraft_metrics to store the aircraft data and cumulative distance)


--the code will automatically redownload the data until you stop it in the shell command.

### use pgadmin4 or postgresql
--5)Visualize the sql tables using pgadmin4 or using queries in postgresql



--If you want to rerun the code update_metrics.py the next day, delete the aircraft_metrics table before in your database using DROP TABLE aircraft_metrics.
