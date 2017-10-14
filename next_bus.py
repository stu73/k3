from __future__ import print_function
import requests
import json
import dateutil.parser
from datetime import datetime
import pytz
import os


# Query TFL API

resp = requests.get('https://api.tfl.gov.uk/StopPoint/40004405165B/Arrivals')
parsed_resp = json.loads(resp.text)

if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))

# Parse Reponse
    
expectedArrival = dateutil.parser.parse(parsed_resp[0]['expectedArrival'])

busNumberPlate = parsed_resp[0]['vehicleId']

currentTime = datetime.now(pytz.timezone('Europe/London'))

timeUntil = expectedArrival - datetime.now(pytz.timezone('Europe/London'))

secs = timeUntil.total_seconds()
hours = int(secs / 3600)
minutes = int(secs / 60) % 60

# Print details

print('Current time : ',currentTime.strftime('%H:%M:%S'))
print('Time until K3 bus (number plate ',busNumberPlate,'): ',minutes,'min\n')

# Get to the bus stop!

if(minutes < 10):
    print("Hurry up to bus stop!\n")

# Flash lights on Unicorn Hat on Raspberry Pi
    
if(minutes == 10):
	os.system('sudo python /home/pi/k3/bus_sparkles.py')

# Write k3 bus details to file

with open("/home/pi/k3/timeUntil.txt", "w") as text_file:
    text_file.write("{0},{1},{2}".format(minutes,busNumberPlate,currentTime.strftime('%H:%M:%S')))
