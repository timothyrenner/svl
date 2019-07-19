from .compiler import svl

__all__ = ["svl"]

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
