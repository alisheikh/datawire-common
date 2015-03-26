import os, signal
from subprocess import Popen
from time import sleep

import common

pids = []

def launch(command):
    pid = Popen(command.split()).pid
    print "[%5d] %s" % (pid, command)
    pids.append(pid)
    sleep(0.3)

commands = """
../directory
python distribution.py -u ark3
python distribution.py -u rhs
python distribution.py -u rdl
python distribution.py
python bizlogic.py
python submission.py
python autobark.py 1
python listen.py ark3
webui/proxy/proxy.js --thost localhost -p 5673 -t 6050
webui/proxy/proxy.js --thost localhost -p 5674 -t 5679
"""

def main():
    try:
        open("users.pickle")
    except IOError:
        common.make_users("users.pickle", 100)

    for command in commands.split("\n"):
        if command and not command.strip().startswith("#"):
            launch(command.strip())
    try:
        sleep(100000)
    finally:
        for pid in pids:
            os.kill(pid, signal.SIGTERM)


if __name__ == "__main__":
    main()
