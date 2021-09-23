from django.apps import AppConfig as DjangoAppConfig

from .check_revision import check_revision


class AppConfig(DjangoAppConfig):
    name = "django_revision"

    def ready(self):
        check_revision()
