from gpiozero import Buzzer, Button
import time


#Buzzer is at GPIO pin 17 and Button is at 18
buzzer = Buzzer(17)
button = Button(18)

def buzz():
    buzzer.on()
    
def off():
    buzzer.off()
    
    
def loop():
    button.when_pressed = buzz
    button.when_released = off
    while True:
        time.sleep(1)
        
        
def main():
    try:
        loop()
         
    except KeyboardInterrupt:
        buzzer.close()
        button.closer()

#buzzer.close()
main()