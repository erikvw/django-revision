from typing import Any

from .revision import Revision


class RevisionMixin:
    manual_revision = None

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        revision = Revision(manual_revision=self.manual_revision)
        kwargs.update({"revision": revision.tag or revision.commit})
        return super().get_context_data(**kwargs)
