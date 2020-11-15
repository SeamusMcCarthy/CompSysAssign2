#!/usr/bin/python3

import asyncio
import time
from kasa import SmartPlug # kasa library written to run via asyncio
from kasa import SmartBulb
async def main():
#   await plugUpd("192.168.68.103")
   await bulbUpd("192.168.68.118")

async def bulbUpd(bulb):
   b = SmartBulb(bulb) # define plug based on IP address
   await b.update() # update status
   print(b.alias) # device name
   await (b.turn_on())
   await b.update()
   print(b.is_on) # state
   time.sleep(5) 
   await (b.turn_off())
   await b.update()
   print(b.is_on) # state

if __name__ == "__main__":
   asyncio.run(main())


