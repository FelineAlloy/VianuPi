from pathlib import Path
import picamerax
import picamerax.array
from time import sleep
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import sys
import numpy as np
from PIL import Image

def take_picture(i, lum):
    with picamerax.array.PiBayerArray(cam) as stream:
        
        now_time = datetime.now()
        
        cam.capture(stream, 'jpeg', bayer=True)
        
        print(f'capture time: {datetime.now()-now_time}')
        
        output = (stream.demosaic() >> 2).astype(np.uint8)
        img = Image.fromarray(output)
        img.save(f'{lum:03d}_{i:03d}.png')
        cam.capture(f'{lum:03d}_{i:03d}.jpg', resize=(100, 100))


led = 40
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led, GPIO.OUT)
pwm = GPIO.PWM(led, 1000)
pwm.start(0)

baseFolder = Path(__file__).parent.resolve()

width = 4056
height = 3040

exp = 8
iso = 800

cam = picamerax.PiCamera(framerate=1/exp)

sleep(2)

cam.resolution = (width, height)
cam.exposure_mode = "verylong"
cam.iso = iso
cam.shutter_speed = int(exp * 1_000_000) #set in (1e-6 s)


for lum in range(10):
    print(f'lum = {lum}')
    for i in range(1, 5):
        
        pwm.ChangeDutyCycle(lum)
        take_picture(i, lum)