from .revision import site_revision


class ModelAdminRevisionMixin:

    """Adds revision to the ModelAdmin context.

    Add to the change_form.html, for example:

        {% block after_field_sets %}
        {{ block.super }}
        <p class="help">Edc Revision {{ revision|default:'unknown?' }}</p>
        {% endblock %}
    """

    def add_view(self, request, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({"revision": site_revision.revision})
        return super().add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({"revision": site_revision.revision})
        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context
        )
