import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1 alpha'

long_description = read('README.txt')

setup(
    name = 'abstract.djangoprofiles',
    version = version,
    description = "Generci Django Profiles package",
    long_description = long_description,
    # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [],
    keywords = 'django profiles',
    author = 'Bruno Ripa',
    author_email = 'bruno.ripa@abstract.it',
    url = 'http://example.com/projects/my.project',
    license = 'BSD',
    packages = find_packages(),
    namespace_packages = ['abstract'],
    include_package_data = True,
    zip_safe = False,
    install_requires = [
          'distribute'
    ],
    test_requires = [
        'mock',
    ]
)
