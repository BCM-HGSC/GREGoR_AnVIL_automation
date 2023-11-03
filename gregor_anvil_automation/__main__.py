"""
By naming the top-level module __main__, it is possible to run this module as
a script by running:
`python -m minimalhello [args...]`
"""

from argparse import ArgumentParser
from pathlib import Path

from . import __version__

def main():
    command_line_parser()
    # REMOVE
    # args = command_line_parser()
    # print(args)

def command_line_parser():
    parser = ArgumentParser(
        description="gregor anvil automation",
        prog="gregor_anvil_automation",
        epilog="See '<command> --help' to read about a specific sub-command.",
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s {}".format(__version__)
    )
    base_parser = ArgumentParser(add_help=False, prog='PROG')
    base_parser.add_argument(
        "tables_dir", type=Path, help="Path to directory containing the TSV table files."
    )
    base_parser.add_argument(
        "config_file", default="~/.config/gregor_anvil_automation.yaml", 
        type=Path, help="Path to the config YAML file"
    )
    subparsers = parser.add_subparsers(dest="cmd", help="Sub-commands")
    short_reads = subparsers.add_parser(
        "short_reads",
        description="Takes in short read files",
        help="Takes in a given short read file",
        parents=[base_parser],
    )
    short_reads.add_argument(
        "short_file",
        type=Path
    )
    long_reads = subparsers.add_parser(
        "long_reads",
        description="Takes in long read files",
        help="Takes in a given long read file",
        parents=[base_parser],
    )
    long_reads.add_argument(
        "long_file",
        type=Path
    )
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
