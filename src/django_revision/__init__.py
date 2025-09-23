from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("django-revision")
except PackageNotFoundError:
    __version__ = "develop"

from .revision import Revision, site_revision
from .revision_field import RevisionField

__all__ = ["Revision", "RevisionField", "site_revision"]
