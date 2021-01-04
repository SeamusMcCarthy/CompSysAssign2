# Project Name: SHOM - Smart Home Office Management 
#### Student Name: Seamus McCarthy   Student ID: 20091380

#### Hardware used
- Raspberry Pi (x 2)
- Mini Black Hat Hack3r board (assembled)
- Sense Hat
- PIR sensor
- Pi Camera
- TP-Link HS100 Smart Plug (x 2)
- TP-Link KL130 Smart Bulb

#### Config requirements for running

- Crontab entries (main proc, killproc, ping for keepalive)
![alt text][CRON]
- Smart Devices dictionary

- Known Devices dictionary
![alt text][KD]

- IFTTT setup
![alt text][IFTTT]

- Second Pi setup (requires SSH keys to be generated)
![alt text][2ndPI]

[KD]: https://github.com/SeamusMcCarthy/CompSysAssign2/blob/master/doc_images/KnownDevices.jpg "Known devices definition"
[IFTTT]: https://github.com/SeamusMcCarthy/CompSysAssign2/blob/master/doc_images/IFTTT.jpg "IFTTT applet calling"
[2ndPI]: https://github.com/SeamusMcCarthy/CompSysAssign2/blob/master/doc_images/SecondPi.jpg "Call to 2nd Pi"
[CRON]: https://github.com/SeamusMcCarthy/CompSysAssign2/blob/master/doc_images/crontab.jpg "Crontab entries"
