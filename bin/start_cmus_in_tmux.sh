#!/bin/bash

pid=$(ps aux | awk '$11 == "cmus" {print $2}')
if [[ -z "$pid" ]]; then
    if [[ $(uname) == "Darwin" ]]; then
        killall tmux 2> /dev/null
    fi
    tmux new-session cmus
else
    if [[ $(uname) == "Linux" ]]; then
        session=$(</proc/$pid/environ grep -z '^TMUX=' | sed 's/.*,//')
        tmux attach -t $session
    else
        tmux attach
    fi
fi
