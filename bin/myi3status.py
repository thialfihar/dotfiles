#!/usr/bin/env python3
import fcntl
import os
import select
import subprocess
import sys
import time

from battery import get_battery_status, I3BAR

if __name__ == "__main__":
    xtitle = subprocess.Popen(['/home/thi/bin/xtitle', '-s', '-f', '%s'], stdout=subprocess.PIPE)
    # make stdin a non-blocking file
    fd = xtitle.stdout.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    title = ''
    buffer = b''
    print('{"version":1}[[]')
    old_status = None
    while True:
        battery = get_battery_status(I3BAR)
        status = ',[{"full_text":"%s", "separator_block_width": 21}%s]' % (title.replace('"', '\\"'), battery)
        if status != old_status:
            print(status)
            sys.stdout.flush()
            old_status = status
        #time.sleep(1.0)

        readable, _, _ = select.select([xtitle.stdout], [], [xtitle.stdout], 5.0)
        if readable:
            buffer += xtitle.stdout.read()

            s = buffer.decode("utf-8")
            while '\n' in s:
                title, s = s.split('\n', 1)

            buffer = s.encode("utf-8")

