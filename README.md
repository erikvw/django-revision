[![Build Status](https://travis-ci.org/erikvw/django-revision.svg?branch=master)](https://travis-ci.org/erikvw/django-revision)
[![Coverage Status](https://coveralls.io/repos/erikvw/django-revision/badge.svg)](https://coveralls.io/r/erikvw/django-revision)
[![PyPI version](https://badge.fury.io/py/django_revision.svg)](http://badge.fury.io/py/django_revision)
# django-revision

Add a Django field class to your models to track the git revision with every model instance saved. (Uses GitPython)

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
    

Installation
------------

    pip install django-revision

If BASE_DIR does not exist in settings, add it:

    BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))

If BASE_DIR is not the _git_ working directory, add, for example:

    GIT_DIR = BASE_DIR.ancestor(1)
    
If you have a deployment case where the source folder is not a _git_ repo, you set the revision manually in settings:
	
	REVISION = '0.1.3'
	
If REVISION is specified in _settings_, _django-revision_ will use that value and not attempt to inspect the source folder -- _git_ repo or not. 

Description
-----------

For research trial data, we need to track the source code revision at time of data collection. 

We deploy our source as a git branch and django-revision picks up the tag:branch:commit and updates
each saved model instance as data is collected.
