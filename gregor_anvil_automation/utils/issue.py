from dataclasses import dataclass
from typing import Optional


@dataclass
class Issue:
    """Represents an issue"""

    field: str
    message: str
    table_name: str
    row: Optional[int]
