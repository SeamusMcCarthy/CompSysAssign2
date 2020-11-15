#!/usr/bin/python3

# Quart used instead of Flask as asyncio is required for kasa
from quart import Quart, render_template, request
from quart_cors import cors
from sense_hat import SenseHat
#from kasa import SmartPlug
from kasa import SmartBulb
from firebase import firebase
import time
import json
import os
import asyncio
# add config file?

# Setup and clear SenseHat
sense = SenseHat()
sense.clear()

# Firebase
firebase = firebase.FirebaseApplication('https://compsys2020-154671.firebaseio.com/', None)
result = firebase.get('/users', None)
times = {}
count = 1
for item, value in result.items():
    times.update({ count : {'start' : value['Start'], 'end' : value['End'] }})
    count = count + 1

print(times)

# Setup Quart app
app = Quart(__name__)
cors(app)

# Create a dictionary for smart devices
devices = {
   1 : {'name' : 'Do Not Disturb', 'ip' : '192.168.68.118', 'state' : 'false'}
#   2 : {'name' : 'Dehumidifier', 'ip' : '192.168.68.103', 'state' : 'false'}
}
print(devices)
# Define Thingspeak visualisation URLs
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
