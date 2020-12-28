from picamera import PiCamera
import datetime
import storeFileFB

camera = PiCamera()
camera.start_preview()
frame = 1

fileLoc = f'/home/pi/week10/img/frame{frame}.jpg' # set location of image file and current time
currentTime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

camera.capture(fileLoc) # capture image and store in fileLoc
print(f'frame {frame} taken at {currentTime}') # print frame number to console
storeFileFB.store_file(fileLoc)
storeFileFB.push_db(fileLoc, currentTime)
frame += 1
