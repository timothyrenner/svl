from .svl import parse_svl

__all__ = ["parse_svl"]

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
