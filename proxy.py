import evdev, time
from evdev import InputDevice, categorize, ecodes

import sys
reload(sys)

modBuffer = [False, False, False, False, False, False, False, False]
modifiers = [29, 42, 56, 125, 97, 54, 100]
#LEFT  CONTROL          1    # 00000001     29
#LEFT  SHIFT            2    # 00000010     42
#LEFT  ALT              4    # 00000100     56
#LEFT  CMD|WIN          8    # 00001000     125
#RIGHT CONTROL          16   # 00010000     97
#RIGHT SHIFT            32   # 00100000     54
#RIGHT ALT              64   # 01000000     100
#RIGHT CMD|WIN          128  # 10000000

keyBuffer = [0,0,0,0,0,0]
key = {      #SCANCODE: USAGEID,
    30: 4,   #a,
    48: 5,   #b
    46: 6,   #c
    32: 7,   #d
    18: 8,   #e
    33: 9,   #f
    34: 10,  #g
    35: 11,  #h
    23: 12,  #i
    36: 13,  #j
    37: 14,  #k
    38: 15,  #l
    50: 16,  #m
    49: 17,  #n
    24: 18,  #o
    25: 19,  #p
    16: 20,  #q
    19: 21,  #r
    31: 22,  #s
    20: 23,  #t
    22: 24,  #u
    47: 25,  #v
    17: 26,  #w
    45: 27,  #x
    21: 28,  #y
    44: 29,  #z
    2: 30,   #1 !
    3: 31,   #2 @
    4: 32,   #3 #
    5: 33,   #4 $
    6: 34,   #5 %
    7: 35,   #6 ^
    8: 36,   #7 &
    9: 37,   #8 *
    10: 38,  #9 (
    11: 39,  #0 )
    28: 40,  # ENTER
    1: 41,   # ESC
    14: 42,  # BACKSPACE
    15: 43,  # TAB
    57: 44,  # SPACE
    12: 45,  # -
    13: 46,  # =
    26: 47,  # {
    27: 48,  # ]
    43: 49,  # \
    39: 51,  # :
    40: 52,  # "
    41: 53,  # `~
    51: 54,  # <
    52: 55,  # >
    53: 56,  # ?
    58: 57,  # CAPSLOCK
    59: 58,  # F1
    60: 59,  # F2
    61: 60,  # F3
    62: 61,  # F4
    63: 62,  # F5
    64: 63,  # F6
    65: 64,  # F7
    66: 65,  # F8
    67: 66,  # F9
    68: 67,  # F10
    69: 68,  # F11
    70: 69,  # F12
    115: 75, # PAGE UP
    111: 76, # DELETE
    114: 78, # PAGE DOWN
    106: 79, # RIGHT
    105: 80, # LEFT
    108: 81, # DOWN
    103: 82, # UP
}

def updateStatus(msg):

    msg = str(msg) + "\t\t"

    msg = msg + str(keyBuffer[0]) + "/"
    msg = msg + str(keyBuffer[1]) + "/"
    msg = msg + str(keyBuffer[2]) + "/"
    msg = msg + str(keyBuffer[3]) + "/"
    msg = msg + str(keyBuffer[4]) + "/"
    msg = msg + str(keyBuffer[5])

    sys.stdout.write("\r                                                                                ")
    sys.stdout.flush()

    sys.stdout.write("\r" + msg)
    sys.stdout.flush()


while True:
    dev =  None
    while dev is None:
            try:
               dev = InputDevice('/dev/input/event0')
            except:
                updateStatus("No keyboard")
                time.sleep (1)
    dev.grab()
    updateStatus("Keyboard Connected")

    try:
        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY:
                data = categorize(event)

                if data.keystate == 0: # Up events
                    if modifiers.count(data.scancode) > 0:
                        modBuffer[modifiers.index(data.scancode)] = False
                    elif keyBuffer.count(data.scancode) > 0:
                        keyBuffer[keyBuffer.index(data.scancode)] = 0
                if data.keystate == 1: # Down events
                    if modifiers.count(data.scancode) > 0:
                        modBuffer[modifiers.index(data.scancode)] = True
                    elif keyBuffer[0] == 0: keyBuffer[0] = data.scancode
                    elif keyBuffer[1] == 0: keyBuffer[1] = data.scancode
                    elif keyBuffer[2] == 0: keyBuffer[2] = data.scancode
                    elif keyBuffer[3] == 0: keyBuffer[3] = data.scancode
                    elif keyBuffer[4] == 0: keyBuffer[4] = data.scancode
                    elif keyBuffer[5] == 0: keyBuffer[5] = data.scancode

                modi = 0
                for i in range(len(modBuffer)):
                    if modBuffer[i] == True:
                        modi += (2**i)

                report = [modi,0]
                for i in range(len(keyBuffer)):
                    report.append(key.get(keyBuffer[i], 0))
                updateStatus(report)

                with open('/dev/hidg0', 'rb+') as fd:
                    fd.write(bytearray(report))

    except:
        keyBuffer = [0,0,0,0,0,0]
        modBuffer = [False, False, False, False, False, False, False, False]

        with open('/dev/hidg0', 'rb+') as fd:
            fd.write(("\0"*8).encode())
        updateStatus("Keyboard disconnected")
        time.sleep (1)
