# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_selectel_storage']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'django-selectel-storage',
    'version': '1.0.1',
    'description': 'A Django storage backend allowing you to easily save user-generated and static files inside Selectel Cloud storage rather than a local filesystem, as Django does by default.',
    'long_description': "=======================\ndjango-selectel-storage\n=======================\n\n\n\n.. image:: https://badge.fury.io/py/django-selectel-storage.svg\n    :target: https://badge.fury.io/py/django-selectel-storage\n\n.. image:: https://img.shields.io/pypi/l/django-selectel-storage\n    :target: https://raw.githubusercontent.com/marazmiki/django-selectel-storage/master/LICENSE\n    :alt: The project license\n\n.. image:: https://travis-ci.org/marazmiki/django-selectel-storage.svg?branch=master\n    :target: https://travis-ci.org/marazmiki/django-selectel-storage\n    :alt: Travis CI build status\n\n.. image:: https://coveralls.io/repos/marazmiki/django-selectel-storage/badge.svg?branch=master\n    :target: https://coveralls.io/r/marazmiki/django-selectel-storage?branch=master\n    :alt: Code coverage percentage\n\n.. image:: https://pypip.in/wheel/django-selectel-storage/badge.svg\n     :target: https://pypi.python.org/pypi/django-selectel-storage/\n     :alt: Wheel Status\n\n.. image:: https://img.shields.io/pypi/pyversions/django-selectel-storage.svg\n     :target: https://img.shields.io/pypi/pyversions/django-selectel-storage.svg\n     :alt: Supported Python versions\n\n.. image:: https://img.shields.io/pypi/djversions/django-selectel-storage.svg\n     :target: https://pypi.org/project/django-selectel-storage/\n     :alt: Supported Django versions\n\n.. image:: https://readthedocs.org/projects/django-selectel-storage/badge/?version=latest\n     :target: https://django-ulogin.readthedocs.io/ru/latest/?badge=latest\n     :alt: Documentation Status\n\n.. image:: https://api.codacy.com/project/badge/Grade/f143275acdf249328a4968b62a94e100\n   :alt: Codacy Badge\n   :target: https://app.codacy.com/manual/marazmiki/django-selectel-storage?utm_source=github.com&utm_medium=referral&utm_content=marazmiki/django-selectel-storage&utm_campaign=Badge_Grade_Dashboard\n\n\nThis application allows you easily save media and static files into Selectel cloud storage.\n\n\nInstallation\n------------\n\n1. Install the package\n\n.. code:: bash\n\n    pip install django-selectel-storage\n\n\n2. Add to your settings module:\n\n.. code:: python\n\n    DEFAULT_FILE_STORAGE = 'django_selectel_storage.storage.SelectelStorage'\n    SELECTEL_STORAGES = {\n        'default': {\n            'USERNAME': 'xxxx_user1',\n            'PASSWORD': 'secret',\n            'CONTAINER_NAME': 'bucket',\n        },\n        'yet-another-schema': {\n            'USERNAME': 'yyyy_user2',\n            'PASSWORD': 'mystery',\n            'CONTAINER_NAME': 'box',\n\n        },\n    }\n\nPlease see details in the `documentation <https://django-selectel-storage.readthedocs.io/en/latest/>`_.\n",
    'author': 'Mikhail Porokhovnichenko',
    'author_email': 'marazmiki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marazmiki/django-selectel-storage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
