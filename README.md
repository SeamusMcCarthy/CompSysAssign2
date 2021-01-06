# Project Name: SHOM - Smart Home Office Management 
#### Student Name: Seamus McCarthy   Student ID: 20091380

### Contents

This document contains the list of hardware components used, where config changes may need to be applied for new users/devices and instructions on how to use the SHOM application.

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

#### Instructions

When the app is first started, the Sense Hat will display the Bluetooth image to inform the user that the Raspberry Pi is searching for devices.
*Ensure Bluetooth is switched in order for your device to be detected*

![][BT]

If no known device is found, an error message is displayed and the process stops.
If a known device is identified, the user details are pulled from the user dictionary. The user is then greeted on the display and the web app is started at which point they can proceed to http://192.168.xx.xx:5000/workday (where 192.168.xx.xx represents the IP address of the Raspberry Pi) to reach the main page

![][MAIN]
![][SNAP]

From here, the user can
- start and end their working day using the button in the top-right corner
- view the environmental readings of the office environment
- toggle the state of the Smart Devices configured in the above dictionary
- record the scheduled and unscheduled break times
- view these user & day specific records in both table and timeline formats
- view a graphical representation of their last 7 start/end times and total break durations
- view/take snapshots of a remote part of the home via the camera attached to the 2nd Pi.

Once the working day is complete, the user must end their day using the button in the top-right corner. This facilitates the posting of the statistical data to the Thingspeak channel defined in the user dictionary.

[KD]: https://github.com/SeamusMcCarthy/CompSysAssign2/blob/master/doc_images/KnownDevices.jpg "Known devices definition"
[SD]: https://github.com/SeamusMcCarthy/CompSysAssign2/blob/master/doc_images/SmartDevices.jpg "Smart devices definition"
[IFTTT]: https://github.com/SeamusMcCarthy/CompSysAssign2/blob/master/doc_images/IFTTT.jpg "IFTTT applet calling"
[2ndPI]: https://github.com/SeamusMcCarthy/CompSysAssign2/blob/master/doc_images/SecondPi.jpg "Call to 2nd Pi"
[CRON]: https://github.com/SeamusMcCarthy/CompSysAssign2/blob/master/doc_images/crontab2.jpg "Crontab entries"
[PIRW]: https://github.com/SeamusMcCarthy/CompSysAssign2/blob/master/doc_images/PIRWiring.jpg "PIR Wiring"
[BT]: https://github.com/SeamusMcCarthy/CompSysAssign2/blob/master/doc_images/BT.jpg "Bluetooth detection"
[MAIN]: https://github.com/SeamusMcCarthy/CompSysAssign2/blob/master/doc_images/Main.jpg "Main Page"
[SNAP]: https://github.com/SeamusMcCarthy/CompSysAssign2/blob/master/doc_images/Snapshot.jpg "Snapshot"
