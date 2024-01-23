"""So far only checks generate_file()"""
from dataclasses import asdict
import filecmp
import os

import pytest

from gregor_anvil_automation.utils.issue import Issue
from gregor_anvil_automation.utils.utils import generate_file


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
