#!/usr/bin/python3

# Quart used instead of Flask as asyncio is required for kasa
# kasa no longer used to retain Quart in case fix is found
#from kasa import SmartPlug
from kasa import SmartBulb

from quart import Quart, render_template, request
from quart_cors import cors
from sense_hat import SenseHat
from firebase import firebase
from bluetooth import *
import time
import json
import os
import asyncio

# add config file?

# Setup Bluetooth discovery
print('Performing Bluetooth scan...')
nearby_phones = discover_devices(lookup_names = True)
print(nearby_phones)

known_phones = {
  '88:BD:45:06:34:87': 'Seamus'
} 

phones = []
for name, addr in nearby_phones:
    phones.append(name)

user = ''
for name in phones:
    if name in known_phones:
       print(known_phones[name])
       user = known_phones[name]
       break

if user == '':
   print('No user identified. Please turn on Bluetooth and try again')
   exit()


# Setup and clear SenseHat
sense = SenseHat()
sense.clear()

# Setup Quart app
app = Quart(__name__)
cors(app)

# Firebase
firebase = firebase.FirebaseApplication('https://compsys2020-154671.firebaseio.com/', None)

# Create a dictionary for smart devices
devices = {
   1 : {'name' : 'Do Not Disturb', 'ip' : '192.168.68.118', 'state' : 'false', 'type' : 'bulb'}
#   2 : {'name' : 'Dehumidifier', 'ip' : '192.168.68.103', 'state' : 'false', 'type' : 'plug'},
#   3 : {'name' : 'Heater', 'ip' : '192.168.68.114', 'state' : 'false', 'type' : 'plug'}
}

# Define Thingspeak visualisation URLs - Seamus
text1="https://thingspeak.com/apps/matlab_visualizations/374478"
text2="https://thingspeak.com/apps/matlab_visualizations/374485"



# Main Route
@app.route('/workday')
async def workday():
    result = firebase.get('/users', None)
    times = {}
    count = 1
    for item, value in result.items():
        times.update({ count : {'start' : value['Start'], 'end' : value['End'] }})
        count = count + 1

    temp=round(sense.get_temperature(),2)
    humid=round(sense.get_humidity(),2)

    for device in devices:
        ip = devices[device]['ip']
        print(ip)
        p = SmartBulb(ip)
        await p.update()
        print(p.alias)
        devices[device]['state'] = p.is_on
        print("Current state is " + str(devices[device]['state']))

    templateData = {
       'devices' : devices,
       'temp' : temp,
       'humid' : humid,
       'chart1' : text1,
       'chart2' : text2,
       'times' : times
    }

    return await render_template('main.html', **templateData)

@app.route('/workday/<device>/<action>')
async def action(device, action):
   result = firebase.get('/users', None)
   times = {}
   count = 1
   for item, value in result.items():
       times.update({ count : {'start' : value['Start'], 'end' : value['End'] }})
       count = count + 1
   temp=round(sense.get_temperature(),2)
   humid=round(sense.get_humidity(),2)

   device = int(device)
   deviceName = devices[device]['name']
   if action == 'on':
      p = SmartBulb(devices[device]['ip'])
      await (p.turn_on())
   if action == 'off':
   # turn off bulb
      p = SmartBulb(devices[device]['ip'])
      await (p.turn_off())

   for device in devices:
       ip = devices[device]['ip']
       p = SmartBulb(ip)
       await p.update()
       devices[device]['state'] = p.is_on

   templateData = {
       'devices' : devices,
       'temp' : temp,
       'humid' : humid,
       'chart1' : text1,
       'chart2' : text2,
       'times' : times
   }
   return await render_template('main.html', **templateData)



if __name__ == "__main__":
    #Run API on port 5000, set debug to true
    app.run(host='0.0.0.0', port=5000, debug=True)
