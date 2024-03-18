import pytest

from gregor_anvil_automation.short_reads.validate import apply_metadata_map_file


@pytest.fixture(name="metadata_map_file", scope="function")
def fixture_metadata_map_file():
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


@pytest.fixture(name="gcp_bucket", scope="function")
def fixture_gcp_bucket():
    return "test-gcp-bucket"


def test_apply_metadata_map_file_pass(metadata_map_file, tables, gcp_bucket):
    """Tests that the function apply_metadata_map_file passes properly"""
    experiment_dna_short_read = tables.get("experiment_dna_short_read")
    aligned_dna_short_read = tables.get("aligned_dna_short_read")

    assert experiment_dna_short_read["experiment_sample_id"] == ""
    assert aligned_dna_short_read["aligned_dna_short_read_file"] == ""
    assert aligned_dna_short_read["aligned_dna_short_read_index_file"] == ""
    assert aligned_dna_short_read["md5sum"] == ""

    apply_metadata_map_file(metadata_map_file, tables, gcp_bucket)

    assert experiment_dna_short_read["experiment_sample_id"] == "BH-#####"

    cram_file_name = "some_name.hgv.cram"
    aligned_dna_short_read_file_path = f"gs://{gcp_bucket}/{cram_file_name}"
    assert (
        aligned_dna_short_read["aligned_dna_short_read_file"]
        == aligned_dna_short_read_file_path
    )

    crai_file_name = "some_name.hgv.cram.crai"
    aligned_dna_short_read_index_file_path = f"gs://{gcp_bucket}/{crai_file_name}"
    assert (
        aligned_dna_short_read["aligned_dna_short_read_index_file"]
        == aligned_dna_short_read_index_file_path
    )

    assert aligned_dna_short_read["md5sum"] == "FAKESUM-001"
