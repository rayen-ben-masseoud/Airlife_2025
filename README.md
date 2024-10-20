# Airlife_2025
--change #database credentials (starting from line 12 in update_metrics.py) and in (src_aircraft/loading_aircraft.py starting from line 7 ) 

-This demo is not fully automated but computes the cumulative distance from the time we launch the update_metrics.py until we kill it:
On the terminal execute the following commands:
1) sudo su -l postgres  
2)psql -h localhost -p 5432 -U noura_post -d postgres # change your credentials as mentioned above
3)CREATE DATABASE aircraft_db;
4)run update_metrics.py
5)Visualize the sql tables using pgadmin4 or using queries in postgresql
--run update_metrics.py (it will create a new table aircraft_metrics to store the aircraft data and cumulative distance)


--the code will automatically redownload the data until you stop it in the shell command.


--Once you finish (after 15mins or 1 hour or the next day) you can visualize the data using sql query in pgadmin4.


--If you want to rerun the code update_metrics.py the next day, delete the aircraft_metrics table before in your database using DROP TABLE aircraft_metrics.
