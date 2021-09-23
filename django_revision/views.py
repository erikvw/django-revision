from django.views.generic.base import ContextMixin

from .revision import Revision


class RevisionMixin(ContextMixin):

    manual_revision = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        revision = Revision(manual_revision=self.manual_revision)
        context.update({"revision": revision.tag or revision.commit})
        return context
