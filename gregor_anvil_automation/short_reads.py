from pathlib import Path

from addict import Dict

from gregor_anvil_automation.utils.utils import get_table_samples


def run(config: Dict, excel_path: Path):
    """The short_reads entry point"""
    table_samples = get_table_samples(excel_path)
    return 0
