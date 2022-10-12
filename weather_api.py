# Local
import os
# Library
import requests as req

API_URL = f"http://api.weatherapi.com/v1/forecast.json?key={os.environ.get('WEATHER_API_KEY')}&q="

def find_location(city):
    url = API_URL + city
    response_json = req.get(url).json()

    if (list(response_json.keys())[0] == "error"):
        return response_json["error"]["message"]
    else:
        return response_json

async def short_broadcast(city):
    response_json = find_location(city)
    if (type(response_json) == type("")): # when returned erorr "No matching location found."
        return response_json

    weather_condition = response_json["current"]["condition"]["text"]
    temperature = str(response_json["current"]["temp_c"]) + "° C" + " | " + str(response_json["current"]["temp_f"]) + "° F" + " 🌡"
    icon_link = "https:" + response_json["current"]["condition"]["icon"]
    humidity = str(response_json["current"]["humidity"]) + "%" + " 💧"

    return {
        "weather_condition": weather_condition, "temperature": temperature,
        "icon_link": icon_link, "humidity": humidity,
    }

async def full_broadcast(city):
    response_json = find_location(city)
    if (type(response_json) == type("")): # when returned erorr "No matching location found."
        return response_json

    location = response_json["location"]["name"] + ", " + response_json["location"]["region"] + ", " + response_json["location"]["country"]
    time = response_json["location"]["localtime"] + " " + response_json["location"]["tz_id"]
    wind_speed = str(response_json["current"]["wind_kph"]) + " kph" + " | " + str(response_json["current"]["wind_mph"]) + " mph" + " 🍃"

    return {"location": location, "time": time, "wind_speed": wind_speed} | await short_broadcast(city)