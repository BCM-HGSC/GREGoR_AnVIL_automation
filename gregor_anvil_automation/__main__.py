"""
By naming the top-level module __main__, it is possible to run this module as
a script by running:
`python -m minimalhello [args...]`
"""

from sys import argv, path
from textwrap import dedent
from argparse import ArgumentParser
from pathlib import Path

from addict import Dict
from yaml import safe_load

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
        "tables_dir", type=Path, help="Path to the pm's directory"
    )
    # --config_file?
    parser.add_argument(
        "-c", "--config_file", default="~/.config/gregor_anvil_automation.yaml", 
        type=Path, help="Path to the config YAML file"
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
