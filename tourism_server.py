from collections import defaultdict
from flask import Flask
import requests
import json
import logging
from logging.handlers import RotatingFileHandler
import db_api

# Global Variable section
WEB_URL = 'http://api.openweathermap.org/data/2.5/'
WEATHER_DATA = 'weather?'
FORECAST_DATA = 'forecast?'
APP_ID = "1830192509846048e422e9bce6861b8f"
HEADERS = {'Content-Type': 'application/json'}
SERVICE_PORT = 8000

# Global variable for Database columns
ID = 0
START_DATE = 1
END_DATE = 2
DESTINATION = 3
PRICE = 4
DESC = 5
TYPE = 6
RISK_FACTOR = 7


app = Flask(__name__)


def read_city_list():
    """
    Read the listed cities in json file and put the cities in weather group
    """
    with open('city.list.json', encoding="utf8") as s:
        all_city_weather_dict = {}
        weather_group = defaultdict(list)
        all_cities_data = json.load(s)
        for item in all_cities_data:
            all_city_weather_dict[item['name']] = \
                get_current_weather(item['coord']['lat'], item['coord']['lon'])['temp']

        for key in all_city_weather_dict.keys():
            if 260 <= all_city_weather_dict[key] <= 270:
                weather_group['260-270'].append(key)
            elif 270 <= all_city_weather_dict[key] <= 280:
                weather_group['270-280'].append(key)
            else:
                weather_group['280 above'].append(key)
        return str(dict(weather_group))


def get_current_weather(lattitude, longitude):
    """
    Get the current weather
    """
    try:
        response_weather = requests.get(WEB_URL + WEATHER_DATA + "lat=" +
                                        str(lattitude) + "&lon=" +
                                        str(longitude) + "&appid=" +
                                        APP_ID)
        curr_weather = response_weather.json()
        return curr_weather['main']
        
    except Exception as excep:
        app.logger.error("Error while getting weather data" + str(excep))


def get_formatted_forecast_data(forecast_list):
    """
    Format the weather data
    """
    weather_dict = defaultdict(int)
    for item in forecast_list:
        for weather_item in item['weather']:
            weather_dict[weather_item['main']] += 1
    return dict(weather_dict)


def get_forecast_weather_data(lattitude, longitude):
    """
    Get forecast weather data and return the probability of the weather
    """
    try:
        response_forecast = requests.get(WEB_URL + FORECAST_DATA + "lat=" +
                                         str(lattitude) + "&lon=" +
                                         str(longitude) + "&appid=" +
                                         APP_ID)
        forecast_weather = response_forecast.json()
        formatted_data = \
            get_formatted_forecast_data(forecast_weather['list'])
        return str(formatted_data)

    except Exception as excep:
        app.logger.error("Error while getting weather data" + str(excep))


@app.route('/weather/<lat>/<long>')
def get_weather_data(lat, long):
    """
    API endpoint for the current weather
    """
    return "Current weather Data is " + str(get_current_weather(lat, long))


@app.route('/forcast/<lat>/<long>')
def get_forecast_data(lat, long):
    """
    API endpoint for the forecasted weather
    """
    return "Probability of forecast data for next 5 days " + str(get_forecast_weather_data(lat, long))


@app.route('/cities/')
def get_cities_weather_data():
    """
    API endpoint to show weather groups of South American capitals
    """
    city_list = read_city_list()
    return city_list


@app.route('/packages/')
def get_tour_packages():
    """
    API endpoints for the available packages of the tourist company
    """
    str_package = ""
    package_data = db_api.select_tour_packages()
    for item in package_data:
        str_package += "[{Tour Id :" + item[ID] + ",Start_Date :" + item[START_DATE] +\
                       ",End_Date :" + item[END_DATE] + ",Destination :" + \
                       item[DESTINATION] + ",Price :" + item[PRICE] +\
                       ",Description : " + item[DESC] + ",Type :" + \
                       item[TYPE] + ",Risk_Factor :" + item[RISK_FACTOR] + "}],"

    package_json = json.dumps(str_package)
    return package_json


@app.route('/trip/<start_date>/<end_date>/')
def get_tour_based_on_dates(start_date, end_date):
    """
    Get available tours based on the dates
    """
    str_package = ""
    package_data = db_api.select_tour_based_on_dates(start_date, end_date)
    for item in package_data:
        str_package += "[{Tour Id :" + item[ID] + ",Start_Date :" + item[START_DATE] +\
                       ",End_Date :" + item[END_DATE] + ",Destination :" + \
                       item[DESTINATION] + ",Price :" + item[PRICE] +\
                       ",Description : " + item[DESC] + ",Type :" + \
                       item[TYPE] + ",Risk_Factor :" + item[RISK_FACTOR] + "}],"

    package_json = json.dumps(str_package)
    return package_json


if __name__ == "__main__":
    # Logging
    handler = RotatingFileHandler('app_logger.log', maxBytes=10000,
                                  backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=SERVICE_PORT)