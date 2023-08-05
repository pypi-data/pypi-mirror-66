# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crispy_forms_uikit',
 'crispy_forms_uikit.layout',
 'crispy_forms_uikit.templates.uikit-3.4.0.layout',
 'crispy_forms_uikit.templatetags']

package_data = \
{'': ['*'], 'crispy_forms_uikit': ['templates/uikit-3.4.0/*']}

install_requires = \
['Django>=2.1', 'django-crispy-forms>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'crispy-forms-uikit',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jan Willems',
    'author_email': 'jw@elevenbts.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
