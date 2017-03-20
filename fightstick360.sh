#!/bin/bash

cd "${BASH_SOURCE%/*}" || exit  
python fightstick360.py &disown
