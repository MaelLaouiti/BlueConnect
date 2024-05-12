from grove_rgb_lcd import *
import datetime
from datetime import date


setRGB(82,151,174)
for a in range(0,1):
    setText("  BlueConnect!"  )
    time.sleep(3)
    
#setText(format(str(current_time)))

def setup():
    pass

def loop():
    current_time = datetime.datetime.now()
    setText("   {}/{}/{}     Il est {}:{}  ".format(current_time.year, current_time.month, current_time.day, current_time.hour,current_time.minute))
    time.sleep(10)
    setRGB(30,30,30)

if __name__=="__main__":
    setup()
    while True:
        loop()
