import psutil
import sys
from subprocess import Popen
import alerts

for process in psutil.process_iter():
    if process.cmdline() == ['python', 'bsBot.py']:
        sys.exit('Process found: exiting.')

print('Process not found: starting it.')
alerts.slackAlert()
Popen(['python', '/home/ec2-user/bsSlackBot/src/bsBot.py'])