#!/usr/bin/python3

from flask import Flask, render_template, request
from flask_cors import CORS
from sense_hat import SenseHat
from firebase import firebase
from bluetooth import *
from datetime import datetime
from datetime import date
from urllib.request import urlopen
from gpiozero import MotionSensor
import time
import json
import os
import requests
import subprocess

# Setup Flask app
app = Flask(__name__)
CORS(app)

# Firebase DB details
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

# Setup and clear SenseHat
sense = SenseHat()
sense.clear()
sense.low_light = True

# Initialise working day and timestamps
# Total break times using 1900-01-01 but this doesn't matter as I only want the time portion
day="false"
break_start_time=""
total_scheduled_break_time = datetime.strptime("00:00:00","%H:%M:%S")
total_unscheduled_break_time = datetime.strptime("00:00:00","%H:%M:%S")

# Initialize vars to be populated once user is known. Need them defined globally.
user=""
TSapi=""
visual1=""
visual2=""
baseURL=""

# Main Route
@app.route('/workday')
def workday():
    getFirebase_data()
    env = getSense_data()

    templateData = {
       'devices' : devices,
       'temp' : env[0],
       'humid' : env[1],
       'chart1' : visual1,
       'chart2' : visual2,
       'breaks' : breaks,
       'day' : day
    }
    return render_template('main.html', **templateData)

# Handle change of device setting
@app.route('/workday/<device>/<action>')
def device_action(device, action):
    global devices

    device = int(device)
    if ((devices[device]['state'] == 'true' and action == 'off') 
    or (devices[device]['state'] == 'false' and action == 'on')):
       devices = toggle_device(device)

    getFirebase_data()
    env = getSense_data()
    templateData = {
        'devices' : devices,
        'temp' : env[0],
        'humid' : env[1],
        'chart1' : visual1,
        'chart2' : visual2,
        'breaks' : breaks,
        'day' : day
    }
    return render_template('main.html', **templateData)

# Manage starting/ending the working day
@app.route('/workday/day/<action>')
def day_action(action):
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
       end_date = datetime.now().strftime("%Y-%m-%d")
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

    getFirebase_data()
    env = getSense_data()
    templateData = {
        'devices' : devices,
        'temp' : env[0],
        'humid' : env[1],
        'chart1' : visual1,
        'chart2' : visual2,
        'breaks' : breaks,
        'day' : day
    }
    return render_template('main.html', **templateData)

# Manage taking a picture
@app.route('/workday/pic')
def take_pic():
    subprocess.Popen(["ssh", "%s" % "pi@192.168.68.117", "python3 pic.py"], shell=False)

    getFirebase_data()
    env = getSense_data()

    templateData = {
        'devices' : devices,
        'temp' : env[0],
        'humid' : env[1],
        'chart1' : visual1,
        'chart2' : visual2,
        'breaks' : breaks,
        'day' : day
    }
    return render_template('main.html', **templateData)



# Manage starting/ending a break
@app.route('/workday/break/<break_type>/<action>')
def break_action(break_type, action):
    global user
    global break_start_time
    global total_scheduled_break_time
    global total_unscheduled_break_time

    break_type = int(break_type)
#    getFirebase_data()
#    env = getSense_data()

    if breaks[break_type]['state'] == 'false' and action == 'on':
       breaks[break_type]['state'] = 'true'
       break_start_time = datetime.now().strftime("%H:%M:%S")

    if breaks[break_type]['state'] == 'true' and action == 'off':
       breaks[break_type]['state'] = 'false'
       break_end_time = datetime.now().strftime("%H:%M:%S")
       break_duration = datetime.strptime(break_end_time,"%H:%M:%S") - datetime.strptime(break_start_time,"%H:%M:%S")
       break_date = datetime.now().strftime("%Y-%m-%d")

       if break_type == 1:
          target = '/scheduled'
          total_scheduled_break_time += break_duration
       else:
          target = '/unscheduled'
          total_unscheduled_break_time += break_duration

       data = {
          'Date' : break_date,
          'Name' : user,
          'Start' : break_start_time,
          'End' : break_end_time
       }
       result = firebase.post(target, data)

    getFirebase_data()
    env = getSense_data()
    templateData = {
        'devices' : devices,
        'temp' : env[0],
        'humid' : env[1],
        'chart1' : visual1,
        'chart2' : visual2,
        'breaks' : breaks,
        'day' : day
    }
    return render_template('main.html', **templateData)

def setup_steps():
   global user
   global visual1
   global visual2
   global baseURL

# Setup PIR & wait for motion. 
# Need the wait outside of the main loop or it will execute each time the template code changes
   pir = MotionSensor(4)
   pir.wait_for_motion()

# Setup Bluetooth discovery
   print('Performing Bluetooth scan...')
   b = (0, 0, 255) #blue
   y = (255, 255, 0) #yellow
   btd = [
     y,y,y,b,y,y,y,y,
     y,y,y,b,b,y,y,y,
     y,b,y,b,y,b,y,y,
     y,y,b,b,b,y,y,y,
     y,y,y,b,y,y,y,y,
     y,y,b,b,b,y,y,y,
     y,b,y,b,y,b,y,y,
     y,y,y,b,b,y,y,y
   ]
   sense.set_pixels(btd)
   nearby_phones = discover_devices(lookup_names = True)
   sense.clear()

# List of MAC addresses and associated user details - name, Thingspeak channel, Matlab visualisations
   known_phones = {
     '88:BD:45:06:34:87': { 'uname' : 'Seamus', 'api' : '0GG6PVV1IBH096HV', 'mvis1' : '374478', 'mvis2' : '374485'},
     '12:23:34:45:56:67': { 'uname' : 'Tracy', 'api' : '0GG6PVV1IBH096HA', 'mvis1' : '374477', 'mvis2' : '374486'}
   }

   phones = []
   for addr, name in nearby_phones:
       phones.append(addr)

   for addr in phones:
       if addr in known_phones:
          user = known_phones[addr]['uname']
          print(user + " has logged on")
          baseURL='https://api.thingspeak.com/update?api_key=%s' % known_phones[addr]['api'] 
          visual1="https://thingspeak.com/apps/matlab_visualizations/%s" % known_phones[addr]['mvis1']
          visual2="https://thingspeak.com/apps/matlab_visualizations/%s" % known_phones[addr]['mvis2']

   if user == '':
      print('No user identified. Please check Bluetooth and try again')
      exit()

   sense.show_message("Hello " + user, text_colour=y, back_colour=b, scroll_speed=0.05)
   sense.clear()



def getSense_data():
    temp=round(sense.get_temperature(),2)
    humid=round(sense.get_humidity(),2)
    return temp, humid

def getFirebase_data():
    result = firebase.get('/scheduled', None)
    sbreaks = {}
    count = 1
    for item, value in result.items():
        if value['Date'] == str(date.today()) and value['Name'] == user:
           sbreaks.update({ count : {'start' : value['Start'], 'end' : value['End'] }})
           count = count + 1

    result = firebase.get('/unscheduled', None)
    ubreaks = {}
    count = 1
    for item, value in result.items():
        if value['Date'] == str(date.today()) and value['Name'] == user:
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
    setup_steps()
    #Run API on port 5000, set debug to false
    app.run(host='0.0.0.0', port=5000, debug=False)

