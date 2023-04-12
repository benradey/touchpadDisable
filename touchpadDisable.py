#!/usr/bin/python

import struct 
import os
import time
import threading

MODIFIER_KEYS = {42, 29, 56, 100, 97, 54}
REENABLE_DELAY = 0.3

f = open( "/dev/input/event4", "rb" ); # Open the file in the read-binary mode
expireTime = 0

def reenable():
    run = True
    while run:
#        print('---')
#        print('time.time(): ' + str(time.time()))
#        print('expireTime: ' + str(expireTime))
        time.sleep(expireTime - time.time())
#        print('Checking reenable')
        if time.time() >= expireTime:
#            print('Re-enabling!')
            os.system('xinput set-prop 14 188 1')
            run = False
		
t = threading.Thread(target=reenable)

while 1:
    data = f.read(24)
    (seconds, useconds, type, code, value) = struct.unpack('llHHI', data)
    if type == 1 and value != 0:
#        print((seconds, useconds, type, code, value))
#        print('---')
        if code not in MODIFIER_KEYS:
            os.system('xinput set-prop 14 188 0')
            expireTime = time.time() + REENABLE_DELAY
#            print('Setting expireTime: ' + str(expireTime))
            if not t.is_alive():
                t = threading.Thread(target=reenable)
                t.start()
#  print(str(time.time()) + ' new expiretime: ' + str(expireTime))
