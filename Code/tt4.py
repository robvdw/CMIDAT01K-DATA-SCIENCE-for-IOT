import json
import time
import os
import psutil
import urllib2 as ul

lastConnectionTime = time.time() # Track the last connection time
lastUpdateTime = time.time() # Track the last update time
postingInterval = 120 # Post data once every 2 minutes
updateInterval = 15 # Update once every 15 seconds

writeAPIkey = "X2O0JB02Z2LN5W8E" # Replace YOUR-CHANNEL-WRITEAPIKEY with your channel write API key
channelID = "920549" # Replace YOUR-CHANNELID with your channel ID
url = "https://api.thingspeak.com/channels/"+channelID+"/bulk_update.json" # ThingSpeak server settings
messageBuffer = []

def httpRequest():
    '''Function to send the POST request to 
    ThingSpeak channel for bulk update.'''

    global messageBuffer
    data = json.dumps({'write_api_key':writeAPIkey,'updates':messageBuffer}) # Format the json data buffer
    req = ul.Request(url = url)
    requestHeaders = {"User-Agent":"mw.doc.bulk-update (Raspberry Pi)","Content-Type":"application/json","Content-Length":str(len(data))}
    for key,val in requestHeaders.iteritems(): # Set the headers
        req.add_header(key,val)
    req.add_data(data) # Add the data to the request
    # Make the request to ThingSpeak
    try:
        response = ul.urlopen(req) # Make the request
        print response.getcode() # A 202 indicates that the server has accepted the request
    except ul.HTTPError as e:
        print e.code # Print the error code
    messageBuffer = [] # Reinitialize the message buffer
    global lastConnectionTime
    lastConnectionTime = time.time() # Update the connection time
    
def getData():
    '''Function that returns the CPU temperature and percentage of CPU utilization'''
    cmd = '/opt/vc/bin/vcgencmd measure_temp'
    process = os.popen(cmd).readline().strip()
    cpuTemp = process.split('=')[1].split("'")[0]
    cpuUsage = psutil.cpu_percent(interval=2)
    return cpuTemp,cpuUsage

def updatesJson():
    '''Function to update the message buffer
    every 15 seconds with data. And then call the httpRequest 
    function every 2 minutes. This examples uses the relative timestamp as it uses the "delta_t" parameter. 
    If your device has a real-time clock, you can also provide the absolute timestamp using the "created_at" parameter.
    '''

    global lastUpdateTime
    message = {}
    message['delta_t'] = int(round(time.time() - lastUpdateTime))
    Temp,Usage = getData()
    message['field1'] = Temp
    message['field2'] = Usage
    global messageBuffer
    messageBuffer.append(message)
    
    
# If posting interval time has crossed 2 minutes update the ThingSpeak channel with your data
if time.time() - lastConnectionTime >= postingInterval:
        httpRequest()
        lastUpdateTime = time.time()

if __name__ == "__main__":  # To ensure that this is run directly and does not run when imported 
    while 1:
        # If update interval time has crossed 15 seconds update the message buffer with data
        if time.time() - lastUpdateTime >= updateInterval:
            updatesJson()

            httpRequest()