import pytest
import os

from gregor_anvil_automation.short_reads.validate import apply_metadata_map_file


@pytest.fixture(name="common_file_path", scope="function")
def fixture_common_file_path():
    dir_name = os.path.dirname(__file__)
    return dir_name


@pytest.fixture(name="tables", scope="function")
def fixture_tables():
    return {
        "experiment_dna_short_read": [
            {
                "experiment_dna_short_read_id": "BCM_TEST-001",
                "experiment_sample_id": "",
            },
        ],
        "aligned_dna_short_read": [
            {
                "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-001",
                "experiment_dna_short_read_id": "BCM_TEST-001",
                "aligned_dna_short_read_file": "",
                "aligned_dna_short_read_index_file": "",
                "md5sum": "",
            }
        ],
    }


@pytest.fixture(name="gcp_bucket", scope="function")
def fixture_gcp_bucket():
    return "test-gcp-bucket"


def test_apply_metadata_map_file_one_sample_pass(
    tmp_path, common_file_path, tables, gcp_bucket
):
    """Tests that the function apply_metadata_map_file passes properly"""

    # Adjust to better fit new and accurate validate.py
    experiment_dna_short_read = tables.get("experiment_dna_short_read")[0]
    aligned_dna_short_read = tables.get("aligned_dna_short_read")[0]

    experiment_sample_id = experiment_dna_short_read["experiment_sample_id"]
    aligned_dna_short_read_file = aligned_dna_short_read["aligned_dna_short_read_file"]
    aligned_dna_short_read_index_file = aligned_dna_short_read[
        "aligned_dna_short_read_index_file"
    ]
    md5sum = aligned_dna_short_read["md5sum"]

    assert not experiment_sample_id
    assert not aligned_dna_short_read_file
    assert not aligned_dna_short_read_index_file
    assert not md5sum

    metadata_map_file = (
        tmp_path / common_file_path / "test_files/metadata_file_one_sample.csv"
    )
    tables = apply_metadata_map_file(metadata_map_file, tables, gcp_bucket)

    assert experiment_sample_id == "BH-####1"

    cram_file_name = "some_name_001.hgv.cram"
    aligned_dna_short_read_file_path = f"gs://{gcp_bucket}/{cram_file_name}"
    assert aligned_dna_short_read_file == aligned_dna_short_read_file_path

    crai_file_name = "some_name_001.hgv.cram.crai"
    aligned_dna_short_read_index_file_path = f"gs://{gcp_bucket}/{crai_file_name}"
    assert aligned_dna_short_read_index_file == aligned_dna_short_read_index_file_path

    assert md5sum == "FAKESUM-001"
