import sys

from django.core.management.color import color_style

from .revision import Revision

style = color_style()


def check_revision(working_dir=None):
    revision = Revision(working_dir=working_dir)
    if revision.invalid:
        msg = 'Revision invalid: Got "' + revision.repo.tag + '"\n'
        sys.stdout.write(style.ERROR(msg))
    else:
        msg = "Revision: " + revision.revision + "\n"
        sys.stdout.write(msg)
    return msg
