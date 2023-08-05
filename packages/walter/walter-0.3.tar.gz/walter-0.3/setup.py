# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['walter']

package_data = \
{'': ['*']}

install_requires = \
['appdirs', 'attrs', 'begins']

setup_kwargs = {
    'name': 'walter',
    'version': '0.3',
    'description': 'A better configuration library for Django and other Python projects',
    'long_description': 'Walter\n======\n\n.. warning::\n\n    Walter is pre-release software. Expect the API to change without notice, and expect this documentation to have lots of sharp edges.\n\nWalter is a configuration library, inspired by `python-decouple <https://pypi.python.org/pypi/python-decouple>`_, and intended to replace direct access to ``os.environ`` in Django ``settings.py`` files (although it is by no means Django-specific). It currently supports Python 3.5+.\n\nIt differs from other, similar libraries for two reasons:\n\n- It will let you specify your configuration parameters in one place and have auto-generated Sphinx documentation, just like with Python code. (Work on this hasn\'t been started yet.)\n- When your users try to start up your app with invalid configuration, the error message they get shows a list of **all of the errors** with every configuration parameter, not just the first one.\n\nInstallation\n------------\n\n::\n\n    pip install walter\n\nUsage\n-----\n\n::\n\n    from walter.config import Config\n\n    # Your configuration needs to be wrapped in a context manager,\n    # so Walter can collect all the errors and display them at the end.\n    with Config("SGC", "Dialer") as config:\n\n        # Read a configuration value with config.get()\n        SECRET_KEY = config.get(\'SECRET_KEY\')\n\n        # Convert the returned value to something other than a string with cast.\n        DEBUG = config.get(\'DEBUG\', cast=bool)\n\n        # You can pass any function that takes a string to `cast`.\n        # Here, we\'re using a third party function to parse a database URL\n        # string into a Django-compatible dictionary.\n        DATABASES = {\n            \'default\': config.get(\'DATABASE_URL\', cast=dj_database_url.parse),\n        }\n\n        # You can also make a parameter optional by giving it a default.\n        RAVEN_DSN = config.get(\'RAVEN_DSN\', default=None)\n\n        # Last but not least, help_text is displayed in your Sphinx docs.\n        SITE_NAME = config.get(\'SITE_NAME\',\n                               help_text="Displayed to users in the admin")',
    'author': 'Leigh Brenecki',
    'author_email': 'leigh@brenecki.id.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.6',
}


setup(**setup_kwargs)
