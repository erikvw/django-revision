#!/usr/bin/env python
import logging
import os
import sys
from os.path import abspath, dirname

import django
from django.conf import settings
from django.test.runner import DiscoverRunner
from edc_test_utils import DefaultTestSettings

app_name = "django_revision"
base_dir = dirname(abspath(__file__))
with open(os.path.join(base_dir, "VERSION")) as f:
    REVISION = f.read().strip()

DEFAULT_SETTINGS = DefaultTestSettings(
    APP_NAME=app_name,
    BASE_DIR=base_dir,
    ALLOWED_HOSTS=["localhost"],
    ROOT_URLCONF=f"{app_name}.tests.urls",
    STATIC_URL="/static/",
    REVISION=REVISION,
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
