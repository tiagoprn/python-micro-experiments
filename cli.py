#!/usr/bin/env python3

# ANSI escape codes (for color support:
# http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html)
# https://www.reddit.com/r/bash/comments/fd1rwc/i_made_a_script_to_show_me_terminal

from os import getenv, path
from subprocess import run
from sys import stdout

# Colors
R='\033[1;31m'
B='\033[1;34m'
CYAN='\033[0;36m'
GREEN='\033[1;32m'
W='\033[1;37m'
YELLOW='\033[1;33m'
RESET='\033[0m'

OSTYPE=getenv('OSTYPE')
if not OSTYPE:
    OSTYPE='linux'

if OSTYPE.startswith('darwin'):
    DES = '/usr/local/share'
    SUDO = ''
elif OSTYPE.startswith('linux'):
    DES = '/usr/share'
    SUDO = 'sudo'
else:
    DES = '/usr/share'
    SUDO = 'sudo'

stdout.write(f"{YELLOW} [*] Executing... {RESET}\n")

if path.exists(f'{DES}'):
    command=f"{SUDO} ls {DES} && echo 'DONE'"
    run(command, shell=True)

stdout.write(f"{GREEN} [*] Finished. {RESET}\n")

