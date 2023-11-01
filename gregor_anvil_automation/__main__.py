"""
By naming the top-level module __main__, it is possible to run this module as
a script by running:
`python -m minimalhello [args...]`
"""

from argparse import ArgumentParser
from pathlib import Path

from . import __version__


def main():
    args = command_line_parser()

def command_line_parser():
    parser = ArgumentParser(
        description="gregor anvil automation",
        prog="gregor_anvil_automation",
        epilog="See '<command> --help' to read about a specific sub-command.",
    )
    parser.add_argument(
        "tables_dir", type=Path, help="Path to directory containing the TSV table files."
    )
    parser.add_argument(
        "-c", "--config_file", default="~/.config/gregor_anvil_automation.yaml", 
        type=Path, help="Path to the config YAML file"
    )
    parser.add_argument(
        "-v","--version", action='version', version=__version__
    )
    subparsers = parser.add_subparsers(dest="act", help="Sub-commands")
    subparsers.add_parser(
        "short_reads",
        description="Takes in short read files",
        type=Path,
        help="Takes in a given short read file",
        parents=[parser],
    )
    subparsers.add_parser(
        "long_reads",
        description="Takes in long read files",
        type=Path,
        help="Takes in a given long read file",
        parents=[parser],
    )
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
