# needed sudo apt-get install libbluetooth3 before could run pybluez
from bluetooth import *

print("performing inquiry...")

nearby_devices = discover_devices(lookup_names = True)

#print("found %d devices" % len(nearby_devices))


known_devices = {}
known_devices = {'88:BD:45:06:34:87': 'Seamus'}

devices = []
for name, addr in nearby_devices:
     print( " %s - %s" % (addr, name))
     devices.append(name)

#print(nearby_devices)
#print(devices)
for name in devices:
   if name in known_devices:
#if '88:BD:45:06:34:87' in devices:
      print(known_devices[name])
 
