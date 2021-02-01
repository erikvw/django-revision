from django import template

from ..revision import site_revision

register = template.Library()


@register.simple_tag
def revision():
    """Returns the git site_revision."""
    return f"{site_revision.revision}"


@register.simple_tag
def revision_tag():
    """Returns the git site_revision."""
    return f"{site_revision.tag or site_revision.revision}"


@register.simple_tag
def revision_branch():
    """Returns the git site_revision."""
    return f"{site_revision.branch}"


@register.simple_tag
def revision_commit():
    """Returns the git site_revision."""
    return f"{site_revision.commit}"
