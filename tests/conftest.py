from pathlib import Path

import addict
import pytest
import yaml


def pytest_addoption(parser):
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="run test that reach out to outside services out of our control",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--integration"):
        integration_config_file = Path("pytest_config.yaml").resolve()
        if not integration_config_file.is_file():
            print(
                f"{integration_config_file} file not found. Skipping integration test."
            )
            skip_integration = pytest.mark.skip(reason="No credentials found")
            for item in items:
                if "integration" in item.keywords:
                    item.add_marker(skip_integration)
    else:
        skip_integration = pytest.mark.skip(reason="Skipping integration tests")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)


@pytest.fixture(name="config")
def fixture_config(request):
    integration_config_file = Path("pytest_config.yaml").resolve()
    with open(integration_config_file) as fin:
        return addict.Dict(yaml.safe_load(fin.read()))
