"""
Loads a .env. The program tries to load the `.env.[username]` file first and if
that does not exist, then defaults to the `.env` file.
"""
import logging
import getpass
from pathlib import Path
from typing import Optional
import coloredlogs

from dotenv import load_dotenv, find_dotenv

logger = logging.getLogger(__name__)


def load_env_vars(custom_env_path: Optional[Path] = None) -> None:
    """Loads the .env file to ENV variables (without actually overriding them)"""
    env_path = custom_env_path or get_env_file_name()
    try:
        find_and_load(env_path)
    except IOError:
        logger.warning("%s file not found. Loading `.env`", env_path)
        try:
            find_and_load(".env")
        except IOError as e:
            logger.error("No default .env file found.")
            raise ENVFileDoesnotExist() from e


def get_env_file_name() -> str:
    """Returns the expected .env file name according to who is running this"""
    return f".env.{getpass.getuser()}"


def find_and_load(env_file_name: str) -> None:
    """Returns the path to a .env file when found"""
    user_env_path = find_dotenv(env_file_name, raise_error_if_not_found=True)
    load_dotenv(user_env_path)


#############
# Exception #
#############
class ENVFileDoesnotExist(Exception):
    """Raised when no .env files exist"""
