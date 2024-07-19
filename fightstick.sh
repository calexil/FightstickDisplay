#!/usr/bin/env bash
##This is the launcher script, make a launcher with this as the command

venv=.venv

if test -n "$1"; then
	script=fightstick_hb
else
	script=fightstick
fi

cd "${BASH_SOURCE%/*}" || exit

if ! test -d "$venv"; then
	python3 -m venv "$venv"
fi

source "$venv"/bin/activate
pip install .
python3 src/"$script".py &
disown
