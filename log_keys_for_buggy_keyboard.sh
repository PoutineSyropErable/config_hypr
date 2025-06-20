#!/bin/bash

# Make sure the log directory exists
mkdir -p "$HOME/.config/hypr/ignore/logs"

# Log file path
logfile="$HOME/.config/hypr/ignore/logs/$(date +'%Y-%m-%d')_keylogs.log"

# Launch wev inside Alacritty, logging both to screen and to the file
alacritty -e bash -c "wev --log-level debug | tee -a \"$logfile\""
