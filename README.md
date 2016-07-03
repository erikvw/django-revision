[![Build Status](https://travis-ci.org/erikvw/django-revision.svg?branch=master)](https://travis-ci.org/erikvw/django-revision)[![Coverage Status](https://coveralls.io/repos/erikvw/django-revision/badge.svg)](https://coveralls.io/r/erikvw/django-revision)

# django-revision

Add a Django field class to your models to track the git revision with every model instance saved. (Uses GitPython, does not work on pthon 3.2)

For example:

    from django.db import models
    
    from django_revision import RevisionField
    
    class TestModel(models.Model):

        revision = RevisionField()

Reference git information from anywhere in your app:

    >>> from django_revision import site_revision
    >>> site_revision.tag
    '1.0'
    >>>site_revision.revision
    'master:4c9c7f4f40e8db109d2b7b6d234defbe9d065d74'

For research trial data, we need to track the source code revision at time of data collection. We deploy our source as a git branch and django-revision picks up the tag:branch:commit and updates
each saved model instance as data is collected.

### Installation

Get the latest version:

    pip install git+https://github.com/erikvw/django-revision@develop#egg=django_revision

Add  GIT_DIR to settings to let `django-revision` know the location of your _git_ working directory, for example:

    GIT_DIR = BASE_DIR.ancestor(1)
    
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

