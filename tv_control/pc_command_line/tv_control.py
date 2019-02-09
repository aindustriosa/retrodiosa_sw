#!/usr/bin/python3
"""
Connects to the arduino in command of the TV (scketch named retrodiosa_IR_bypass). Use:

tv_control COMMAND

to view the available commands, use:

tv_control

with no arguments.
"""

import serial
import time
import sys
import collections


command_mappings = collections.OrderedDict()
command_mappings['on_off'] = b'q'
command_mappings['on'] = b'1'
command_mappings['off'] = b'2'
command_mappings['chan+'] = b'w'
command_mappings['chan-'] = b'e'
command_mappings['vol+'] = b'r'
command_mappings['vol-'] = b't'
command_mappings['mute'] = b'y',
command_mappings['menu_enter'] = b'u'
command_mappings['menu_exit'] = b'i'
command_mappings['menu_ok'] = b'o'
command_mappings['menu_arrow_up'] = b'p'
command_mappings['menu_arrow_down'] = b'a'
command_mappings['menu_arrow_right'] = b's'
command_mappings['menu_arrow_left'] = b'd'
command_mappings['source_tv'] = b'f'
command_mappings['source_pc'] = b'g'
command_mappings['source_video'] = b'h'
command_mappings['source_scart'] = b'j'
command_mappings['pip_source_left'] = b'k'
command_mappings['pip_source_right'] = b'l'

if len(sys.argv) == 2:
    if sys.argv[1] in command_mappings:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        ser.write(command_mappings[sys.argv[1]])
        ser.close()
        sys.exit()

print("Available commands:")
for i in command_mappings:
    print("   ", i)