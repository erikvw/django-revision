# -*- coding: utf-8 -*-
import os
from setuptools import setup
from setuptools import find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-revision',
    version='0.1.1',
    author=u'Erik van Widenfelt',
    author_email='ew2789@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='http://github/erikvw/django-revision',
    license='GPL licence, see LICENCE',
    description='Add a Django field class to your models to track the git revision with every model instance saved.',
    long_description=README,
    zip_safe=False,
    keywords='django fields git',
    install_requires=[
        'Django>=1.7',
        'GitPython>=1.0.0',
        'unipath>=1.1',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
