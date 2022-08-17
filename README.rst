|pypi| |actions| |codecov| |downloads|

django-revision
---------------

Add a Django field class to your models to track the git revision with every model instance saved.

python 3.7, Django 3.0+. Uses `GitPython`.

For example:

.. code-block:: python

    from django.db import models

    from django_revision import RevisionField

    class TestModel(models.Model):

        revision = RevisionField()

.. code-block:: python

    >>> test_model = TestModel.objects.create()
    >>>test_model.revision
    '0.1dev0'

If the source is modified after the git tag was applied:

.. code-block:: python

    >>> test_model = TestModel.objects.create()
    >>>test_model.revision
    >>> '0.1dev0-35-ge9f632e:develop:e9f632e92143c53411290b576487f48c15156603'

Reference git information from anywhere in your app:

.. code-block:: python

    >>> from django_revision import site_revision
    >>> site_revision.tag
    '0.1dev0'
    >>>site_revision.revision
    '0.1dev0'


For research trial data, we need to track the source code revision at time of data collection. We deploy our source as a git branch and django-revision picks up the tag:branch:commit and updates
each saved model instance as data is collected.

Installation
------------

Add to settings:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django_revision.apps.AppConfig',
        ...
    ]

If your `git` working directory is something other than ``settings.BASE_DIR`` add ``GIT_DIR`` to ``settings`` with the path to your `git` working directory. For example:

.. code-block:: python

    GIT_DIR = BASE_DIR.ancestor(2)

If you have a deployment case where the source folder is not a `git` repo, you can set the revision manually in settings:

.. code-block:: python

    REVISION = '0.1.3'

Using in a View and Template
----------------------------

In the view's ``get_context_data`` set a context attribute to ``revision.tag`` or just use the ``RevisionMixin``:

.. code-block:: python

    from django_revision.views import RevisionMixin

    class MyView(RevisionMixin, TemplateView):
        ...

In your template:

.. code-block:: python

    {% block footer %}
	<footer class="footer">
	  <div class="container">
	    <div class="col-md-4"><p class="text-muted text-center"><small>{{ year }}&nbsp;{{ institution }}</small></p></div>
	    <div class="col-md-4"><p class="text-muted text-center"><small>Revision: {{ revision }}</small></p></div>
	    <div class="col-md-4"><p class="text-muted text-center"><small>For Research Purposes Only</small></p></div>
	  </div>
	</footer>
    {% endblock footer %}

.. |pypi| image:: https://img.shields.io/pypi/v/django-revision.svg
    :target: https://pypi.python.org/pypi/django-revision

.. |actions| image:: https://github.com/erikvw/django-revision/workflows/build/badge.svg?branch=develop
  :target: https://github.com/erikvw/django-revision/actions?query=workflow:build

.. |codecov| image:: https://codecov.io/gh/erikvw/django-revision/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/erikvw/django-revision

.. |downloads| image:: https://pepy.tech/badge/django-revision
   :target: https://pepy.tech/project/django-revision
