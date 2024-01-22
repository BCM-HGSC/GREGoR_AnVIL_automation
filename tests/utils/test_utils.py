"""So far only checks generate_file()"""
from dataclasses import asdict
import filecmp
import os

import pytest

from gregor_anvil_automation.utils.issue import Issue
from gregor_anvil_automation.utils.utils import generate_file
from gregor_anvil_automation.utils.env import load_env_vars, find_and_load


@pytest.fixture(name="valid_table")
def fixture_valid_table():
    return {
        "analyte": [
            {
                "participant_id": "test-participant_id-001",
                "analyte_id": "test-analyte_id-001",
            },
            {
                "participant_id": "test-participant_id-002",
                "analyte_id": "test-analyte_id-002",
            },
        ]
    }


@pytest.fixture(name="valid_issues")
def fixture_valid_issues():
    return [
        Issue(
            "participant_id",
            "Value participant_id already exists in the table participant in row 3",
            "participant",
            3,
        ),
        Issue(
            "analyte_id",
            "Value analyte_id already exists in the table analyte in row 3",
            "analyte",
            3,
        ),
        Issue(
            "family_id",
            "Value family_id already exists in the table family in row 3",
            "family",
            3,
        ),
    ]


@pytest.fixture(name="common_file_path")
def fixture_common_file_path():
    dir_name = os.path.dirname(__file__)
    return dir_name


@pytest.fixture(name="invalid_env_file")
def fixture_invalid_env_file(tmp_path, common_file_path):
    file_path = tmp_path / common_file_path / "test_files/invalid_env_file.env"
    return file_path


@pytest.fixture(name="valid_env_file")
def fixture_valid_env_file(tmp_path, common_file_path):
    file_path = tmp_path / common_file_path / "test_files/valid_env_file.env"
    return file_path


def test_generate_csv_valid_table_tsv(valid_table, common_file_path, tmp_path):
    """Test that check_utils successfully generates {table_name}_result.tsv"""
    analyte_result = tmp_path / common_file_path / "test_files/analyte_result.tsv"
    analyte_control = tmp_path / common_file_path / "test_files/analyte_control.tsv"
    data_headers = ["participant_id", "analyte_id"]
    generate_file(analyte_result, data_headers, valid_table["analyte"], "\t")

    assert filecmp.cmp(analyte_control, analyte_result, shallow=False)


def test_generate_csv_valid_issues_csv(valid_issues, common_file_path, tmp_path):
    """Test that check_utils successfully generates issues_result.csv"""
    issues_result = tmp_path / common_file_path / "test_files/issues_result.csv"
    issues_control = tmp_path / common_file_path / "test_files/issues_control.csv"
    data_headers = ["field", "message", "table_name", "row"]
    generate_file(
        issues_result, data_headers, [asdict(issue) for issue in valid_issues], ","
    )

    assert filecmp.cmp(issues_control, issues_result, shallow=False)


def test_find_and_load_invalid(invalid_env_file):
    try:
        find_and_load(invalid_env_file)
    except OSError:
        assert True  # REMOVE - find better way


def test_find_and_load_valid(valid_env_file, monkeypatch):
    monkeypatch.setenv("EMAIL_USERNAME", "hgsc@bcm.edu")
    monkeypatch.setenv("EMAIL_PASSWORD", "123donthackme")
    monkeypatch.setenv("EMAIL_HOST", "smtp.bcm.edu")
    monkeypatch.setenv("EMAIL_USERNAME", "25")
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", "test-utils")
    find_and_load(valid_env_file)
    assert True  # REMOVE - don't know how to test


def test_load_env_vars_invalid(invalid_env_file):
    try:
        load_env_vars(invalid_env_file)
    except OSError:
        assert True  # REMOVE - find better way


def test_load_env_vars_valid(valid_env_file, monkeypatch):
    monkeypatch.setenv("EMAIL_USERNAME", "hgsc@bcm.edu")
    monkeypatch.setenv("EMAIL_PASSWORD", "123donthackme")
    monkeypatch.setenv("EMAIL_HOST", "smtp.bcm.edu")
    monkeypatch.setenv("EMAIL_USERNAME", "25")
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", "test-utils")
    load_env_vars(valid_env_file)
    assert True  # REMOVE - don't know how to test
