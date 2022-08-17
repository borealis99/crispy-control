from machine import Pin
import time

last_stable = ( ( -1 , -1 ) , -1 ) # ((A,B),time)
last_change = ( ( -1 , -1 ) , -1 ) # ((A,B),time)
clicks = 0

def checkLast (pin_triggered, direction_triggered, a, b, ms=2):
    global last_stable
    global last_change
    t = time.ticks_ms()
    tpl = ( (a,b) , t )
    if a != b and t - last_change[1] > ms and last_change[0] != tpl[0] :
        last_change = tpl
        #print( last_stable, last_change)
        #print(a,b)
        return True
    elif a == b and t - last_stable[1] > ms and last_stable[0] != tpl[0] :
        last_stable = tpl
        #print( last_stable, last_change)
        #print(a,b)
        return True
    return False

def rotary(pin_triggered, a, b):
    global last_stable
    global last_change
    prev_stable = last_stable
    prev_change = last_change
    direction_triggered = (a,b)[pin_triggered]
    if not checkLast(pin_triggered, direction_triggered, a, b) :
        return False
    #print( "AB"[pin_triggered] , ("FALL", "RISE")[direction_triggered], a, b, time.ticks_ms())
    #print(prev_stable, prev_change)
    #print(last_stable, last_change)
    #if pin_triggered == 1 and direction_triggered == 0 and prev_stable[0] == (1,1) and prev_change[0] == (0,1):
    if pin_triggered == 1 and direction_triggered == 0 and prev_stable[0] != last_stable[0] and prev_change[0] == (0,1):
        global clicks
        clicks += 1
        #print("#####################################################################################",clicks)
    #elif pin_triggered == 0 and direction_triggered == 0 and prev_stable[0] == (1,1) and prev_change[0] == (1,0):
    elif pin_triggered == 0 and direction_triggered == 0 and prev_stable[0] != last_stable[0] and prev_change[0] == (1,0):
        global clicks
        clicks -= 1
        #print("#####################################################################################",clicks)
    #print('===============')

    # A RISE
    #if pin_triggered == 0 and direction_triggered == 1 :
    #    return True
        

pA = Pin(26, Pin.IN, Pin.PULL_DOWN)
pB = Pin(27, Pin.IN, Pin.PULL_DOWN)

pA.irq(lambda pin: rotary(0, pA.value(), pB.value()), Pin.IRQ_FALLING | Pin.IRQ_RISING)
pB.irq(lambda pin: rotary(1, pA.value(), pB.value()), Pin.IRQ_FALLING | Pin.IRQ_RISING)


while True:
    time.sleep(1)
    print(clicks)

