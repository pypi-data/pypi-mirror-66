"""
This module is for the main application logic
"""
from __future__ import print_function

import logging
import logging.config
import os
import signal
import subprocess
import sys
import tempfile
from time import sleep

import gevent
from gevent import monkey
from gevent.pywsgi import WSGIServer

from .config import get_conf
from .mpc import Controller, get_mpd_client
from .rpc import create_app

monkey.patch_all(subprocess=True)


def on_main_crash(*args, **kwargs):
    print('A crash occurred in "main" greenlet. Aborting...')
    sys.exit(1)




class Larigira(object):
    def __init__(self):

        self.log = logging.getLogger("larigira")
        self.conf = get_conf()
        self.controller = Controller(self.conf)
        self.controller.link_exception(on_main_crash)
        self.http_server = WSGIServer(
            ("", int(self.conf["HTTP_PORT"])), create_app(self.controller.q, self)
        )

    def start(self):
        self.controller.start()
        self.http_server.start()


def sd_notify(ready=False, status=None):
    args = ["systemd-notify"]
    if ready:
        args.append("--ready")
    if status is not None:
        args.append("--status")
        args.append(status)
    try:
        subprocess.check_call(args)
    except:
        pass


def main():
    tempfile.tempdir = os.environ["TMPDIR"] = os.path.join(
        os.getenv("TMPDIR", "/tmp"), "larigira.%d" % os.getuid()
    )
    if not os.path.isdir(os.environ["TMPDIR"]):
        os.makedirs(os.environ["TMPDIR"])

    if get_conf()["LOG_CONFIG"]:
        logging.config.fileConfig(
            get_conf()["LOG_CONFIG"], disable_existing_loggers=True
        )
    else:
        log_format = "%(asctime)s|%(levelname)s[%(name)s:%(lineno)d] %(message)s"
        logging.basicConfig(
            level=logging.DEBUG if get_conf()["DEBUG"] else logging.INFO,
            format=log_format,
            datefmt="%H:%M:%S",
        )
    logging.addLevelName(9, "DEBUGV")

    def debugv(self, message, *args, **kws):
        if self.isEnabledFor(9):
            self._log(9, message, args, **kws)

    logging.Logger.debugv = debugv

    if get_conf()["MPD_WAIT_START"]:

        while True:
            try:
                get_mpd_client(get_conf())
            except Exception as exc:
                print("exc", exc, file=sys.stderr)
                logging.debug(
                    "Could not connect to MPD at (%s,%s), waiting",
                    get_conf()["MPD_HOST"],
                    get_conf()["MPD_PORT"],
                )
                sd_notify(status="Waiting MPD connection")
                sleep(int(get_conf()["MPD_WAIT_START_RETRYSECS"]))
            else:
                logging.info("MPD ready!")
                sd_notify(ready=True, status="Ready")
                break

    larigira = Larigira()
    larigira.start()

    def sig(*args):
        print("invoked sig", args)
        larigira.controller.q.put(dict(kind="signal", args=args))

    for signum in (signal.SIGHUP, signal.SIGALRM):
        gevent.signal(signum, sig, signum)
    gevent.wait()


if __name__ == "__main__":
    main()
