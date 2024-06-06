import requests
from config import *

#weather_api_key = "f8ae60e75445be1098f5e9f6c2a7335c"

def get_weather_data(city_name):
    api_address = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_api_key}"
    try:
        response = requests.get(api_address)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: An error occurred during the API request: {e}")
        return None

def process_user_input():

    import speech_recognition as sr  # Import speech recognition library

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak the city name:")
        audio = r.listen(source)

    try:
        # Improve error handling and feedback for incorrect recognition
        w = r.recognize_google(audio)
        if not w:
            print("Could not understand your input. Please try again.")
            return process_user_input()  # Recursively call to get valid input
        else:
            return w.capitalize()  # Capitalize the first letter
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return process_user_input()  # Recursively call to get valid input
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None  # Indicate failure to get city name

def get_temperature(weather_data):

    if weather_data:
        try:
            return round(weather_data["main"]["temp"] - 273.15, 1)  # Convert to Celsius
        except (KeyError, TypeError):
            print("Error: Could not extract temperature from weather data.")
            return None
    else:
        return None

def get_description(weather_data):

    if weather_data:
        try:
            return weather_data["weather"][0]["description"]
        except (KeyError, TypeError):
            print("Error: Could not extract description from weather data.")
            return None
    else:
        return None

