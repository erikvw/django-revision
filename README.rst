|pypi| |actions| |codecov| |downloads| |clinicedc|

django-revision
===============

Add a Django field class to your models to track a revision number with every model instance saved.

python 3.12+, Django 5.2+. Uses `GitPython`.

Use ``django-revision`` in Django projects where you need to track the source code revision on each model instance on add and change.

* If you deploy your live Django project from a cloned git branch, ``django-revision`` picks up the ``tag:branch:commit`` and updates each saved model instance as data is collected.
* If you are not running your Django project from a cloned repository, ``django-revision`` can discover the revision number from other sources as described below.

When used together with `django-simple-history`_, you can trace the revision number through the audit trail of a model instance.


Installation
------------

Add to settings:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'django_revision.apps.AppConfig',
        # ...
    ]

Add a revision field to your models
-----------------------------------

For example:

.. code-block:: python

    from django.db import models
    from simple_history.models import HistoricalRecords
    from django_revision import RevisionField

    class TestModel(models.Model):
        revision = RevisionField()
        history = HistoricalRecord()


or use the ``RevisionModelMixin``:


.. code-block:: python

    from django.db import models
    from simple_history.models import HistoricalRecords
    from django_revision.model_mixins import RevisionField

    class TestModel(RevisionModelMixin, models.Model):
        history = HistoricalRecord()


then create or save a model instance


.. code-block:: text

    >>> test_model = TestModel.objects.create()
    >>> test_model.revision
    '0.1dev0'


If the source is modified after the git tag was applied:

.. code-block:: text

    >>> test_model = TestModel.objects.create()
    >>> test_model.revision
    '0.1dev0-35-ge9f632e:develop:e9f632e92143c53411290b576487f48c15156603'


How django-revision discovers the revision number
-------------------------------------------------

``django-revision`` was originally developed to discover the git tag when a django project is run from a cloned git repository. By default, an exception will be raised if the working directory is not a git repository. However this behaviour can be bypassed by telling ``django-revision`` to ignore git discovery. ``django-revision`` will then try to discover a revision number from other sources. If all sources fail, an exception is raised.

The ``revision`` number is discovered in this order:

1. from the git tag if working directory is a git repository
2. from package metadata ``version()``
3. from ``[project][version]`` from ``pyproject.toml``, if it exists
4. from ``VERSION``, if it exists
5. from  ``settings.REVISION``

If the project using ``django-revision`` is not run from a git repo an exception will be raised by default. To bypass git discovery, update settings:

.. code-block:: python

    DJANGO_REVISION_IGNORE_WORKING_DIR = True


Discovery will now walk through the remaining options until one returns a value. To skip any one of the remaining options, update settings:


.. code-block:: python

    DJANGO_REVISION_IGNORE_METADATA = True

and / or

.. code-block:: python

    DJANGO_REVISION_IGNORE_TOML_FILE = True

and / or

.. code-block:: python

    DJANGO_REVISION_IGNORE_VERSION_FILE = True


You can hardcode a revision in settings as well (although this is not recommended):

.. code-block:: python

    REVISION = "1.0.0"

or

.. code-block:: python

    DJANGO_REVISION_REVISION = "1.0.0"


The ``settings.REVISION`` attribute is only used if the other options return ``None`` or you have told ``django-revision`` to ignore the other discovery options as shown above.

Relying on settings.REVISION
----------------------------
Hard coding ``settings.REVISION`` or ``settings. DJANGO_REVISION_REVISION`` is not recommended since you might forget to update the value and tag your data instances with the wrong revision number.


Using a git folder other than settings.BASE_DIR
-----------------------------------------------
By default, the git working directory is expected to be the same as settings.BASE_DIR. If not, add ``settings.GIT_DIR`` to ``settings`` with the path to your `git` working directory. For example:

.. code-block:: python

    GIT_DIR = Path(BASE_DIR).parent.parent

Using in a View and Template
----------------------------

In the view's ``get_context_data`` set a context attribute to ``revision.tag`` or just use the ``RevisionMixin``:

.. code-block:: python

    from django_revision.views import RevisionMixin

    class MyView(RevisionMixin, TemplateView):
        pass

In your template:

.. code-block:: text

    {% block footer %}
      <footer class="footer">
        <div class="container">
          <div class="col-md-4"><p class="text-muted text-center"><small>{{ year }}&nbsp;{{ institution }}</small></p></div>
          <div class="col-md-4"><p class="text-muted text-center"><small>Revision: {{ revision }}</small></p></div>
          <div class="col-md-4"><p class="text-muted text-center"><small>For Research Purposes Only</small></p></div>
        </div>
      </footer>
    {% endblock footer %}

Recommended for research trials
-------------------------------
For research trial data, you need to track the source code revision at time of data collection and modification. For example, if you deploy your live Django project from a cloned git branch, ``django-revision`` picks up the ``tag:branch:commit`` and updates each saved model instance as data is collected. If you running your Django project from a cloned repository, ``django-revision`` can discover the revision number from other sources as described above.

When used with `django-simple-history`_, you can trace the revision number through all modifications of a model instance.


.. |pypi| image:: https://img.shields.io/pypi/v/django-revision.svg
    :target: https://pypi.python.org/pypi/django-revision

.. |actions| image:: https://github.com/erikvw/django-revision/workflows/build/badge.svg?branch=develop
  :target: https://github.com/erikvw/django-revision/actions?query=workflow:build

.. |codecov| image:: https://codecov.io/gh/erikvw/django-revision/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/erikvw/django-revision

.. |downloads| image:: https://pepy.tech/badge/django-revision
   :target: https://pepy.tech/project/django-revision

.. |clinicedc| image:: https://img.shields.io/badge/framework-Clinic_EDC-green
   :alt:Made with clinicedc
   :target: https://github.com/clinicedc

.. _django-simple-history: https://github.com/django-commons/django-simple-history
