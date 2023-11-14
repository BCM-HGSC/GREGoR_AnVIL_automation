from pathlib import Path

from addict import Dict

from gregor_anvil_automation.utils.utils import get_table_samples


def run(config: Dict, excel_path: Path) -> int:
    """The short_reads entry point"""
    table_samples = get_table_samples(excel_path)
    # Validate files

    # If all ok, generate tsvs

    # If any errors, email issues

    # If all is good, email of success and files generated

    return 0
