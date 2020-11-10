#!/usr/bin/python3

import json
import time
import asyncio
from urllib.request import urlopen
from sense_hat import SenseHat
from multiprocessing import Process
from kasa import SmartPlug

#async def main():
#
#   await p.update()
#   print(p.alias)
#
#   await (p.turn_on())
#   time.sleep(5)
#   await (p.turn_off())
#
#if __name__ == "__main__":
#   asyncio.run(main())
####

#sense = SenseHat()
#sense.clear()

#   for event in sense.stick.get_events():
#       if(event.action=='pressed'):
#          if (event.direction=='up'):
#             print('You selected channel ' + event.direction)
#          if (event.direction=='down'):
#             print('You selected channel ' + event.direction)
#          if (event.direction=='left'):
#             print('You selected channel ' + event.direction)
#          if (event.direction=='right'):
#             print('You selected channel ' + event.direction)
#          if (event.direction=='middle'):
#                 print('In here ' + str(pedal))

####

#WRITE_API_KEY='TQ0J17EP6L66NKX0'

#baseURL='https://api.thingspeak.com/update?api_key=%s' % WRITE_API_KEY

#startTemp = time.time()
#startHumid = time.time()

def writeTempData(temp):
   # Sending the data to thingSpeak in the query string
   # conn = urlopen(baseURL + '&field1=%s' % (temp))
   print('Temp = ' + str(temp))
   # print(conn.read())
   # Closing the connection
   # conn.close()


def writeHumidityData(humid):
      print('Humidity = ' + str(humid))

async def plug():
   p = SmartPlug("192.168.68.103")
   await p.update()
   print(p.alias)

   await p.turn_on()
   time.sleep(5)
   await p.turn_off()


def logTimes():
   while True:
     for event in sense.stick.get_events():
       if(event.action=='pressed'):
          if (event.direction=='up'):
             print('You selected channel ' + event.direction)
          if (event.direction=='down'):
             print('You selected channel ' + event.direction)
          if (event.direction=='left'):
             print('You selected channel ' + event.direction)
          if (event.direction=='right'):
             print('You selected channel ' + event.direction)
          if (event.direction=='middle'):
                 print('In here ' + event.direction)


if __name__ == '__main__':
   sense = SenseHat()
   sense.clear()

#   logTimes()
   asyncio.run(plug())



#   while True:
#      temp=round(sense.get_temperature(),2)
#      humid=round(sense.get_humidity(),2)
#      elapsed = round(time.time(),0)
#      p1 = Process(target=writeTempData, args=(temp,))
#      p2 = Process(target=writeHumidityData, args=(humid,))
#      p3 = Process(target=logTimes, args=(,))
#      if (elapsed - startTemp) > 5:
#         p1.start()
#         startTemp = elapsed
#      if (elapsed - startHumid) > 10:
#         p2.start()
#         startHumid = elapsed
      
   
