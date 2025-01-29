"""
By naming the top-level module __main__, it is possible to run this module as
a script by running:
`python -m minimalhello [args...]`
"""

from argparse import ArgumentParser, Namespace
from logging import getLogger, INFO
from pathlib import Path
from os import environ
from datetime import datetime
import coloredlogs

import addict

from .utils.working_dir import get_working_dir
from .utils.env import load_env_vars
from . import __version__
from . import validate
from .utils.utils import parse_yaml


logger = getLogger(__name__)


def main() -> int:
    """Main method of gregor workflow"""
    args = command_line_parser()
    load_env_vars(args.env_file)
    config = parse_yaml(args.config_file)
    name = f"{config.log_dir}/gregor_automation_{datetime.now()}.log"
    coloredlogs.install(
        filename=name,
        format="%(asctime)s,%(msecs)d - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=INFO,
    )
    # Working Dir
    parent = environ.get("TMPDIR", None)  # From user or cluster
    with get_working_dir(config.get("working_dir"), parent=parent) as working_dir:
        logger.info("Running User Commands")
        result = run_command(config, args, working_dir)
    return result


def run_command(config: addict.Dict, args, working_dir: Path) -> int:
    """Runs the command given by the user"""
    logger.info("Running Short Read Validation")
    return validate.run(
        config,
        args.input_path,
        args.batch_number,
        working_dir,
    )


def command_line_parser() -> Namespace:
    """Parses the arguments provided by the user"""
    parser = ArgumentParser(
        description="gregor anvil automation",
    )
    parser.add_argument(
        "--version", action="version", version=f"gregor_anvil_automation {__version__}"
    )
    parser.add_argument(
        "input_path",
        type=Path,
        help="Path to excel provided by the PM or path to directory containing TSVs",
    )
    parser.add_argument(
        "--config_file",
        default="~/.config/gregor_anvil_automation.yaml",
        type=Path,
        help="Path to the config YAML file",
    )
    parser.add_argument(
        "batch_number",
        type=int,
        help="batch_number is passed to help normalize data",
    )
    parser.add_argument(
        "--env_file",
        default="~/.env",
        type=Path,
        help="Specifies the .env file to be used or assumes .env exist in current working directory",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
