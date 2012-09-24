#!/usr/bin/env python

import sys

RED = '#dc322f'
YELLOW = '#b58900'
GREEN = '#859900'

def get_value(filename):
    return file(filename).read().strip()

def calc_time(rate, left):
    if not rate:
        return (None, None)
    minutes = 60 * left // rate
    return (minutes // 60, minutes % 60)

max_capacity = int(get_value('/sys/class/power_supply/BAT0/energy_full'))
remaining_capacity = int(get_value('/sys/class/power_supply/BAT0/energy_now'))
present_rate = int(get_value('/sys/class/power_supply/BAT0/power_now'))
charging_state = get_value('/sys/class/power_supply/BAT0/status').lower()
ac_online = int(get_value('/sys/class/power_supply/ADP1/online'))

percentage = 100.0 * remaining_capacity / max_capacity

if percentage < 25:
    color = RED
elif percentage < 80:
    color = YELLOW
else:
    color = GREEN

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
    output += ' [<fc=%s>%02d:%02d</fc>]' % (color, eta_hours, eta_minutes)

if ac_online:
    output += ' (<fc=%s>ac</fc>)' % GREEN

print output
