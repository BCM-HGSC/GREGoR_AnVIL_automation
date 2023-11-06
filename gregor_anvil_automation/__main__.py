"""
By naming the top-level module __main__, it is possible to run this module as
a script by running:
`python -m minimalhello [args...]`
"""

from argparse import ArgumentParser
from logging import basicConfig, getLogger, INFO
from pathlib import Path

from . import __version__


logger = getLogger(__name__)


def main():
    args = command_line_parser()
    basicConfig(level=INFO)
    logger.info(f"{args=}")


def command_line_parser():
    parser = ArgumentParser(
        description="gregor anvil automation",
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s {}".format(__version__)
    )
    parser.add_argument(
        "command",
        choices=["short_reads", "long_reads"],
        help="which type of submission to do",
    )
    parser.add_argument(
        "data_dir",
        type=Path,
        help="Path to directory containing the TSV table files.",
    )
    parser.add_argument(
        "--config_file",
        default="~/.config/gregor_anvil_automation.yaml",
        type=Path,
        help="Path to the config YAML file",
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
