# django-revision

Add a Django field class to your models to track the git revision with every model instance saved. (Uses GitPython)

For example:

    from django.db import models
    
    from revision import RevisionField
    
    class TestModel(models.Model):

        revision = RevisionField()

Reference git information from anywhere in your app:

    >>> from revision import site_revision
    >>> site_revision.tag
    '1.0'
    >>>site_revision.revision
    'master:4c9c7f4f40e8db109d2b7b6d234defbe9d065d74'
    

Installation
------------

    pip install django-revision
    
If BASE_DIR does not exist in settings, add it:

    BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))

Description
-----------

For research trial data, we need to track the source code revision at time of data collection. 

We deploy our source as a git branch and django-revision picks up the tag or branch:commit and updates
each saved model instance as data is collected.
