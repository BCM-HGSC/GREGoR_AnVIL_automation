import pytest
import os

from gregor_anvil_automation.short_reads.validate import apply_metadata_map_file


@pytest.fixture(name="common_file_path", scope="function")
def fixture_common_file_path():
    dir_name = os.path.dirname(__file__)
    return dir_name


@pytest.fixture(name="one_sample_tables", scope="function")
def fixture_one_sample_tables():
    return {
        "experiment_dna_short_read": [
            {
                "experiment_dna_short_read_id": "BCM_TEST-001",
                "experiment_sample_id": "NA",
            },
        ],
        "aligned_dna_short_read": [
            {
                "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-001",
                "experiment_dna_short_read_id": "BCM_TEST-001",
                "aligned_dna_short_read_file": "NA",
                "aligned_dna_short_read_index_file": "NA",
                "md5sum": "NA",
            }
        ],
    }


@pytest.fixture(name="many_samples_tables", scope="function")
def fixture_many_samples_tables():
    return {
        "experiment_dna_short_read": [
            {
                "experiment_dna_short_read_id": "BCM_TEST-001",
                "experiment_sample_id": "NA",
            },
            {
                "experiment_dna_short_read_id": "BCM_TEST-002",
                "experiment_sample_id": "NA",
            },
            {
                "experiment_dna_short_read_id": "BCM_TEST-003",
                "experiment_sample_id": "NA",
            },
            {
                "experiment_dna_short_read_id": "BCM_TEST-004",
                "experiment_sample_id": "NA",
            },
            {
                "experiment_dna_short_read_id": "BCM_TEST-005",
                "experiment_sample_id": "NA",
            },
            {
                "experiment_dna_short_read_id": "BCM_TEST-006",
                "experiment_sample_id": "NA",
            },
            {
                "experiment_dna_short_read_id": "BCM_TEST-007",
                "experiment_sample_id": "NA",
            },
            {
                "experiment_dna_short_read_id": "BCM_TEST-008",
                "experiment_sample_id": "NA",
            },
            {
                "experiment_dna_short_read_id": "BCM_TEST-009",
                "experiment_sample_id": "NA",
            },
            {
                "experiment_dna_short_read_id": "BCM_TEST-010",
                "experiment_sample_id": "NA",
            },
        ],
        "aligned_dna_short_read": [
            {
                "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-001",
                "experiment_dna_short_read_id": "BCM_TEST-001",
                "aligned_dna_short_read_file": "NA",
                "aligned_dna_short_read_index_file": "NA",
                "md5sum": "NA",
            },
            {
                "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-002",
                "experiment_dna_short_read_id": "BCM_TEST-002",
                "aligned_dna_short_read_file": "NA",
                "aligned_dna_short_read_index_file": "NA",
                "md5sum": "NA",
            },
            {
                "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-003",
                "experiment_dna_short_read_id": "BCM_TEST-003",
                "aligned_dna_short_read_file": "NA",
                "aligned_dna_short_read_index_file": "NA",
                "md5sum": "NA",
            },
            {
                "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-004",
                "experiment_dna_short_read_id": "BCM_TEST-004",
                "aligned_dna_short_read_file": "NA",
                "aligned_dna_short_read_index_file": "NA",
                "md5sum": "NA",
            },
            {
                "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-005",
                "experiment_dna_short_read_id": "BCM_TEST-005",
                "aligned_dna_short_read_file": "NA",
                "aligned_dna_short_read_index_file": "NA",
                "md5sum": "NA",
            },
            {
                "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-006",
                "experiment_dna_short_read_id": "BCM_TEST-006",
                "aligned_dna_short_read_file": "NA",
                "aligned_dna_short_read_index_file": "NA",
                "md5sum": "NA",
            },
            {
                "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-007",
                "experiment_dna_short_read_id": "BCM_TEST-007",
                "aligned_dna_short_read_file": "NA",
                "aligned_dna_short_read_index_file": "NA",
                "md5sum": "NA",
            },
            {
                "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-008",
                "experiment_dna_short_read_id": "BCM_TEST-008",
                "aligned_dna_short_read_file": "NA",
                "aligned_dna_short_read_index_file": "NA",
                "md5sum": "NA",
            },
            {
                "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-009",
                "experiment_dna_short_read_id": "BCM_TEST-009",
                "aligned_dna_short_read_file": "NA",
                "aligned_dna_short_read_index_file": "NA",
                "md5sum": "NA",
            },
            {
                "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-010",
                "experiment_dna_short_read_id": "BCM_TEST-010",
                "aligned_dna_short_read_file": "NA",
                "aligned_dna_short_read_index_file": "NA",
                "md5sum": "NA",
            },
        ],
    }


@pytest.fixture(name="gcp_bucket", scope="function")
def fixture_gcp_bucket():
    return "test-gcp-bucket"


def test_apply_metadata_map_file_one_sample_pass(
    tmp_path, common_file_path, one_sample_tables, gcp_bucket
):
    """Tests that the function apply_metadata_map_file passes properly"""

    errors = []
    experiment_dna_short_read_sample = one_sample_tables["experiment_dna_short_read"][0]
    aligned_dna_short_read_sample = one_sample_tables["aligned_dna_short_read"][0]

    experiment_sample_id = experiment_dna_short_read_sample.get("experiment_sample_id")
    aligned_dna_short_read_file = aligned_dna_short_read_sample.get(
        "aligned_dna_short_read_file"
    )
    aligned_dna_short_read_index_file = aligned_dna_short_read_sample.get(
        "aligned_dna_short_read_index_file"
    )
    md5sum = aligned_dna_short_read_sample.get("md5sum")

    assert errors == []
    assert experiment_sample_id == "NA"
    assert aligned_dna_short_read_file == "NA"
    assert aligned_dna_short_read_index_file == "NA"
    assert md5sum == "NA"

    metadata_map_file = (
        tmp_path / common_file_path / "test_files/metadata_file_one_sample.csv"
    )
    apply_metadata_map_file(metadata_map_file, one_sample_tables, gcp_bucket, errors)

    assert errors == []
    # TODO: soft req - need to make results more dynamic if metadata file ever changes
    # Check experiment data
    experiment_dna_short_read_sample = one_sample_tables["experiment_dna_short_read"][0]
    assert experiment_dna_short_read_sample == {
        "experiment_dna_short_read_id": "BCM_TEST-001",
        "experiment_sample_id": "BH-####1",
    }
    # Check aligned data
    aligned_dna_short_read_sample = one_sample_tables["aligned_dna_short_read"][0]
    assert aligned_dna_short_read_sample == {
        "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-001",
        "experiment_dna_short_read_id": "BCM_TEST-001",
        "aligned_dna_short_read_file": f"gs://{gcp_bucket}/some_name_001.hgv.cram",
        "aligned_dna_short_read_index_file": f"gs://{gcp_bucket}/some_name_001.hgv.cram.crai",
        "md5sum": "FAKESUM-001",
    }


def test_apply_metadata_map_file_many_samples_pass(
    tmp_path, common_file_path, many_samples_tables, gcp_bucket
):
    errors = []
    experiment_dna_short_read_samples = many_samples_tables["experiment_dna_short_read"]
    aligned_dna_short_read_samples = many_samples_tables["aligned_dna_short_read"]

    assert errors == []
    for experiment_dna_short_read_sample in experiment_dna_short_read_samples:
        experiment_sample_id = experiment_dna_short_read_sample.get(
            "experiment_sample_id"
        )
        assert experiment_sample_id == "NA"
    for aligned_dna_short_read_sample in aligned_dna_short_read_samples:
        aligned_dna_short_read_file = aligned_dna_short_read_sample.get(
            "aligned_dna_short_read_file"
        )
        aligned_dna_short_read_index_file = aligned_dna_short_read_sample.get(
            "aligned_dna_short_read_index_file"
        )
        md5sum = aligned_dna_short_read_sample.get("md5sum")
        assert aligned_dna_short_read_file == "NA"
        assert aligned_dna_short_read_index_file == "NA"
        assert md5sum == "NA"

    metadata_map_file = (
        tmp_path / common_file_path / "test_files/metadata_file_many_samples.csv"
    )
    apply_metadata_map_file(metadata_map_file, many_samples_tables, gcp_bucket, errors)

    # TODO: soft req - need to make results more dynamic if metadata file ever changes
    # Check experiment data
    experiment_dna_short_read_samples = many_samples_tables["experiment_dna_short_read"]
    assert experiment_dna_short_read_samples == [
        {
            "experiment_dna_short_read_id": "BCM_TEST-001",
            "experiment_sample_id": "BH-####1",
        },
        {
            "experiment_dna_short_read_id": "BCM_TEST-002",
            "experiment_sample_id": "BH-####2",
        },
        {
            "experiment_dna_short_read_id": "BCM_TEST-003",
            "experiment_sample_id": "BH-####3",
        },
        {
            "experiment_dna_short_read_id": "BCM_TEST-004",
            "experiment_sample_id": "BH-####4",
        },
        {
            "experiment_dna_short_read_id": "BCM_TEST-005",
            "experiment_sample_id": "BH-####5",
        },
        {
            "experiment_dna_short_read_id": "BCM_TEST-006",
            "experiment_sample_id": "BH-####6",
        },
        {
            "experiment_dna_short_read_id": "BCM_TEST-007",
            "experiment_sample_id": "BH-####7",
        },
        {
            "experiment_dna_short_read_id": "BCM_TEST-008",
            "experiment_sample_id": "BH-####8",
        },
        {
            "experiment_dna_short_read_id": "BCM_TEST-009",
            "experiment_sample_id": "BH-####9",
        },
        {
            "experiment_dna_short_read_id": "BCM_TEST-010",
            "experiment_sample_id": "BH-###10",
        },
    ]
    # Check aligned data
    aligned_dna_short_read_samples = many_samples_tables["aligned_dna_short_read"]
    assert aligned_dna_short_read_samples == [
        {
            "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-001",
            "experiment_dna_short_read_id": "BCM_TEST-001",
            "aligned_dna_short_read_file": f"gs://{gcp_bucket}/some_name_001.hgv.cram",
            "aligned_dna_short_read_index_file": f"gs://{gcp_bucket}/some_name_001.hgv.cram.crai",
            "md5sum": "FAKESUM-001",
        },
        {
            "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-002",
            "experiment_dna_short_read_id": "BCM_TEST-002",
            "aligned_dna_short_read_file": f"gs://{gcp_bucket}/some_name_002.hgv.cram",
            "aligned_dna_short_read_index_file": f"gs://{gcp_bucket}/some_name_002.hgv.cram.crai",
            "md5sum": "FAKESUM-002",
        },
        {
            "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-003",
            "experiment_dna_short_read_id": "BCM_TEST-003",
            "aligned_dna_short_read_file": f"gs://{gcp_bucket}/some_name_003.hgv.cram",
            "aligned_dna_short_read_index_file": f"gs://{gcp_bucket}/some_name_003.hgv.cram.crai",
            "md5sum": "FAKESUM-003",
        },
        {
            "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-004",
            "experiment_dna_short_read_id": "BCM_TEST-004",
            "aligned_dna_short_read_file": f"gs://{gcp_bucket}/some_name_004.hgv.cram",
            "aligned_dna_short_read_index_file": f"gs://{gcp_bucket}/some_name_004.hgv.cram.crai",
            "md5sum": "FAKESUM-004",
        },
        {
            "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-005",
            "experiment_dna_short_read_id": "BCM_TEST-005",
            "aligned_dna_short_read_file": f"gs://{gcp_bucket}/some_name_005.hgv.cram",
            "aligned_dna_short_read_index_file": f"gs://{gcp_bucket}/some_name_005.hgv.cram.crai",
            "md5sum": "FAKESUM-005",
        },
        {
            "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-006",
            "experiment_dna_short_read_id": "BCM_TEST-006",
            "aligned_dna_short_read_file": f"gs://{gcp_bucket}/some_name_006.hgv.cram",
            "aligned_dna_short_read_index_file": f"gs://{gcp_bucket}/some_name_006.hgv.cram.crai",
            "md5sum": "FAKESUM-006",
        },
        {
            "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-007",
            "experiment_dna_short_read_id": "BCM_TEST-007",
            "aligned_dna_short_read_file": f"gs://{gcp_bucket}/some_name_007.hgv.cram",
            "aligned_dna_short_read_index_file": f"gs://{gcp_bucket}/some_name_007.hgv.cram.crai",
            "md5sum": "FAKESUM-007",
        },
        {
            "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-008",
            "experiment_dna_short_read_id": "BCM_TEST-008",
            "aligned_dna_short_read_file": f"gs://{gcp_bucket}/some_name_008.hgv.cram",
            "aligned_dna_short_read_index_file": f"gs://{gcp_bucket}/some_name_008.hgv.cram.crai",
            "md5sum": "FAKESUM-008",
        },
        {
            "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-009",
            "experiment_dna_short_read_id": "BCM_TEST-009",
            "aligned_dna_short_read_file": f"gs://{gcp_bucket}/some_name_009.hgv.cram",
            "aligned_dna_short_read_index_file": f"gs://{gcp_bucket}/some_name_009.hgv.cram.crai",
            "md5sum": "FAKESUM-009",
        },
        {
            "aligned_dna_short_read_id": "BCM_aligned_dna_short_read_id-010",
            "experiment_dna_short_read_id": "BCM_TEST-010",
            "aligned_dna_short_read_file": f"gs://{gcp_bucket}/some_name_010.hgv.cram",
            "aligned_dna_short_read_index_file": f"gs://{gcp_bucket}/some_name_010.hgv.cram.crai",
            "md5sum": "FAKESUM-010",
        },
    ]
