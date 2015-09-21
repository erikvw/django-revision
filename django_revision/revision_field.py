from django.db.models import CharField

from .revision import site_revision


class RevisionField(CharField):
    """Updates the value to the current git branch and commit."""

    description = "RevisionField"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        kwargs.setdefault('max_length', 75)
        kwargs.setdefault('verbose_name', 'Revision')
        super(RevisionField, self).__init__(*args, **kwargs)

    def pre_save(self, model, add):
        value = site_revision.revision
        setattr(model, self.attname, value)
        return value

    def get_internal_type(self):
        return "CharField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect the _actual_ field.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        # That's our definition!
        return (field_class, args, kwargs)
