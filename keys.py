import os
from dotenv import load_dotenv
"""
Get consumer key variable for OpenWeather API
"""
# initialize keys from env
load_dotenv()
# retrieve key from environment variables
consumer_key = os.environ.get('WEATHER_CON_KEY')
