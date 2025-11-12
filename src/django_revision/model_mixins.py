from django.db import models

from .revision_field import RevisionField


class RevisionModelMixin(models.Model):
    revision = RevisionField(
        help_text=(
            "System field. From git repository (tag:branch:commit), "
            "project metadata, project toml, project VERSION, or settings."
        )
    )

    class Meta:
        abstract = True
