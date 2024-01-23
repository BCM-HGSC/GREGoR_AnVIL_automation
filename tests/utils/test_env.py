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
    try:
        find_and_load(invalid_env_file)
    except OSError:
        assert True


def test_find_and_load_valid(valid_env_file, monkeypatch):
    monkeypatch.setenv("EMAIL_USERNAME", "hgsc@bcm.edu")
    monkeypatch.setenv("EMAIL_PASSWORD", "123donthackme")
    monkeypatch.setenv("EMAIL_HOST", "smtp.bcm.edu")
    monkeypatch.setenv("EMAIL_USERNAME", "25")
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", "test-utils")
    try:
        find_and_load(valid_env_file)
        assert True
    except OSError:
        assert False


def test_load_env_vars_invalid(invalid_env_file):
    try:
        load_env_vars(invalid_env_file)
    except OSError:
        assert True


def test_load_env_vars_valid(valid_env_file, monkeypatch):
    monkeypatch.setenv("EMAIL_USERNAME", "hgsc@bcm.edu")
    monkeypatch.setenv("EMAIL_PASSWORD", "123donthackme")
    monkeypatch.setenv("EMAIL_HOST", "smtp.bcm.edu")
    monkeypatch.setenv("EMAIL_USERNAME", "25")
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", "test-utils")
    try:
        load_env_vars(valid_env_file)
        assert True
    except OSError:
        assert False
