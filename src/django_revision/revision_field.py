from django.db.models import CharField

from .revision import site_revision


class RevisionField(CharField):
    """Updates the revision number.

    Value is discovered from the current git branch and commit,
    the project metadata, the project pyproject.toml, the project
    VERSION file, or from settings.REVISION.

    See also the settings attributes that control discovery.
    """

    description = "RevisionField"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("editable", False)
        kwargs.setdefault("blank", True)
        kwargs.setdefault("default", "")
        kwargs.setdefault("max_length", 75)
        kwargs.setdefault("verbose_name", "Revision")
        super().__init__(*args, **kwargs)

    def pre_save(self, model, add):  # noqa: ARG002
        value = site_revision.revision
        setattr(model, self.attname, value)
        return value

    def get_internal_type(self):
        return "CharField"
