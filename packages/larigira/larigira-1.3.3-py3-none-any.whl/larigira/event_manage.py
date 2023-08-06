from __future__ import print_function
import sys
import argparse
import json

from .db import EventModel
from .config import get_conf


def main_list(args):
    m = EventModel(args.file)
    for alarm, action in m.get_all_alarms_expanded():
        json.dump(dict(alarm=alarm, action=action), sys.stdout, indent=4)
        sys.stdout.write('\n')


def main_getaction(args):
    m = EventModel(args.file)
    json.dump(m.get_action_by_id(int(args.actionid)), sys.stdout, indent=4)


def main_add(args):
    m = EventModel(args.file)
    m.add_event(
        dict(kind="frequency", interval=args.interval, start=1),
        [dict(kind="mpd", howmany=1)],
    )


def main():
    conf = get_conf()
    p = argparse.ArgumentParser()
    p.set_defaults(func=None)
    p.add_argument(
        "-f", "--file", help="Filepath for DB", required=False, default=conf["DB_URI"]
    )
    sub = p.add_subparsers()
    sub_list = sub.add_parser("list")
    sub_list.set_defaults(func=main_list)

    sub_getaction = sub.add_parser("getaction")
    sub_getaction.set_defaults(func=main_getaction)
    sub_getaction.add_argument('actionid')

    sub_add = sub.add_parser("add")
    sub_add.add_argument("--interval", type=int, default=3600)
    sub_add.set_defaults(func=main_add)

    args = p.parse_args()
    if args.func is None:
        p.print_help()
        sys.exit(2)
    args.func(args)


if __name__ == "__main__":
    main()
