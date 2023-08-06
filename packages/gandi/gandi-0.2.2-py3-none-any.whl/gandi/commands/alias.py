import argparse
import json
from typing import Dict, Optional, Set

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
        print("\n".join(sorted(aliases)))
        return True

    if args.add:
        return add_alias(url, auth, args.add, aliases)

    if args.remove:
        return remove_alias(url, auth, args.remove, aliases)

    # Unreachable
    raise AssertionError


def get_aliases(url: str, auth: GandiAuth) -> Optional[Set[str]]:
    res = requests.get(url, auth=auth)
    if res.status_code != 200:
        return None

    data = json.loads(res.text)
    return set(data["aliases"])


def add_alias(url: str, auth: GandiAuth, alias: str, aliases: Set[str]) -> bool:
    if alias in aliases:
        print(f"Alias '{alias}' already exists")
        return False

    if not update_aliases(url, auth, aliases | {alias}):
        return False

    print(f"Created alias '{alias}'")
    return True


def remove_alias(url: str, auth: GandiAuth, alias: str, aliases: Set[str]) -> bool:
    if alias not in aliases:
        print(f"Alias '{alias}' does not exist")
        return False

    if not update_aliases(url, auth, aliases - {alias}):
        return False

    print(f"Removed alias '{alias}'")
    return True


def update_aliases(url: str, auth: GandiAuth, aliases: Set[str]) -> bool:
    res = requests.patch(url, json={"aliases": list(aliases)}, auth=auth)
    try:
        res.raise_for_status()
    except requests.HTTPError as e:
        print("Error occurred while updating aliases")
        print(e.args)
        return False

    return True
