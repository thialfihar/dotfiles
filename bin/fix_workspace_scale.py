#!/usr/bin/env python3
import os
import sys

import i3

outputs = i3.get_outputs()
workspaces = i3.get_workspaces()

current = outputs[0]["current_workspace"]
if current.startswith("7"):
    os.system("~/bin/xrandr_scale.sh 0.5")
    i3.command("bar", "mode invisible")
else:
    os.system("~/bin/xrandr_scale.sh 1")
    i3.command("bar", "mode dock")
