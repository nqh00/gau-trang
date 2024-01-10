"""
Log in to the jellyfin server and store credentials on disk.

This is meant to be called once interactively before using non-interactive
scripts, eg, those in the ``./examples`` directory.
"""

import getpass
from argparse import ArgumentParser

from . import JellyfinClient

parser = ArgumentParser(description=__doc__)
parser.add_argument("SERVER", help="https://jellyfin.example.lol")
parser.add_argument("--user", help="Your jellyfin username. Will be prompted if unset.")
parser.add_argument("--password", help="Your jellyfin password. Will be prompted if unset.")
args = parser.parse_args()

x = JellyfinClient(args.SERVER)

x.login(
    args.user or input("Username?"),
    args.password or getpass.getpass("Password?"),
)
