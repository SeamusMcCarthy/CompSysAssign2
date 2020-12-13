#!/usr/bin/python3

# Quart used instead of Flask as asyncio is required for kasa
# kasa no longer used for plugs but retain Quart in case fix is found
#from kasa import SmartPlug
#from kasa import SmartBulb

#from quart import Quart, render_template, request, flash
#from quart_cors import cors
from flask import Flask, render_template, request, flash
from flask_cors import CORS
from sense_hat import SenseHat
from firebase import firebase
from bluetooth import *
from datetime import datetime
from urllib.request import urlopen
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
# Needed for flash
#app.secret_key = b'_5_5_5_5_5_5xec]'

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

# Define Thingspeak channel API
WRITE_API_KEY='0GG6PVV1IBH096HV'
baseURL='https://api.thingspeak.com/update?api_key=%s' % WRITE_API_KEY

# Define Thingspeak visualisation URLs - Seamus
text1="https://thingspeak.com/apps/matlab_visualizations/374478"
text2="https://thingspeak.com/apps/matlab_visualizations/374485"

# Initialise working day and timestamps
day="false"
break_start_time=""
total_scheduled_break_time = datetime.strptime("00:00:00","%H:%M:%S")
total_unscheduled_break_time = datetime.strptime("00:00:00","%H:%M:%S")
print(total_scheduled_break_time)
print(total_unscheduled_break_time)

user=""

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
       'breaks' : breaks,
       'day' : day
    }
    return render_template('main.html', **templateData)

@app.route('/workday/<device>/<action>')
def device_action(device, action):
    getFirebase_data()
    env = getSense_data()
    global devices
    device = int(device)
    if ((devices[device]['state'] == 'true' and action == 'off') 
    or (devices[device]['state'] == 'false' and action == 'on')):
       devices = toggle_device(device)

    templateData = {
        'devices' : devices,
        'temp' : env[0],
        'humid' : env[1],
        'chart1' : text1,
        'chart2' : text2,
        'breaks' : breaks,
        'day' : day
    }
    return render_template('main.html', **templateData)

@app.route('/workday/day/<action>')
def day_action(action):
    getFirebase_data()
    env = getSense_data()
    global start_time
    global day
    if day == 'false' and action == 'on':
       day = 'true'
       start_time_hr = int(datetime.now().strftime("%H"))
       start_time_mn = int(datetime.now().strftime("%M"))
       start_time_sc = int(datetime.now().strftime("%S"))
       start_time = str(round(start_time_hr + ((start_time_mn * 60 + start_time_sc) / 3600),2))

    if day == 'true' and action == 'off':
       day = 'false'
       end_time_hr = int(datetime.now().strftime("%H"))
       end_time_mn = int(datetime.now().strftime("%M"))
       end_time_sc = int(datetime.now().strftime("%S"))
       end_time = str(round(end_time_hr + ((end_time_mn * 60 + end_time_sc) / 3600),2))
       end_date = datetime.now().strftime("%Y-%M-%d")
       end_date = end_date + "T00:00:00Z"

       sch_hr = int(total_scheduled_break_time.strftime("%H")) * 60
       sch_mn = int(total_scheduled_break_time.strftime("%M"))
       sch_sc = round((int(total_scheduled_break_time.strftime("%S")) / 60),0)
       sch_tot = str(sch_hr + sch_mn + sch_sc)

       unsch_hr = int(total_unscheduled_break_time.strftime("%H")) * 60
       unsch_mn = int(total_unscheduled_break_time.strftime("%M"))
       unsch_sc = round((int(total_unscheduled_break_time.strftime("%S")) / 60),0)
       unsch_tot = str(unsch_hr + unsch_mn + unsch_sc)

       conn = urlopen(baseURL + '&field1=%s&field2=%s&field3=%s&field4=%s&created_at="%s"' % (start_time, end_time, sch_tot, unsch_tot, end_date))

    templateData = {
        'devices' : devices,
        'temp' : env[0],
        'humid' : env[1],
        'chart1' : text1,
        'chart2' : text2,
        'breaks' : breaks,
        'day' : day
    }
    return render_template('main.html', **templateData)

@app.route('/workday/break/<break_type>/<action>')
def break_action(break_type, action):
    global user
    global break_start_time
    global total_scheduled_break_time
    global total_unscheduled_break_time

    break_type = int(break_type)
    getFirebase_data()
    env = getSense_data()

    if breaks[break_type]['state'] == 'false' and action == 'on':
       breaks[break_type]['state'] = 'true'
       break_start_time = datetime.now().strftime("%H:%M:%S")

    if breaks[break_type]['state'] == 'true' and action == 'off':
       breaks[break_type]['state'] = 'false'
       break_end_time = datetime.now().strftime("%H:%M:%S")
       break_duration = datetime.strptime(break_end_time,"%H:%M:%S") - datetime.strptime(break_start_time,"%H:%M:%S")
       print(break_start_time + " " + break_end_time)
       break_date = datetime.now().strftime("%Y-%m-%d")
       if break_type == 1:
          target = '/scheduled'
          total_scheduled_break_time += break_duration
       else:
          target = '/unscheduled'
          total_unscheduled_break_time += break_duration

       print(total_scheduled_break_time)
       print(total_unscheduled_break_time)

       data = {
          'Date' : break_date,
          'Name' : user,
          'Start' : break_start_time,
          'End' : break_end_time
       }
       result = firebase.post(target, data)

    templateData = {
        'devices' : devices,
        'temp' : env[0],
        'humid' : env[1],
        'chart1' : text1,
        'chart2' : text2,
        'breaks' : breaks,
        'day' : day
    }
    return render_template('main.html', **templateData)

def check_bluetooth():
   # Setup Bluetooth discovery
   print('Performing Bluetooth scan...')
   global user
   user='Seamus'
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

def toggle_device(device):
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

    return devices

if __name__ == "__main__":
    check_bluetooth()
    #Run API on port 5000, set debug to true
    app.run(host='0.0.0.0', port=5000, debug=True)

