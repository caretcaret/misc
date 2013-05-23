#petbot
An interactive modular reddit bot. You can see its behavior at http://reddit.com/u/Petbot.

##What does this code do?
petbot is a framework for creating a reddit bot that can sustain conversation with posters. The behavior of the bot is defined by plugins to the framework.

##Why would I want to use it?
If you want to run a *responsive* reddit bot with *multiple* behaviors without worrying about the communication between reddit and your bot.

##What platform does it run on?
petbot is written in **Python 3**. Be sure to install `requests` and run `petbot.py` using Python 3 if you have both Python 2 and Python 3 installed.

##How do I install it?
Install the `requests` library by running

    pip install requests

Put any necessary plugin behavior that you want in the plugins folder.

##How do I run it?
Edit `config.ini` appropriately (comments included) and run

    python petbot.py

Consult `-h` or `--help` for options to override your config file.

##How do I run the tests?
No tests (yet).

##What license does it have?
petbot is released under Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0) and its text can be found at http://creativecommons.org/licenses/by-sa/3.0/.