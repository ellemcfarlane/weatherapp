# Created by Elle McFarlane
from flask import Flask, render_template, request
import json
import urllib.request
import urllib.error
from keys import consumer_key

# Weather app that provides weather information for given city

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    """handles page not found error"""
    return render_template('404.html'), 404

@app.route('/', methods=['GET', 'POST'])
def weather():
    """main url"""
    if request.method == 'POST':
        # get typed city name
        city = request.form['city']
    else:
        # default name is los angeles
        city = 'los angeles'

    # OpenWeather API key
    api = consumer_key

    # get json data from api
    try:
        json_weather_data = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?units=imperial&q=' + city + '&appid=' + api).read()
    except urllib.error.URLError as e: return page_not_found(e)

    try:
        # convert weather JSON data to a list
        list_weather_data = json.loads(json_weather_data)

        # get city coordinates for UV data
        lat = str(int(list_weather_data['coord']['lat']))
        lon = str(int(list_weather_data['coord']['lon']))
        print(
            'http://api.openweathermap.org/data/2.5/uvi?appid=' +
            api + '&lat=' + lat + '&lon=' + lon)
        # get uv index data at location
        json_uv_data = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/uvi?appid=' +
            api + '&lat=' + lat + '&lon=' + lon).read()
    except urllib.error.URLError as e: return page_not_found(e)

    # convert uv JSON data to a list
    list_uv_data = json.loads(json_uv_data)

    # create dictionary from weather and uv data
    weather_data = {
        "country": str(list_weather_data['sys']['country']),
        "temp": str(list_weather_data['main']['temp']) + ' F',
        "weather_description": str(list_weather_data['weather'][0]['description']),
        "icon_link": str("http://openweathermap.org/img/wn/" + list_weather_data['weather'][0]['icon'] + "@2x.png"),
        "pressure": str(list_weather_data['main']['pressure']) + ' hPa',
        "humidity": str(list_weather_data['main']['humidity']) + '%',
        "city_name": str(list_weather_data['name']).lower(),
        "UV": str(list_uv_data['value'])
    }
    # load data to HTML format for display
    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
