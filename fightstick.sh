#!/bin/bash

cd "${BASH_SOURCE%/*}" || exit  
python fightstick.py &disown
