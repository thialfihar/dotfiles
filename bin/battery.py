#!/usr/bin/env python3
import sys
import time

XMOBAR = "xmobar"
I3BAR = "i3bar"
I3BLOCKS = "i3blocks"

format = I3BLOCKS

if len(sys.argv) > 1:
    if sys.argv[1] == "i3blocks":
        format = I3BLOCKS
    elif sys.argv[1] == "i3bar":
        format = I3BAR
    elif sys.argv[1] == "xmobar":
        format = XMOBAR

RED = '#dc322f'
YELLOW = '#b58900'
GREEN = '#859900'

def get_value(filename):
    return open(filename, 'r').read().strip()

def calc_time(rate, left):
    if not rate:
        return (None, None)
    minutes = 60 * left // rate
    return (minutes // 60, minutes % 60)

def get_battery_status(format):
    max_capacity = int(get_value('/sys/class/power_supply/BAT0/charge_full'))
    remaining_capacity = int(get_value('/sys/class/power_supply/BAT0/charge_now'))
    present_rate = int(get_value('/sys/class/power_supply/BAT0/current_now'))
    charging_state = get_value('/sys/class/power_supply/BAT0/status').lower()
    ac_online = int(get_value('/sys/class/power_supply/AC/online'))

    percentage = 100.0 * remaining_capacity / max_capacity

    if percentage < 25:
        color = RED
    elif percentage < 80:
        color = YELLOW
    else:
        color = GREEN

    if format in (I3BLOCKS, I3BAR):
        output = "%.0f%%" % percentage
    else:
        output = '<fc=%s>%.0f</fc>%%' % (color, percentage)
    is_charging = False

    if charging_state == 'discharging':
        (eta_hours, eta_minutes) = calc_time(present_rate, remaining_capacity)
    elif charging_state == 'charging':
        (eta_hours, eta_minutes) = calc_time(present_rate, max_capacity - remaining_capacity)
        is_charging = True
    else:
        (eta_hours, eta_minutes) = (None, None)

    if eta_hours is not None:
        if is_charging:
            pass
        elif eta_hours == 0 and eta_minutes < 30:
            color = RED
        else:
            color = YELLOW

        if format in (I3BLOCKS, I3BAR):
            output += " [%02d:%02d]" % (eta_hours, eta_minutes)
        else:
            output += ' [<fc=%s>%02d:%02d</fc>]' % (color, eta_hours, eta_minutes)

    if ac_online:
        if format in (I3BLOCKS, I3BAR):
            output += " (ac)"
        else:
            output += ' (<fc=%s>ac</fc>)' % GREEN

    if format == I3BLOCKS:
        output = "%s\n%s\n%s" % (output, output, color)
    elif format == I3BAR:
        output = ',{"full_text":"%s", "color": "%s", "separator_block_width": 21}' % (output, color)

    return output


if __name__ == "__main__":
    if format == I3BLOCKS:
        print(get_battery_status(format))
    elif format == I3BAR:
        while True:
            print(get_battery_status(format))
            time.sleep(5.0)
    else:
        print(get_battery_status(format))
