import argparse
import json
from typing import Dict, List

import requests

from gandi.auth import GandiAuth


def create_command(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparser = parser.add_parser("alias", help="manage email aliases")
    subparser.add_argument("-l", "--list", action="store_true")
    subparser.add_argument("-a", "--add", metavar="ALIAS", type=str)
    subparser.add_argument("-d", "--delete", metavar="ALIAS", type=str)
    subparser.set_defaults(func=alias)
    return subparser


def alias(config: Dict[str, str], auth: GandiAuth, args: argparse.Namespace):
    domain = config["domain"]
    mailbox_id = config["mailbox_id"]
    url = f"https://api.gandi.net/v5/email/mailboxes/{domain}/{mailbox_id}"
    if args.list:
        print("\n".join(get_aliases(url, auth)))
    elif args.add:
        if add_alias(url, auth, args.add):
            print(f"Created alias '{alias}'")
        else:
            print(f"Alias '{alias}' already exists")

    elif args.delete:
        if delete_alias(url, auth, args.delete):
            print(f"Removed alias '{alias}'")
        else:
            print(f"Alias '{alias}' does not exist")


def get_aliases(url: str, auth: GandiAuth):
    res = requests.get(url, auth=auth)
    res.raise_for_status()
    data = json.loads(res.text)
    return data["aliases"]


def add_alias(url: str, auth: GandiAuth, alias: str):
    aliases = get_aliases(url, auth)
    if alias in aliases:
        return False

    aliases.append(alias)
    update_aliases(url, auth, aliases)
    return True


def delete_alias(url: str, auth: GandiAuth, alias: str):
    aliases = get_aliases(url, auth)
    if alias not in aliases:
        return False

    aliases.remove(alias)
    update_aliases(url, auth, aliases)
    return True


def update_aliases(url: str, auth: GandiAuth, aliases: List[str]):
    requests.patch(url, json={"aliases": aliases}, auth=auth).raise_for_status()
