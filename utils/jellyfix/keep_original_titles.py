"""
Set all movies and tv shows titles to the original, untranslated title.

Workaround for https://features.jellyfin.org/posts/32/keep-original-title-option
"""
import getpass
import itertools
from argparse import ArgumentParser

from jellyfix import JellyfinClient


def fix(client, item_id):
    """
    Update an item if its name and original title do not match.
    """
    detail = client.get_item(item_id)
    if detail.original_title and detail.name != detail.original_title:
        print(f"Renaming '{detail.name}' to '{detail.original_title}'")
        detail.name = detail.original_title
        client.update_item(detail)
    else:
        print(f"No need to rename '{detail.name}'")


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("SERVER", help="Example: http://127.0.0.1:8096")
    args = parser.parse_args()

    client = JellyfinClient(args.SERVER)
    if not client.logged:
        client.login(input("Username: "), getpass.getpass("Password: "))

    #For renaming series, chain client.get_series()
    for item in itertools.chain(client.get_movies()):
        fix(client, item.id)


if __name__ == "__main__":
    main()
