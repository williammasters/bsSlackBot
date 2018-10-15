import psutil
import sys
from subprocess import Popen

for process in psutil.process_iter():
    if process.cmdline() == ['python', 'bsBot.py']:
        sys.exit('Process found: exiting.')

print('Process not found: starting it.')
Popen(['python', '/home/ec2-user/bsSlackBot/bsBot.py'])