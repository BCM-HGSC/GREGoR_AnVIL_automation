import warnings


def ignore_deprecation_warning():
    """Ignores DeprecationWarning"""
    warnings.warn("deprecated", DeprecationWarning)


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    ignore_deprecation_warning()
