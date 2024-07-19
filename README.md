# Fightstick Display  
[![Build Status](https://github.com/calexil/FightstickDisplay/actions/workflows/python-app.yml/badge.svg)](https://github.com/calexil/FightstickDisplay/actions/workflows/python-app.yml)  [![CodeFactor](https://www.codefactor.io/repository/github/calexil/fightstickdisplay/badge)](https://www.codefactor.io/repository/github/calexil/fightstickdisplay)  [![Maintainability](https://api.codeclimate.com/v1/badges/237a2b5bbbfd21b0c613/maintainability)](https://codeclimate.com/github/calexil/FightstickDisplay/maintainability)  [![GitHub issues](https://img.shields.io/github/issues/calexil/FightstickDisplay.svg)](https://github.com/calexil/FightstickDisplay/issues)  [![GitHub stars](https://img.shields.io/github/stars/calexil/FightstickDisplay.svg)](https://github.com/calexil/FightstickDisplay/stargazers)  [![GitHub forks](https://img.shields.io/github/forks/calexil/FightstickDisplay.svg)](https://github.com/calexil/FightstickDisplay/network) 

**A simple program written in python to display fightstick inputs.** 
# Screenshots
<img src="/theme/fightstick.gif" width="320" height="195"><img src="/theme/fightstickHB.gif" width="320" height="195">

# Installation
## Manual installation
Requirements:
* Python *3.7+*
* `python3-venv`

Clone the repository:
``` bash
git clone https://github.com/calexil/FightstickDisplay.git
```

# Usage 💾
* If you desire, make a launcher with fightstick.sh or fightstick_hb.sh as the startup script.
* Most fightsticks will be mapped correctly by default, but if yours is not
simply open the **theme/layout.ini** or **theme/layouthb.ini** file and tinker with it until its mapped correctly.
Usually only the rt/lt/rb/lb buttons get mixed up a little. If your fightstick is not detected
at all, **[let us know by clicking here!](https://github.com/calexil/FightstickDisplay/issues/new?title=My%20Gamepad%20was%20not%20detected!&body=My%20Gamepad%20Make:%0A%0AMy%20Gamepad%20Model:%0A)**
* For troubleshooting, launch the program with "-D", "-d" or "--debug" to print button values to the terminal for troubleshooting: `python3 src/fightstick.py --debug` or `python3 src/fightstick_hb.py --debug`
* You can also use your own images for all items, and if you like different color buttons, just be sure to edit the image names to match in the main program
* Enjoy

# Cleanup
To clean up dependencies (for instance, if you want to reinstall them), use the
provided script:

```bash
./cleanup.sh
```

## Debian packaging
To build a `.deb` Debian package, assuming you are on a Debian-based
distribution, use the following commands:

```bash
apt-get install build-essential debhelper devscripts equivs
mk-build-deps -i
dpkg-buildpackage -us -uc -b
```

Then you can install your package:

```bash
apt install ../fightstick-display_*.deb
```

# Current Version 📰
**Version 2.0** **[Watch it in action here](https://twitch.tv/calexil)**
# Contributors: :busts_in_silhouette:	
* [calexil](https://github.com/calexil)
* [benmoran56](https://github.com/benmoran56)

# Donate :heavy_dollar_sign:
This software is provided free of charge, but it certainly took time and effort to make, please consider
* [Making a donation](https://calexil.com/#donate) to support the project, and my other works.
