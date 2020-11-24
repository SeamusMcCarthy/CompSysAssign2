#!/usr/bin/python3

# Quart used instead of Flask as asyncio is required for kasa
# kasa no longer used for plugs but retain Quart in case fix is found
#from kasa import SmartPlug
#from kasa import SmartBulb

#from quart import Quart, render_template, request, flash
from flask import Flask, render_template, request, flash
#from quart_cors import cors
from flask_cors import CORS
from sense_hat import SenseHat
from firebase import firebase
from bluetooth import *
from datetime import datetime
import time
import json
import os
import asyncio
import requests

# Setup and clear SenseHat
sense = SenseHat()
sense.clear()

# Setup Quart app
#app = Quart(__name__)
#cors(app)
app = Flask(__name__)
CORS(app)
app.secret_key = b'_5_5_5_5_5_5xec]'

# Firebase
firebase = firebase.FirebaseApplication('https://compsys2020-154671.firebaseio.com/', None)

# Create a dictionary for smart devices
devices = {
   1 : {'name' : 'Dehumidifier', 'ip' : '192.168.68.103', 'state' : 'false', 'type' : 'plug'},
   2 : {'name' : 'Room Heater', 'ip' : '192.168.68.114', 'state' : 'false', 'type' : 'plug'},
   3 : {'name' : 'Do Not Disturb', 'ip' : '192.168.68.118', 'state' : 'false', 'type' : 'bulb'}
}

# Create a dictionary for breaks
breaks = {
   1 : {'name' : 'Scheduled', 'state' : 'false'},
   2 : {'name' : 'Unscheduled', 'state' : 'false'}
}

# Define Thingspeak visualisation URLs - Seamus
text1="https://thingspeak.com/apps/matlab_visualizations/374478"
text2="https://thingspeak.com/apps/matlab_visualizations/374485"

# Main Route
@app.route('/workday')
#async def workday():
def workday():
    getFirebase_data()
    env = getSense_data()

    templateData = {
       'devices' : devices,
       'temp' : env[0],
       'humid' : env[1],
       'chart1' : text1,
       'chart2' : text2,
       'breaks' : breaks
    }
#    await flash("Welcome to SHOM")
    flash("Welcome to SHOM")
#    return await render_template('main.html', **templateData)
    return render_template('main.html', **templateData)

@app.route('/workday/<device>/<action>')
#async def action(device, action):
def action(device, action):
    getFirebase_data()
    env = getSense_data()
    toggleDevice(device)

    templateData = {
        'devices' : devices,
        'temp' : env[0],
        'humid' : env[1],
        'chart1' : text1,
        'chart2' : text2,
        'breaks' : breaks
    }
#    return await render_template('main.html', **templateData)
    return render_template('main.html', **templateData)

def check_bluetooth():
   # Setup Bluetooth discovery
   print('Performing Bluetooth scan...')
   #nearby_phones = discover_devices(lookup_names = True)
   #print(nearby_phones)
   
   #known_phones = {
   #  '88:BD:45:06:34:87': 'Seamus'
   #} 
   
   #phones = []
   #for name, addr in nearby_phones:
   #    phones.append(name)
 
   #user = ''
   #for name in phones:
   #    if name in known_phones:
   #       print(known_phones[name])
   #       user = known_phones[name]

   #if user == '':
   #   print('No user identified. Please turn on Bluetooth and try again')
   #   exit()

def getSense_data():
    temp=round(sense.get_temperature(),2)
    humid=round(sense.get_humidity(),2)
    print(temp, humid)
    return temp, humid

def getFirebase_data():
    result = firebase.get('/scheduled', None)
    sbreaks = {}
    count = 1
    for item, value in result.items():
        sbreaks.update({ count : {'start' : value['Start'], 'end' : value['End'] }})
        count = count + 1

    result = firebase.get('/unscheduled', None)
    ubreaks = {}
    count = 1
    for item, value in result.items():
        ubreaks.update({ count : {'start' : value['Start'], 'end' : value['End'] }})
        count = count + 1

    breaks[1]['times'] = sbreaks
    breaks[2]['times'] = ubreaks

def toggleDevice(device):
    device = int(device)
    if device == 1:
       url = 'https://maker.ifttt.com/trigger/ToggleOffice1/with/key/bTQ6D-WnYUA6ZpK2vQ_95m'
       x = requests.post(url)

    if device == 2:
       url = 'https://maker.ifttt.com/trigger/ToggleOffice3/with/key/bTQ6D-WnYUA6ZpK2vQ_95m'
       x = requests.post(url)

    if device == 3:
       url = 'https://maker.ifttt.com/trigger/ToggleLight/with/key/bTQ6D-WnYUA6ZpK2vQ_95m'
       x = requests.post(url)

    if devices[device]['state'] == 'true':
       devices[device]['state'] = 'false'
    else: 
       devices[device]['state'] = 'true'

if __name__ == "__main__":
    check_bluetooth()
    #Run API on port 5000, set debug to true
    app.run(host='0.0.0.0', port=5000, debug=True)

