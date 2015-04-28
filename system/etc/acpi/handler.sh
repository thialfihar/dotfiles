#!/bin/bash

case $1 in
  button/lid)
    case "$3" in
        close)
            logger 'LID closed'
            DISPLAY=:0.0 su thi -c '/usr/bin/i3lock -c 000000'
            pm-suspend
            ;;
        open)
            logger 'LID opened'
            ;;
        *)
            logger "ACPI action undefined: $3"
            ;;
    esac
    ;;
esac
