[![Build Status](https://travis-ci.org/erikvw/django-revision.svg?branch=develop)](https://travis-ci.org/erikvw/django-revision)
[![Coverage Status](https://coveralls.io/repos/erikvw/django-revision/badge.svg)](https://coveralls.io/r/erikvw/django-revision)

# django-revision

Add a Django field class to your models to track the git revision with every model instance saved.

Uses `GitPython` (does not work on python version 3.2.)

For example:

    from django.db import models
    
    from django_revision import RevisionField
    
    class TestModel(models.Model):

        revision = RevisionField()

... then

    >>> test_model = TestModel.objects.create()
    >>>test_model.revision
    '0.1dev0'

If the source is modified after the git tag was applied:

    >>> test_model = TestModel.objects.create()
    >>>test_model.revision
    >>> '0.1dev0-35-ge9f632e:develop:e9f632e92143c53411290b576487f48c15156603'

Reference git information from anywhere in your app:

    >>> from django_revision import site_revision
    >>> site_revision.tag
    '0.1dev0'
    >>>site_revision.revision
    '0.1dev0'


For research trial data, we need to track the source code revision at time of data collection. We deploy our source as a git branch and django-revision picks up the tag:branch:commit and updates
each saved model instance as data is collected.

### Installation

Get the latest version:

    pip install git+https://github.com/erikvw/django-revision@develop#egg=django_revision

Add to settings:

    INSTALLED_APPS = [
        ...
        'django_revision.apps.AppConfig',
        ...
    ]

If your _git_ working directory is something other than `settings.BASE_DIR` add `GIT_DIR` to `settings` with the path to your _git_ working directory. For example:

    GIT_DIR = BASE_DIR.ancestor(2)
    
If you have a deployment case where the source folder is not a _git_ repo, you can set the revision manually in settings:
	
    REVISION = '0.1.3'

### Using in a View and Template
In the view's `get_context_data` set a context attribute to `revision.tag` or just use the `RevisionMixin`:

    from django_revision.views import RevisionMixin

    class MyView(RevisionMixin, TemplateView):
        ...

In your template:

    {% block footer %} 
	<footer class="footer">
	  <div class="container">
	    <div class="col-md-4"><p class="text-muted text-center"><small>{{ year }}&nbsp;{{ institution }}</small></p></div>
	    <div class="col-md-4"><p class="text-muted text-center"><small>Revision: {{ revision }}</small></p></div>
	    <div class="col-md-4"><p class="text-muted text-center"><small>For Research Purposes Only</small></p></div>
	  </div>
	</footer>
    {% endblock footer %}

