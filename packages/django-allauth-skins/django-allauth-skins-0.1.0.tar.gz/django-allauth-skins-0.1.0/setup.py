# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_allauth_skins']

package_data = \
{'': ['*'],
 'django_allauth_skins': ['static/allauth_skins/css/*',
                          'static/allauth_skins/images/*',
                          'static/allauth_skins/js/*',
                          'templates/allauth_skins/*']}

setup_kwargs = {
    'name': 'django-allauth-skins',
    'version': '0.1.0',
    'description': 'Styled templates for django-allauth',
    'long_description': '# AllAuth Skins\n\nStyled templates for django-allauth\n',
    'author': 'Adin Hodovic',
    'author_email': 'hodovicadin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
