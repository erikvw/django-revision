from django.conf import settings

if settings.APP_NAME == "django_revision":
    from .tests import models  # noqa
