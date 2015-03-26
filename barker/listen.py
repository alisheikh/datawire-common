"""
- Theoretically performs auth via the user db
- Connects to the output side of distribution (//host/inbox/user)
- Displays latest barks
"""

from argparse import ArgumentParser

from proton.reactor import Reactor
from datawire import Receiver, Processor

import common

class GetBarks(object):

    def __init__(self, user):
        self.receiver = Receiver("//localhost/inbox/%s" % user, Processor(self))

    def on_reactor_init(self, event):
        self.receiver.start(event.reactor)

    def on_message(self, event):
        print "Received", event.message.body


def main():
    parser = ArgumentParser(prog="listen")
    parser.add_argument("user")
    args = parser.parse_args()

    users = common.load_data("users.pickle")

    assert args.user in users
    Reactor(GetBarks(args.user)).run()


if __name__ == "__main__":
    main()