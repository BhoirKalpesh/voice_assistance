import pyttsx3 as p
import speech_recognition as sr
from selenium_web import *
from YT import *
from news import *
import randfacts
from jokes import *
from weather import *
from config import *
import datetime

engine = p.init()
rate = engine.getProperty('rate')
engine.setProperty('rate',160)
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
def speak(text):
    engine.say(text)
    engine.runAndWait()
def greet_user():
    current_hour = datetime.datetime.now().hour

    if 5 <= current_hour < 12:
        greeting = "Good morning"
    elif 12 <= current_hour < 18:
        greeting = "Good afternoon"
    elif 18 <= current_hour < 22:
        greeting = "Good evening"
    else:
        greeting = "Good night"
    return greeting

greet_user()

r = sr.Recognizer()
speak(f"Hello sir,{greet_user()}")
speak("I am your voice assistant.")
speak("What can i do for you")
def listen_and_recognize():
    attempts = 0

    while attempts < 3:
        with sr.Microphone() as source:
            r.energy_threshold = 4000
            r.adjust_for_ambient_noise(source, 1.2)
            print("Listening...")
            audio = r.listen(source)
            try:
                text2 = r.recognize_google(audio)
                print(text2)
                return text2
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
                speak("Sorry, I could not understand the audio.")
                attempts += 1

    print("Maximum attempts reached. Exiting...")
    return None

"""
text = listen_and_recognize()
if "what" and "about" and "you" in text:
    speak("i am also having a good day sir")
speak("What can i do for you")"""

text2 = listen_and_recognize()

while True:
    if text2:
        if "information" in text2:
            speak("you need information related to which topic?")
            infor=listen_and_recognize()
            if infor:
                print("searching {} in wikipedia".format(infor))
                speak("searching {} in wikipedia".format(infor))

                assist = Infow()
                assist.get_info(infor)
            text2 = listen_and_recognize()

        elif "play" and "video" in text2:
            speak("you want me to play which video?")
            vid = listen_and_recognize()
            if vid:
                print("Playing {} an youtube".format(vid))
                speak("Playing {} on youtube".format(vid))
                assist = Music()
                assist.play(vid)

            text2 = listen_and_recognize()

        elif "news" in text2:
            print("Sure sir, Now i will read news for you?")
            speak("Sure sir, Now i will read news for you?")
            arr = news()
            for i in range(len(arr)):
                print(arr[i])
                speak(arr[i])

            text2 = listen_and_recognize()

        elif "joke" and "jokes" in text2:
            speak("sure sir, get ready for some chuckles")
            print(text2)
            arr=joke()
            print(arr[0])
            speak(arr[0])
            print(arr[1])
            speak(arr[1])

            text2 = listen_and_recognize()

        elif "facts" in text2 or "fact" in text2:
            speak("sure sir, ")
            x=randfacts.get_fact()
            print(x)
            speak("Did you know that, "+x)
            text2 = listen_and_recognize()

        elif "weather" in text2 or "temperature" in text2:
            speak("Sure, tell me the city name.")
            city_name = process_user_input()

            if city_name:
                weather_data = get_weather_data(city_name)
                if weather_data:
                    temperature = get_temperature(weather_data)
                    description = get_description(weather_data)
                    if temperature is not None and description is not None:
                        print(f"The weather in {city_name} is {description} with a temperature of {temperature:.1f} degrees Celsius.")
                        speak(f"The weather in {city_name} is {description} with a temperature of {temperature:.1f} degrees Celsius.")
                    else:
                        print("Error: Could not retrieve complete weather information.")
                        speak("Error: Could not retrieve complete weather information.")
                else:
                    print(f"Error: Could not retrieve weather data for {city_name}.")
                    speak(f"Error: Could not retrieve weather data for {city_name}.")
            else:
                print("Could not understand the city name. Please try again.")
                speak("Could not understand the city name. Please try again.")

            text2 = listen_and_recognize()

        elif "exit" in text2.lower():
            print("Exiting...\nGood Bye")
            speak("good bye")
            break

        else:
            import os
            import google.generativeai as genai
            genai.configure(api_key=openai_api_key)

            # Create the model
            # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
            generation_config = {
                "temperature": 0.5,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 192,
                "response_mime_type": "text/plain",
            }

            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
            ]
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                safety_settings=safety_settings,
                generation_config=generation_config,
            )
            chat_session = model.start_chat(
                history=[
                ]
            )
            response = chat_session.send_message(text2)
            ans = response.text
            cleaned_ans = ans.replace('*','')
            print(cleaned_ans)
            speak(cleaned_ans)

            text2=listen_and_recognize()