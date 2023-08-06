import argparse
import configparser
import logging
import os
import sys
from pathlib import Path
from typing import Dict

from gandi import __version__, commands
from gandi.auth import GandiAuth


def run() -> None:
    """Command line entry point"""
    args = parse_args()
    setup_logging(args)
    config = read_config(args.config)

    auth = GandiAuth(config["api_key"])
    args.func(config, auth, args)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=Path, help="path to config file")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase output verbosity",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )

    subparsers = parser.add_subparsers(title="available commands")
    commands.alias.create_command(subparsers)

    return parser.parse_args()


def setup_logging(args: argparse.Namespace) -> None:
    """Setup logging"""
    level = logging.INFO if args.verbose else logging.WARNING
    logging.basicConfig(format="%(message)s", level=level)


def read_config(conf_file: Path = None) -> Dict[str, str]:
    """Find and read configuration file"""
    if not conf_file:
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME", "~/.config")
        conf_file = Path(xdg_config_home).expanduser() / "gandi" / "config"

    config = configparser.ConfigParser()
    try:
        with conf_file.open() as fil:
            config.read_file(fil)
    except FileNotFoundError:
        logging.error("Configuration file %s not found", conf_file)
        sys.exit(1)

    section = "gandi"
    keys = ("api_key", "domain", "mailbox_id")
    return {k: config.get(section, k) for k in keys}
