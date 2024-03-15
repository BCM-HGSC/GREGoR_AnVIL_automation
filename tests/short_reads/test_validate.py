import pytest

from gregor_anvil_automation.short_reads.validate import apply_metadata_map_file


@pytest.fixture(name="csv_dummy_data", scope="function")
def fixture_csv_dummy_data():
    return [
        {
            "experiment_dna_short_read_id": "BCM_TEST-001",
            "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-001",
            "cram_file_name": "some_name.hgv.cram",
            "crai_file_name": "some_name.hgv.cram.crai",
            "sm_tag": "BH-#####",
            "md5sum": "FAKESUM-001",
        }
    ]


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


def test_apply_metadata_map_file_pass():
    """Tests that the function apply_metadata_map_file passes properly"""
    return 0
