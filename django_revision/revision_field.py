from django.db.models import CharField

from .revision import site_revision


class RevisionField(CharField):
    """Updates the value to the current git branch and commit."""

    description = "RevisionField"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("editable", False)
        kwargs.setdefault("blank", True)
        kwargs.setdefault("null", True)
        kwargs.setdefault("max_length", 75)
        kwargs.setdefault("verbose_name", "Revision")
        super(RevisionField, self).__init__(*args, **kwargs)

    def pre_save(self, model, add):
        value = site_revision.revision
        setattr(model, self.attname, value)
        return value

    def get_internal_type(self):
        return "CharField"
