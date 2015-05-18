# revision
Add a revision field class to your Django models to track your source code git revision at the time of data collection.

For example:

    from django.db import models
    
    from revision import RevisionField
    
    class TestModel(models.Model):

        revision = RevisionField()

Installation
------------

    pip install django-revision
    
If BASE_DIR does not exist in settings, add it:

    BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))

