#!/usr/bin/env python3

### PWBus - Main
#:
#:  maintainer: fabio.szostak@perfweb.com.br | Tue Nov 19 11:17:54 -03 2019

__author__ = 'fszostak@gmail.com'

import sys
import getopt
import traceback

from pwbus.commons.logging import log_exit
from pwbus.engines.engine_manager import EngineManager

# pwbus
#


def main(argv):
    channel = None
    engine = None
    command = None

    help_message = '\npwbus [-e <engine>] [-c <channel> start\n\n      -e <redis|socket>\n      --engine=<redis|socket>\n\n      -c <channel_id>\n      --channel=channel_id\n\n      start the server\n'

    try:
        opts, args = getopt.getopt(argv, "he:c:", ["start|channel=|engine="])
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(help_message)
            sys.exit()
        elif opt == 'start':
            command = arg
        elif opt in ("-e", "--engine"):
            engine = arg
        elif opt in ("-c", "--channel"):
            channel = arg

    for arg in args:
        if arg == "start":
            command = arg

    try:
        if command:
            engine_manager = EngineManager()
            engine_manager.action(command, engine, channel)
            sys.exit(0)

    except:
        sys.exit(1)

    print(help_message)


# __main__
#
if __name__ == "__main__":
    pwbus(sys.argv[1:])
