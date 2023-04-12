#!/usr/bin/python

import struct 
import os
import time
import threading
import l5p_kbl

MODIFIER_KEYS = {42, 29, 56, 100, 97, 54}
REENABLE_DELAY_TOUCHPAD = 0.3
REENABLE_DELAY_RGB = 5
RGB_COLOR = '204080'

controller = l5p_kbl.LedController()
rgb_on = controller.build_control_string(
	effect='static',
	colors=[RGB_COLOR,RGB_COLOR,RGB_COLOR,RGB_COLOR],
	speed=1,
	brightness=1,
	wave_direction=None
)
rgb_off = controller.build_control_string(
	effect='static',
	colors=['000000','000000','000000','000000'],
	speed=1,
	brightness=1,
	wave_direction=None
)

f = open( "/dev/input/event4", "rb" ); # Open the file in the read-binary mode
expireTimeTouchpad = 0
expireTimeRgb = 0

def reenableTouchpad():
    run = True
    while run:
        time.sleep(expireTimeTouchpad - time.time())
        if time.time() >= expireTimeTouchpad:
            os.system('xinput set-prop 14 188 1')
            run = False
            
def turnOff():
    run = True
    while run:
        time.sleep(expireTimeRgb - time.time())
        if time.time() >= expireTimeRgb:
            controller.send_control_string(rgb_off)
            run = False
		
tt = threading.Thread(target=reenableTouchpad)
tr = threading.Thread(target=turnOff)

while 1:
    data = f.read(24)
    (seconds, useconds, type, code, value) = struct.unpack('llHHI', data)
    if type == 1 and value != 0:
        controller.send_control_string(rgb_on)
        expireTimeRgb = time.time() + REENABLE_DELAY_RGB
        if not tr.is_alive():
            tr = threading.Thread(target=turnOff)
            tr.start()
        if code not in MODIFIER_KEYS:
            os.system('xinput set-prop 14 188 0')
            expireTimeTouchpad = time.time() + REENABLE_DELAY_TOUCHPAD
            if not tt.is_alive():
                tt = threading.Thread(target=reenableTouchpad)
                tt.start()
