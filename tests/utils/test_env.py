import os
import pytest

from gregor_anvil_automation.utils.env import load_env_vars, find_and_load


@pytest.fixture(name="invalid_env_file")
def fixture_invalid_env_file(tmp_path, common_file_path):
    file_path = tmp_path / common_file_path / "test_files/invalid_env_file.env"
    return file_path


@pytest.fixture(name="valid_env_file")
def fixture_valid_env_file(tmp_path, common_file_path):
    file_path = tmp_path / common_file_path / "test_files/valid_env_file.env"
    return file_path


def test_find_and_load_invalid(invalid_env_file):
    with pytest.raises(OSError):
        find_and_load(invalid_env_file)


def test_find_and_load_valid(valid_env_file):
    find_and_load(valid_env_file)
    assert os.environ["ENVIRONMENT"] == "DEV"


def test_load_env_vars_invalid(invalid_env_file):
    with pytest.raises(OSError):
        load_env_vars(invalid_env_file)


def test_load_env_vars_valid(valid_env_file):
    load_env_vars(valid_env_file)
    assert os.environ["ENVIRONMENT"] == "DEV"
