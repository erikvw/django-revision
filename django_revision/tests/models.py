from django.db import models

from django_revision import RevisionField


class TestModel(models.Model):

    revision_field = RevisionField()
