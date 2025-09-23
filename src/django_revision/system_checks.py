from django.core.checks import CheckMessage, Error
from django.core.management import color_style

from django_revision import Revision
from django_revision.exceptions import (
    RevisionError,
    RevisionGitDirDoesNotExist,
    RevisionGitError,
    RevisionPackageNotFoundError,
    RevisionTomlError,
)

style = color_style()

__all__ = ["check_for_revision"]


def check_for_revision(app_configs, **kwargs) -> list[CheckMessage]:  # noqa: ARG001
    errors = []

    try:
        str(Revision(verbose=True))
    except (
        RevisionError,
        RevisionGitError,
        RevisionGitDirDoesNotExist,
        RevisionPackageNotFoundError,
        RevisionTomlError,
    ):
        errors.append(
            Error(
                "Unable to determine the application revision. ",
                id="django_revision.E001",
            )
        )
    return errors
