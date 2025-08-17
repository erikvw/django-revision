from django.db import models

from django_revision.model_mixins import RevisionModelMixin


class TestModel(RevisionModelMixin, models.Model):

    pass
