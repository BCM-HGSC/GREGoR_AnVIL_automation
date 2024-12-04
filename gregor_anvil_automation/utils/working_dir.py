"""Code for working with local storage."""


from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory


@contextmanager
def get_working_dir(working_dir=None, suffix=None, prefix=None, parent=None):
    """A context manager that wraps working_dir if true and does nothing
    or creates a temporary directory and cleans up. The value is a resolved
    `Path`."""
    if working_dir:
        yield abs_path(working_dir)
    else:
        if parent:
            parent = str(abs_path(parent))
        temp = TemporaryDirectory(suffix, prefix, parent)
        try:
            yield Path(temp.name)
        finally:
            temp.cleanup()


def abs_path(path):
    """Convert to resolved pathlib.Path."""
    return Path(path).resolve()
