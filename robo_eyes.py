import board
import time

from random import randint

from PIL import Image, ImageSequence, ImageDraw
from adafruit_ht16k33.matrix import Matrix8x8


blinkCountdown = 100 # Countdown to next blink (in frames)
gazeCountdown  =  75 # Countdown to next eye movement
gazeFrames     =  50 # Duration of eye movement (smaller = faster)

eyeX = 3
eyeY = 3   # Current pupil position

newX = 3
newY = 3   # Next pupil position

dX   = 0
dY   = 0   # Distance from prior to new position

i2c = board.I2C
matrix = Matrix8x8(i2c)
matrix2 = Matrix8x8(i2c, address=0x71)

#set brightness to lowest setting, increase up to maximum 1 if needed
matrix.brightness(0)
matrix2.brightness(0)

while True: #main loop
    #open the bitmap GIF and create an iterator
    blinkSeq = Image.open('/home/thommorley/pi_eyes/blink.gif')
    blinkImg = ImageSequence.Iterator(blinkSeq)
    
    blinkCountdown -= 1
    gazeCountdown -= 1
        
    if blinkCountdown < 9:
        img = blinkImg[blinkCountdown]
    else:
        img = blinkImg[0]
       
    draw = ImageDraw.Draw(img)
    
    if gazeCountdown <= gazeFrames:
        interX = int(newX - (dX * gazeCountdown/gazeFrames))
        interY = int(newY - (dY * gazeCountdown/gazeFrames))
        draw.rectangle((interX, interY, interX+1, interY+1), outline=0, fill=0)
        
        if gazeCountdown == 0:
            eyeX = newX
            eyeY = newY
                    
            while True:  # Pick random positions until one is within the eye circle
                newX = randint(0,6)
                newY = randint(0,6)
                
                if newX < 2:
                    if newY < 2:
                        continue
                    elif newY > 5:
                        continue
                elif newX > 5:
                    if newY < 2:
                        continue
                    elif newY > 5:
                        continue
                else:
                    break
            dX = newX - eyeX
            dY = newY - eyeY
            gazeFrames = randint(3, 10)
            gazeCountdown = randint(gazeFrames, 120)
            
    else:
        draw.rectangle((eyeX, eyeY, eyeX+1, eyeY+1), outline=0, fill=0)
    
    matrix.image(img.rotate(270))
    matrix2.image(img.rotate(90))
    
    
    blinkSeq.close()
    
    if blinkCountdown == 0:
        blinkCountdown = randint(5, 180)
    
    time.sleep(.01)
