from argparse import ArgumentParser


def get_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="A simple BitTorrent client that can download files using the BitTorrent protocol."
    )
    parser.add_argument(
        "decode",
        type=str,
        required=False,
        help="Path to the .torrent file to download.",
    )
    return parser