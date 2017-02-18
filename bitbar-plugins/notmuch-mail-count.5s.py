#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3
# encoding: utf-8
# <bitbar.title>Notmuch unread counter</bitbar.title>
# <bitbar.desc>Show notmuch unread count</bitbar.desc>
# <bitbar.dependencies>notmuch</bitbar.dependencies>
import os
import re
import subprocess

home = os.path.expanduser("~")

unread_mails = subprocess.check_output("/usr/local/bin/notmuch search tag:unread".split())

mails = unread_mails.decode("utf-8").split("\n")
count = len(mails)
if count:
    print(":incoming_envelope: {count} unread | color=red".format(count=count))
else:
    print("")

print("---")

pattern = re.compile(r'^(?P<thread>\S*) +\S+ +\S+ +\S+ +(?P<people>.*?); +(?P<subject>.*?)( +\([^)]*\))?$')
for m in mails:
    if not m.strip():
        continue
    mo = pattern.match(m)
    if not mo:
        print("didn't match: " + m)
        exit(-1)

    thread = mo.group("thread")
    subject = mo.group("subject")[:64].replace('|', ':')
    people = " ".join(mo.group("people").split()[:2]).replace('|', ',').strip(",")

    print(("{subject} - {people} | color=green terminal=false " +
           "bash={home}/bin/open-mail-in-emacs-osx param1={thread}")
            .format(thread=thread, subject=subject, people=people, home=home))
