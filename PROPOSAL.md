# Project Name: SHOM - Smart Home Office Management 
#### Student Name: Seamus McCarthy   Student ID: 20091380

Given that so many people currently affected by the pandemic are now working from home, my project will be a Smart Home Office Management 
system for remote workers. The project will have several functions : 

 - Monitor the office environment for temperature and humidity readings
 - Allow the user to react to and alter these levels 
 - Display & Record working hours
 - Display & Record scheduled and unscheduled breaks
 - Provide a 'Do Not Disturb' system to minimise interruptions

The office environment controls will allow the user to respond to temperature and humidity readings by remotely controlling a heater
and dehumidifier to maintain healthy levels.

The recorded working hours and breaks will be presented to the user in graph form and allow them to identify if home life is interfering with work 
responsibilities or whether work is intruding on home life. Ultimately, it may identify unnoticed "work from home" patterns that will allow 
the user to more effectively plan their schedule around situations that would not occur in an actual office environment.

In the absence of actual meeting rooms, the 'Do Not Disturb' function will provide a convenient visual means of letting family members know that 
you are in a situation where disturbances might be disruptive. In order to achieve this, a colour changing light can be placed outside the office 
and controlled wirelessly so that, for example, a red light indicates that you are on a call or a green light suggests that you're available. 

## Tools, Technologies and Equipment

Physical devices - Raspberry Pi, SenseHat, TP-Link Smart Plugs & Bulb

The solution will involve a Python webservice running on the Raspberry Pi. When a HTTP request is received, the webservice renders a HTML page, which utilises 
Jinja templating and some Javascript visuals, and will display the various environment levels, working time details and controls. The controls will allow
the user to switch on/off certain devices and start/stop the timers around working hours and break lengths.

The python-kasa package makes use of the proprietary TP-Link Smart Home protocol to communicate with the plugs and bulb. As python-kasa utilises asyncio, I 
will have to change the webservice from Flask to Quart. Similarly, I will have to use quart_cors rather than CORS.

The working day start/end times and break lengths will be written to a Thingspeak channel at the end of the working day and I will create MATLAB Visualisations 
so that the start/end times are contained within a single chart and similarly, the scheduled and unscheduled break lengths will be charted together. The public 
URLs for both of these Visualisations will be used to display the graphs on the webpage for analysis by the user.



