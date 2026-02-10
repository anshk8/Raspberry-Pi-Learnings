from gpiozero import LED
import time

'''
NOTES:
- When using 5V Pin, I used a resistor to connect the LED to the ground. This is to prevent the LED from burning out due to too much current.
- When using GPIO Pin, I did not use a resistor because the GPIO pins provide a limited current, which is safe for most LEDs. 

'''

#Which GPIO pin the LED is connected to
light = LED(4)

#Toggle On
light.on()

time.sleep(2)

light.off()