# Project Name: SHOM - Smart Home Office Management 
#### Student Name: Seamus McCarthy   Student ID: 20091380

### Intro

This document contains the list of hardware components used, where config changes may need to be applied and instructions on how to use the SHOM application.

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
![][CRON]

- Smart Devices dictionary
![][SD]
- Known Devices dictionary
![][KD]

- IFTTT setup
![][IFTTT]

- Second Pi setup (requires SSH keys to be generated)
![][2ndPI]

- PIR Wiring (for GPIO pin 4)
![][PIRW]

[KD]: https://github.com/SeamusMcCarthy/CompSysAssign2/blob/master/doc_images/KnownDevices.jpg "Known devices definition"
[SD]: https://github.com/SeamusMcCarthy/CompSysAssign2/blob/master/doc_images/SmartDevices.jpg "Smart devices definition"
[IFTTT]: https://github.com/SeamusMcCarthy/CompSysAssign2/blob/master/doc_images/IFTTT.jpg "IFTTT applet calling"
[2ndPI]: https://github.com/SeamusMcCarthy/CompSysAssign2/blob/master/doc_images/SecondPi.jpg "Call to 2nd Pi"
[CRON]: https://github.com/SeamusMcCarthy/CompSysAssign2/blob/master/doc_images/crontab.jpg "Crontab entries"
[PIRW]: https://github.com/SeamusMcCarthy/CompSysAssign2/blob/master/doc_images/PIRWiring.jpg "PIR Wiring" {:height="50%" width="50%"}
