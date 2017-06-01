#!/bin/bash
#This is the launcher script, make a launcher with this as the command

cd "${BASH_SOURCE%/*}" || exit  
python fightstick.py &disown
