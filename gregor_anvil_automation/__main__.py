"""
By naming the top-level module __main__, it is possible to run this module as
a script by running:
`python -m minimalhello [args...]`
"""

from argparse import ArgumentParser, Namespace
from logging import basicConfig, getLogger, INFO
from pathlib import Path
from os import environ

import addict

from . import __version__
from .short_reads import validate
from .utils.utils import parse_yaml
from gregor_anvil_automation.utils.working_dir import get_working_dir

logger = getLogger(__name__)


def main() -> int:
    """Main method of gregor workflow"""
    args = command_line_parser()
    basicConfig(level=INFO)
    config = parse_yaml(args.config_file)
    # Working Dir
    parent = environ.get("TMPDIR", None)  # From user or cluster
    with get_working_dir(config.get("working_dir"), parent=parent) as working_dir:
        return run_command(config, args, working_dir)


def run_command(config: addict.Dict, args, working_dir) -> int:
    """Runs the command given by the user"""
    # TODO: This will be updated once we have validation/upload workflows established
    return_code = 0
    if args.command == "short_reads":
        return_code = validate.run(
            config,
            args.excel_path,
            (args.batch_id).strip(),
            (args.gcp_bucket).strip(),
            working_dir,
        )
    return return_code


def command_line_parser() -> Namespace:
    """Parses the arguments provided by the user"""
    parser = ArgumentParser(
        description="gregor anvil automation",
    )
    parser.add_argument(
        "--version", action="version", version=f"gregor_anvil_automation {__version__}"
    )
    parser.add_argument(
        "command",
        choices=["short_reads", "long_reads"],
        help="which type of submission to do",
    )
    parser.add_argument(
        "excel_path",
        type=Path,
        help="Path to excel provided by the PM",
    )
    parser.add_argument(
        "--config_file",
        default="~/.config/gregor_anvil_automation.yaml",
        type=Path,
        help="Path to the config YAML file",
    )
    parser.add_argument(
        "batch_id",
        help="batch_id is passed to help normalize data",
    )
    parser.add_argument(
        "gcp_bucket",
        help="gcp_bucket is passed to help normalize data",
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
