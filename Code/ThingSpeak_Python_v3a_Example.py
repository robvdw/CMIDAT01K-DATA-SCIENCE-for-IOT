import json
import time
import os
import psutil
import requests



writeAPIkey = "X2O0JB02Z2LN5W8E" # Replace YOUR-CHANNEL-WRITEAPIKEY with your channel write API key
channelID = "920549" # Replace YOUR-CHANNELID with your channel ID
#url = "https://api.thingspeak.com/channels/"+channelID+"/bulk_update.json" # ThingSpeak server settings

url= "https://api.thingspeak.com/update"
messageBuffer = []


queries = {"api_key": "X2O0JB02Z2LN5W8E",
            "field1": 120,
            "field2": 80}

r = requests.get(url, params=queries)
if r.status_code == requests.codes.ok:
    print("Data Received!")
else:
    print("Error Code: " + str(r.status_code))
