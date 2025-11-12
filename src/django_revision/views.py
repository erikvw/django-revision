from typing import Any

from .revision import Revision


class RevisionMixin:
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        revision = Revision()
        kwargs.update({"revision": revision.tag or revision.revision})
        return super().get_context_data(**kwargs)
