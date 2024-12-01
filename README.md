# sqlalchemy-challenge

This assignment was broken down into 2 parts: Climate analysis and designing a climate app

Part 1:
Using Python and SQLAlchemy, a basic climate analysis was conducted along with a data
exploration of the climate database. Using SQLAlchemy ORM queries, Pandas, and Matplotlib:
'create_engine()' function was used to connect to SQLite data, 'automap_base()' was used
to reflect the tables into classes and then save references to classes named 'station' and
'measurement'. Python was linked to the database by creating a SQLAlchemy session.

Precipitation Analysis:
Found the most recent date in the dataset dynamically to avoid hardcoding, allowing
scripts more flexibility and reusability. 
Using that date, 12 months of precipitation data was retrieved by querying previous
12 months of data.
Loaded the query results into a Pandas DataFrame and set the column  names. The DataFrame 
was sorted by 'date' values, and the results were plotted on a line graph. The summary 
statistics were printed for the precipitation data.

Station Analysis:
Designed a query to calculate the total number of stations in the dataset, then another 
query was desgined to find hte most active stations with the most rows. They were then 
listed in descending order using the observation counts. Station ID USC00519281 was the
station with the greatest number of observations, and its analysis was conducted retrieving
the lowest, highest, and avg temperature. 
Designed a query to get the previous 12 months of temperature observation (TOBS) data. 
Plotted the results into a histogram with 12 bins and finally closed the session.

Part 2:
Designed a climate app:
Created the homepage and listed all the available routes, then proceeded to convert
the query results from the precipitation analysis to a dictionary using 'date' as the 
key and 'prcp' as the value. Created the 'stations' and 'TOBS' routes. Also created a 
function that calculates temperature statistics. If only a start date is given, then it 
retrieves the data from that date. If both start and end date are given, it retrieves 
data for that specified range. All routes are designed to return a JSON list. 
 

