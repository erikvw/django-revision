import sys

from django.conf import settings
from django.core.management.color import color_style
from git import InvalidGitRepositoryError

from .revision import Revision

style = color_style()


def check_revision(working_dir: str) -> str:
    try:
        revision = Revision(
            working_dir=working_dir or getattr(settings, "GIT_DIR", settings.BASE_DIR)
        )
    except InvalidGitRepositoryError:
        msg = 'Revision invalid: Got InvalidGitRepositoryError"\n'
        sys.stdout.write(style.ERROR(msg))
    else:
        msg = "Revision: " + revision.revision + "\n"
        sys.stdout.write(msg)
    return msg
