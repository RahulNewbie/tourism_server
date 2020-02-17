Instructions to run the application.


This project has two parts. One is to put the tour data into the database and other is the 
rest server, which will connect openweathermap.org/api to get the weather data as well as database to 
get the tour data and show it to user. Project is written in python3 and pep8 standard is followed.


Please install Flask, json, requests, 

First please run the tour_planner application. This pplication will read the CSV file(tour_data.csv) and insert 
tour records into database.

To run the application, please use the following command.
python tour_planner.py

Now, database is ready with the tour data.

Next is to run the rest servera and open APIs for the user. Before that, please change the APP ID for the
openweather website
Please open the tourism_server.py and change the APP_ID and put your openweather website id.

To run the rest serer

python tourism_server.py

Once the rest server is up and running, user can use following API to fetch tour and weather data.

1. To fetch all the tour packages.

http://localhost:8000/packages/

2. To fetch the tours available in between start date and end date

http://localhost:8000/trip/<start_date>/<end_date>/

As an example, please use the following command

http://localhost:8000/trip/07-02-2020/12-02-2020/

please change the start date and end date according to the available tour packages. Tour packages will be visible in CSV file.


3. To fetch the weather of a city by providing the latitude and longitude.

http://localhost:8000/weather/<lat>/<lon>

As an example, use the following command
http://localhost:8000/weather/35/139

It will show the current temp, tem, max, temp_min, pressure, humidity of the city



4. To have the forecast of a city for next 5 days.
Please note, forecast API of openweather website gives data of 3hours interval. So, i made an assumtion and below API will give forecast data in form of probablity

http://localhost:8000/forcast/<lat>/<lon>

As an example, pease use the following command
http://localhost:8000/forcast/35/139


5. To fetch the weather groups of different south american capitals

http://localhost:8000/cities/

This will show you the cities with different temperature groups, according to the data found in openweather website.

You can change the cities list by editing the city.list.json file.

I have put some capitals in the json file.

