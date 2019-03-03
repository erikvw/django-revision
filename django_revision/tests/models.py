from django.db import models

from ..model_mixins import RevisionModelMixin


class TestModel(RevisionModelMixin, models.Model):

    pass
