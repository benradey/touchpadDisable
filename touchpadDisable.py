#!/usr/bin/python

import struct 
import os
import time
import threading
import l5p_kbl

MODIFIER_KEYS = {42, 29, 56, 100, 97, 54, 15, 125}
REENABLE_DELAY_TOUCHPAD = 0.5
REENABLE_DELAY_RGB = 5
COLOR_PERFORMANCE = '600000'
COLOR_QUIET = '000060'
COLOR_BALANCED = '606060'

controller = l5p_kbl.LedController()
rgb_on_performance = controller.build_control_string(
	effect='static',
	colors=[COLOR_PERFORMANCE,COLOR_PERFORMANCE,COLOR_PERFORMANCE,COLOR_PERFORMANCE],
	speed=1,
	brightness=1,
	wave_direction=None
)
rgb_on_quiet = controller.build_control_string(
	effect='static',
	colors=[COLOR_QUIET,COLOR_QUIET,COLOR_QUIET,COLOR_QUIET],
	speed=1,
	brightness=1,
	wave_direction=None
)
rgb_on_balanced = controller.build_control_string(
	effect='static',
	colors=[COLOR_BALANCED,COLOR_BALANCED,COLOR_BALANCED,COLOR_BALANCED],
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

controller.send_control_string(rgb_off)
f = open( "/dev/input/event4", "rb" ); # Open the file in the read-binary mode
expireTimeTouchpad = 0
expireTimeRgb = 0

def reenableTouchpad():
    run = True
    while run:
        time.sleep(expireTimeTouchpad - time.time())
        if time.time() >= expireTimeTouchpad:
            #os.system('xinput set-prop "SYNA2BA6:00 06CB:CE78 Touchpad" 345 1')
            os.system('xinput set-button-map "SYNA2BA6:00 06CB:CE78 Touchpad" 1 2 3 4 5 6 7')
            os.system('xinput set-prop "SYNA2BA6:00 06CB:CE78 Touchpad" 330 0')
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
        powermode = open("/sys/module/legion_laptop/drivers/platform:legion/PNP0C09:00/powermode", "r").read(1)
        if powermode == '1':
            controller.send_control_string(rgb_on_performance)
        elif powermode == '2':
            controller.send_control_string(rgb_on_quiet)
        else:
            controller.send_control_string(rgb_on_balanced)
        expireTimeRgb = time.time() + REENABLE_DELAY_RGB
        if not tr.is_alive():
            tr = threading.Thread(target=turnOff)
            tr.start()
        if code not in MODIFIER_KEYS:
            expireTimeTouchpad = time.time() + REENABLE_DELAY_TOUCHPAD
            if not tt.is_alive():
                #os.system('xinput set-prop "SYNA2BA6:00 06CB:CE78 Touchpad" 345 0')
                os.system('xinput set-button-map "SYNA2BA6:00 06CB:CE78 Touchpad" 0 0 0 4 5 6 7')
                os.system('xinput set-prop "SYNA2BA6:00 06CB:CE78 Touchpad" 330 -1')
                tt = threading.Thread(target=reenableTouchpad)
                tt.start()
