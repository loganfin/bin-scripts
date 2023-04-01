#!/usr/bin/env python3

# Based on a script from
#   https://wiki.archlinux.org/title/Keyboard_backlight#D-Bus

# Depends on upower and dbus-python
#   pacman -S upower dbus-python

import dbus
import sys

def kb_light_set(delta):
    bus = dbus.SystemBus()
    kbd_backlight_proxy = bus.get_object('org.freedesktop.UPower', '/org/freedesktop/UPower/KbdBacklight')
    kbd_backlight = dbus.Interface(kbd_backlight_proxy, 'org.freedesktop.UPower.KbdBacklight')

    current = kbd_backlight.GetBrightness()
    maximum = kbd_backlight.GetMaxBrightness()
    new = max(0, min(current + delta, maximum))

    if 0 <= new <= maximum:
        current = new
        kbd_backlight.SetBrightness(current)

if __name__ == '__main__':
    if len(sys.argv) == 2 or len(sys.argv) == 3:
        if sys.argv[1] == "--up" or sys.argv[1] == "-u":
            if len(sys.argv) == 3:
                kb_light_set(int(sys.argv[2]))
            else:
                kb_light_set(1)
        elif sys.argv[1] == "--down" or sys.argv[1] == "-d":
            if len(sys.argv) == 3:
                kb_light_set(-int(sys.argv[2]))
            else:
                kb_light_set(-1)
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("Usage: kb-light.py [option]\n")
            print("  -h, --help for help")
            print("  -u, --down to decrease")
            print("  -d, --up to increase\n")
        else:
            print("Unknown argument:", sys.argv[1])
    else:
        print("Script takes one or two argument.", len(sys.argv) - 1, "arguments provided.")
