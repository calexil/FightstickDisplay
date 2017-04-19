#!/bin/bash
#This is the launcher script

cd "${BASH_SOURCE%/*}" || exit  
python fightstick.py &disown
