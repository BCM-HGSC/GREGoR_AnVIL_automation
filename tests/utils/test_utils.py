"""So far only checks generate_csv()"""
import filecmp

import pytest

from gregor_anvil_automation.utils.issue import Issue
from gregor_anvil_automation.utils.utils import generate_csv


@pytest.fixture(name="valid_tables")
def fixture_valid_tables():
    return {
        "participant": [
            {
                "participant_id": "test-participant_id-001",
                "family_id": "test-family_id-001",
            },
            {
                "participant_id": "test-participant_id-002",
                "family_id": "test-family_id-002",
            },
        ],
        "analyte": [
            {
                "participant_id": "test-participant_id-001",
                "analyte_id": "test-analyte_id-001",
            },
            {
                "participant_id": "test-participant_id-002",
                "analyte_id": "test-analyte_id-002",
            },
        ],
        "family": [
            {"family_id": "test-family_id-001"},
            {"family_id": "test-family_id-002"},
        ],
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
    # Hint `Path`
    # To see if your code is working move around the gregor directory and run `pytest`
    return "tests/utils/test_files"


def test_generate_csv_valid_table_tsv(valid_tables, common_file_path):
    """Test that check_utils successfully generates {table_name}_result.tsv"""
    """
    Get rid of for loop -- sometimes unavoidable but in here it is. Adds
    complexity to the test.

    Only have to test 1 thing so no family analyte participant etc. In reality,
    it doesnt even have to be participant. It can be some random tsv with random
    data unrelated to the Gregor stuff since all we care is if it generates
    a tsv file as expected.

    Pytest - look into tmp_path so you are not keeping the result tsvs
    """
    for key, value in valid_tables.items():
        file_path = f"{common_file_path}/{key}_result.tsv"
        data_headers = value[0].keys()
        generate_csv(file_path, data_headers, value, "\t")

    analyte_control = f"{common_file_path}/analyte_control.tsv"
    analyte_result = f"{common_file_path}/analyte_result.tsv"

    assert filecmp.cmp(analyte_control, analyte_result, shallow=False)


def test_generate_csv_valid_issues_csv(valid_issues, common_file_path):
    """Test that check_utils successfully generates issues_result.csv"""
    for issue in valid_issues:
        file_path = f"{common_file_path}/issues_result.csv"
        data_headers = ["field", "message", "table_name", "row"]
        generate_csv(file_path, data_headers, issue, ",")

    with open(f"{common_file_path}/issues_control.csv", "r") as i_control:
        issues_control = i_control.readlines()
    with open(f"{common_file_path}/issues_result.csv", "r") as i_result:
        issues_result = i_result.readlines()

    assert filecmp.cmp(issues_control, issues_result, shallow=False)
