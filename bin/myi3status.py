#!/usr/bin/env python3
import fcntl
import os
import re
import select
import subprocess
import sys

from datetime import datetime
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
        battery = get_battery_status(I3BAR).strip(',')
        status = [
            '{"full_text":"%s", "separator_block_width": 21}' % title.replace('"', '\\"'),
            battery,
            '{"full_text":"%s", "separator_block_width": 21}' % datetime.now().strftime('%H:%M:%S'),
        ]
        status = ',[' + ', '.join(status) + ']'
        if status != old_status:
            print(status)
            sys.stdout.flush()
            old_status = status
        #time.sleep(1.0)

        readable, _, _ = select.select([xtitle.stdout], [], [xtitle.stdout], 1.0)
        if readable:
            new = xtitle.stdout.read()
            new = re.sub(r'[\\]([^\\])', r'\\\\\1', new.decode('utf-8'))
            buffer += new.encode('utf-8')

            s = buffer.decode("utf-8")
            while '\n' in s:
                title, s = s.split('\n', 1)

            buffer = s.encode("utf-8")

