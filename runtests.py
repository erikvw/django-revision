#!/usr/bin/env python
import logging
import sys
from os.path import abspath, dirname

import django
from django.conf import settings
from django.test.runner import DiscoverRunner
from edc_test_utils import DefaultTestSettings

app_name = "django_revision"
base_dir = dirname(abspath(__file__))

DEFAULT_SETTINGS = DefaultTestSettings(
    APP_NAME=app_name,
    BASE_DIR=base_dir,
    ALLOWED_HOSTS=["localhost"],
    ROOT_URLCONF=f"{app_name}.tests.urls",
    STATIC_URL="/static/",
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.messages",
        "django.contrib.sessions",
        "django.contrib.sites",
        "django.contrib.staticfiles",
        "django_revision.apps.AppConfig",
    ],
).settings


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    tags = [t.split("=")[1] for t in sys.argv if t.startswith("--tag")]
    failures = DiscoverRunner(failfast=True, tags=tags).run_tests([f"{app_name}.tests"])
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()


# import logging
# import os
# import sys
#
# import django
# from django.conf import settings
# from django.test.runner import DiscoverRunner
#
# app_name = "django_revision"
#
#
# class DisableMigrations:
#     def __contains__(self, item):
#         return True
#
#     def __getitem__(self, item):
#         return None
#
#
# installed_apps = [
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.messages",
#     "django.contrib.sessions",
#     "django.contrib.sites",
#     "django.contrib.staticfiles",
#     "django_revision.apps.AppConfig",
# ]
#
# DEFAULT_SETTINGS = dict(
#     BASE_DIR=os.path.dirname(os.path.realpath(__file__)),
#     GIT_DIR=os.path.dirname(os.path.realpath(__file__)),
#     ALLOWED_HOSTS=["localhost"],
#     DEBUG=True,
#     ROOT_URLCONF=f"{app_name}.tests.urls",
#     STATIC_URL="/static/",
#     INSTALLED_APPS=installed_apps,
#     DATABASES={
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#         },
#     },
#     TEMPLATES=[
#         {
#             "BACKEND": "django.template.backends.django.DjangoTemplates",
#             "APP_DIRS": True,
#             "OPTIONS": {
#                 "context_processors": [
#                     "django.contrib.auth.context_processors.auth",
#                     "django.contrib.messages.context_processors.messages",
#                     "django.template.context_processors.request",
#                 ]
#             },
#         }
#     ],
#     MIDDLEWARE=[
#         "django.middleware.security.SecurityMiddleware",
#         "django.contrib.sessions.middleware.SessionMiddleware",
#         "django.middleware.common.CommonMiddleware",
#         "django.middleware.csrf.CsrfViewMiddleware",
#         "django.contrib.auth.middleware.AuthenticationMiddleware",
#         "django.contrib.messages.middleware.MessageMiddleware",
#         "django.middleware.clickjacking.XFrameOptionsMiddleware",
#     ],
#     LANGUAGE_CODE="en-us",
#     TIME_ZONE="UTC",
#     USE_I18N=True,
#     USE_L10N=True,
#     USE_TZ=True,
#     APP_NAME=f"{app_name}",
#     DEFAULT_FILE_STORAGE="inmemorystorage.InMemoryStorage",
#     MIGRATION_MODULES=DisableMigrations(),
#     PASSWORD_HASHERS=("django.contrib.auth.hashers.MD5PasswordHasher",),
# )
#
# if os.environ.get("TRAVIS"):
#     DEFAULT_SETTINGS.update(
#         DATABASES={
#             "default": {
#                 "ENGINE": "django.db.backends.mysql",
#                 "NAME": "edc",
#                 "USER": "travis",
#                 "PASSWORD": "",
#                 "HOST": "localhost",
#                 "PORT": "",
#             },
#         }
#     )
#
#
# def main():
#     if not settings.configured:
#         settings.configure(**DEFAULT_SETTINGS)
#     django.setup()
#     failures = DiscoverRunner(failfast=True).run_tests([f"{app_name}.tests"])
#     sys.exit(failures)
#
#
# if __name__ == "__main__":
#     logging.basicConfig()
#     main()
