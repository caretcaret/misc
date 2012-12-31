#petbot
An interactive modular reddit bot. You can see its behavior at http://reddit.com/u/Petbot.

##What does this code do?
petbot is a framework for creating a reddit bot that can sustain conversation with posters. The behavior of the bot is defined by plugins to the framework.

##Why would I want to use it?
If you want to run a *responsive* reddit bot with *multiple* behaviors without worrying about the communication between reddit and your bot.

##What platform does it run on?
petbot is written in Python 3.

##How do I install it?
Install the `requests` library by running

    pip install requests

Put any necessary plugin behavior that you want in the plugins folder.

##How do I run it?
Edit `config.ini` and run `petbot.py`. (Command line options parser to come later.)

##How do I run the tests?
No tests (yet).

##What license does it have?
petbot is released under Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0) and its text can be found at http://creativecommons.org/licenses/by-sa/3.0/.