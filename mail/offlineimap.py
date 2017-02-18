#!/usr/bin/env python
import subprocess

def get_password(host, port, account):
    try:
        data = subprocess.check_output(r"gpg -q --no-tty --batch --passphrase $(security find-generic-password -a F574281F1FA6622D891AFEF33F90286D5CB674B6 -s GnuPG -w) -d ~/.authinfo.gpg", shell=True)
    except subprocess.CalledProcessError:
	data = ""

    for line in data.split("\n"):
        line = line.strip()
        words = line.split()
        if len(words) != 8:
            continue

        if words[1] == host and words[3] == account and words[5] == str(port):
            return words[7]

    return ""

