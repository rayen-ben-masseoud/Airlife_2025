# Airlife_2025
--change #database credentials (starting from line 12 in update_metrics.py) and in (src_aircraft/loading_aircraft.py starting from line 7 ) 


--run update_metrics.py (it will create a new table aircraft_metrics to store the aircraft data and cumulative distance)


--the code will automatically redownload the data until you stop it in the shell command.


--Once you finish (after 15mins or 1 hour or the next day) you can visualize the data using sql query in pgadmin4.


--If you want to rerun the code update_metrics.py the next day, delete the aircraft_metrics table before in your database using DROP TABLE aircraft_metrics.
