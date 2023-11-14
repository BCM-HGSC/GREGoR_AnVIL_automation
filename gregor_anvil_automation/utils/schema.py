"""Utility functions in regards to schema"""

from pathlib import Path

import addict

from .utils import parse_yaml


def get_schema(table_name: str) -> addict.Dict:
    """Returns the schema"""
    schema = get_schema_path(table_name)
    return parse_yaml(schema)


def get_schema_path(table_name: str) -> Path:
    """Returns the path of the schema associated with the given table name. If
    it does not exist, it will return a SchemaDoesNotExist error."""
    parent_dir = Path(__file__).resolve().parent.parent
    schema_path = parent_dir / "validation/schemas" / f"{table_name}.yaml"
    schema_path = schema_path.resolve()
    if not schema_path.exists():
        raise SchemaDoesNotExist(table_name)
    return schema_path


class SchemaDoesNotExist(Exception):
    """Raised if a schema that was called does not exists."""
