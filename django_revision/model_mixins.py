from django.db import models

from .revision_field import RevisionField


class RevisionModelMixin(models.Model):

    revision = RevisionField(help_text="System field. Git repository tag:branch:commit.")

    class Meta:
        abstract = True
