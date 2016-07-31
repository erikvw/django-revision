import sys

from django.apps import AppConfig as DjangoAppConfig

from .revision import Revision


class AppConfig(DjangoAppConfig):
    name = 'django_revision'

    def ready(self):
        revision = Revision()
        sys.stdout.write('Revision: ' + revision.revision + '\n')
