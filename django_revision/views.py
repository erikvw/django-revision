from django.views.generic.base import ContextMixin
from django_revision.revision import Revision


class RevisionMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        revision = Revision()
        context.update({'revision': revision.tag or revision.commit})
        return context
