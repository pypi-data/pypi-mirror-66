import argparse
import json
from typing import Dict, List, Optional

import requests

from gandi.auth import GandiAuth


def create_command(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparser = parser.add_parser("mbox", help="manage email mailboxes")
    subparser.add_argument("-d", "--domain", type=str)

    actions = subparser.add_mutually_exclusive_group(required=True)
    actions.add_argument("-l", "--list", action="store_true")

    subparser.set_defaults(func=mbox)
    return subparser


def mbox(config: Dict[str, str], auth: GandiAuth, args: argparse.Namespace) -> bool:
    try:
        domain = args.domain if args.domain is not None else config["domain"]
        url = f"https://api.gandi.net/v5/email/mailboxes/{domain}"
    except KeyError as e:
        print("Missing required config parameter: {}".format(*e.args))
        return False

    mboxes = get_mailboxes(url, auth)
    if mboxes is None:
        return False

    if args.list:
        fmt = "{:<30} {:<16} {:<8} {:>12}   {}"
        header = fmt.format("Address", "Domain", "Type", "Quota Used", "Mailbox ID")
        rows = [
            fmt.format(
                mbox["address"],
                mbox["domain"],
                mbox["mailbox_type"],
                mbox["quota_used"],
                mbox["id"],
            )
            for mbox in mboxes
        ]

        print(header)
        print("\n".join(rows))

    return True


def get_mailboxes(url: str, auth: GandiAuth) -> Optional[List[str]]:
    res = requests.get(url, auth=auth)
    if res.status_code != 200:
        return None

    data = json.loads(res.text)
    return data
