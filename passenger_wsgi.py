import sys, os
INTERP = "/home/jzhang94/local/bin/python"
#INTERP is present twice so that the new python interpreter knows the actual executable path
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

from paste.deploy import loadapp
application = loadapp('config:/home/jzhang94/didiget.in/production.ini')