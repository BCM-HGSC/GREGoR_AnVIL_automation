import os
import pytest

from gregor_anvil_automation.utils.env import (
    find_dotenv,
    load_dotenv,
    load_env_vars,
    find_and_load,
    ENVFileDoesnotExist,
)

import pprint


@pytest.fixture(name="valid_env_file")
def fixture_valid_env_file():
    file_path = f"{os.path.dirname(__file__)}/test_files/valid_env_file.env"
    return file_path


def test_find_and_load_invalid(tmp_path):
    """Test that find_and_load successfully raises an error when given an invalid .env"""
    os.environ.pop("ENVIRONMENT", None)
    os.environ.pop("EMAIL_USERNAME", None)
    os.environ.pop("EMAIL_PASSWORD", None)
    os.environ.pop("EMAIL_HOST", None)
    os.environ.pop("EMAIL_PORT", None)
    os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
    with pytest.raises(OSError):
        find_and_load(tmp_path / "invalid_env_file.env")


def test_find_and_load_valid(valid_env_file):
    """Test that find_and_load successfully creates environment variables when given a valid .env"""
    os.environ.pop("ENVIRONMENT", None)
    os.environ.pop("EMAIL_USERNAME", None)
    os.environ.pop("EMAIL_PASSWORD", None)
    os.environ.pop("EMAIL_HOST", None)
    os.environ.pop("EMAIL_PORT", None)
    os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
    assert not os.environ.get("ENVIRONMENT")
    find_and_load(valid_env_file)
    assert os.environ["ENVIRONMENT"] == "DEV"


def test_load_env_vars_invalid(tmp_path):
    """Test that load_env_vars successfully raises an error when given an invalid .env"""
    os.environ.pop("ENVIRONMENT", None)
    os.environ.pop("EMAIL_USERNAME", None)
    os.environ.pop("EMAIL_PASSWORD", None)
    os.environ.pop("EMAIL_HOST", None)
    os.environ.pop("EMAIL_PORT", None)
    os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
    with pytest.raises(ENVFileDoesnotExist):
        load_env_vars(tmp_path / "invalid_env_file.env")


def test_load_env_vars_valid(valid_env_file):
    """Test that load_env_vars successfully creates environment variables when given a valid .env"""
    os.environ.pop("ENVIRONMENT", None)
    os.environ.pop("EMAIL_USERNAME", None)
    os.environ.pop("EMAIL_PASSWORD", None)
    os.environ.pop("EMAIL_HOST", None)
    os.environ.pop("EMAIL_PORT", None)
    os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
    assert not os.environ.get("ENVIRONMENT")
    load_env_vars(valid_env_file)
    pprint.pprint(os.environ["ENVIRONMENT"])
    assert os.environ["ENVIRONMENT"] == "DEV"
