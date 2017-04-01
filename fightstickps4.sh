#!/bin/bash

cd "${BASH_SOURCE%/*}" || exit  
python fightstickps4.py &disown
