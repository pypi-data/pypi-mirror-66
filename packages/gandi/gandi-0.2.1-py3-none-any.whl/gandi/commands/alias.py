import argparse
import json
from typing import Dict, List, Optional

import requests

from gandi.auth import GandiAuth


def create_command(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparser = parser.add_parser("alias", help="manage email aliases")
    subparser.add_argument("-i", "--id", metavar="MAILBOX_ID", type=str)
    subparser.add_argument("-d", "--domain", type=str)

    actions = subparser.add_mutually_exclusive_group(required=True)
    actions.add_argument("-l", "--list", action="store_true")
    actions.add_argument("-a", "--add", metavar="ALIAS", type=str)
    actions.add_argument("-r", "--remove", metavar="ALIAS", type=str)

    subparser.set_defaults(func=alias)
    return subparser


def alias(config: Dict[str, str], auth: GandiAuth, args: argparse.Namespace) -> bool:
    domain = args.domain if args.domain is not None else config["domain"]
    mailbox_id = args.id if args.id is not None else config["mailbox_id"]
    url = f"https://api.gandi.net/v5/email/mailboxes/{domain}/{mailbox_id}"
    aliases = get_aliases(url, auth)
    if aliases is None:
        return False

    if args.list:
        print("\n".join(aliases))
    else:
        if args.add:
            if args.add in aliases:
                print(f"Alias '{args.add}' already exists")
                return False

            aliases.append(args.add)
        elif args.remove:
            if args.remove not in aliases:
                print(f"Alias '{args.remove}' does not exist")
                return False

            aliases.remove(args.remove)

        if not update_aliases(url, auth, aliases):
            return False

    return True


def get_aliases(url: str, auth: GandiAuth) -> Optional[List[str]]:
    res = requests.get(url, auth=auth)
    if res.status_code != 200:
        return None

    data = json.loads(res.text)
    return data["aliases"]


def update_aliases(url: str, auth: GandiAuth, aliases: List[str]) -> bool:
    res = requests.patch(url, json={"aliases": aliases}, auth=auth)
    return res.status_code == 200
