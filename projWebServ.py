#!/usr/bin/python3

from flask import Flask, render_template, request
from flask_cors import CORS
from sense_hat import SenseHat
from kasa import SmartPlug
import time
import json
import os
import asyncio
# Setup and clear SenseHat
sense = SenseHat()
sense.clear()

# Setup Flask app
app = Flask(__name__)
CORS(app)

# Create a dictionary for smart devices
devices = {
   1 : {'name' : 'Office 1', 'ip' : '192.168.68.103', 'state' : 'false'},
   2 : {'name' : 'Office 2', 'ip' : '192.168.68.114', 'state' : 'false'}
}


# Main Route
#@app.route('/workday',methods=['GET'])
@app.route('/workday')
async def workday():
#    temp=round(sense.get_temperature(),2)
#    humid=round(sense.get_humidity(),2)

    for device in devices:
        ip = devices[device]['ip']
        print(ip)
        p = SmartPlug(ip)
        await p.update()
        print(p.alias)
        print(p.is_on) 
#        devices[device]['state'] = p.is_on
#        print("Current state is " + devices[device]['state'])

    text1="<div><iframe width='450' height='260' style='border: 1px solid' src='https://thingspeak.com/apps/matlab_visualizations/374478'></iframe></div>"
    text2="<iframe width='450' height='260' style='border: 1px solid' src='https://thingspeak.com/apps/matlab_visualizations/374485'></iframe>"
#    os.system('python3 plugtest.py')
    return text1+text2+"\n"
    

if __name__ == "__main__":
    #Run API on port 5000, set debug to true
    app.run(host='0.0.0.0', port=5000, debug=True)
