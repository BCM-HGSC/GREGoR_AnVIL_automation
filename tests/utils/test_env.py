import os
import pytest

from gregor_anvil_automation.utils.env import (
    load_env_vars,
    find_and_load,
    ENVFileDoesnotExist,
)


@pytest.fixture(name="valid_env_file")
def fixture_valid_env_file():
    file_path = f"{os.path.dirname(__file__)}/test_files/valid_env_file.env"
    return file_path


def test_find_and_load_invalid(tmp_path):
    """Test that find_and_load successfully raises an error when given an invalid .env"""
    with pytest.raises(OSError):
        find_and_load(tmp_path / "invalid_env_file.env")


def test_find_and_load_valid(valid_env_file):
    """Test that find_and_load successfully creates environment variables when given a valid .env"""
    os.environ.pop("MADE_UP_ENV_VAR", None)
    assert not os.environ.get("MADE_UP_ENV_VAR")
    find_and_load(valid_env_file)
    assert os.environ["MADE_UP_ENV_VAR"] == "DEV"


def test_load_env_vars_invalid(tmp_path):
    """Test that load_env_vars successfully raises an error when given an invalid .env"""
    with pytest.raises(ENVFileDoesnotExist):
        load_env_vars(tmp_path / "invalid_env_file.env")


def test_load_env_vars_valid(valid_env_file):
    """Test that load_env_vars successfully creates environment variables when given a valid .env"""
    os.environ.pop("MADE_UP_ENV_VAR", None)
    assert not os.environ.get("MADE_UP_ENV_VAR")
    load_env_vars(valid_env_file)
    assert os.environ["MADE_UP_ENV_VAR"] == "DEV"
