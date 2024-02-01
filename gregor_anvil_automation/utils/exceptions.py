from dataclasses import dataclass
from pathlib import Path


@dataclass
class InputPathDoesNotExistError(Exception):
    """Raised when the given input_path does"""

    input_path: Path
