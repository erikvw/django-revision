import sys

from django.apps import AppConfig as DjangoAppConfig
from django.core.management.color import color_style

from .revision import Revision

style = color_style()


class AppConfig(DjangoAppConfig):
    name = 'django_revision'

    def ready(self):
        revision = Revision()
        if revision.invalid:
            sys.stdout.write(style.ERROR(
                'Revision invalid: Got "' + revision.revision + '"\n'))
        else:
            sys.stdout.write('Revision: ' + revision.revision + '\n')
