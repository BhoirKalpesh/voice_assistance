import requests
from config import *

api_address = "http://newsapi.org/v2/top-headlines?country=us&apiKey="+key

json_data = requests.get(api_address).json()

ar=[]

def news():
    for i in range(3):
        ar.append("Number "+ str(i+1)+", " + json_data["articles"][i]["title"]+".")

    return ar
