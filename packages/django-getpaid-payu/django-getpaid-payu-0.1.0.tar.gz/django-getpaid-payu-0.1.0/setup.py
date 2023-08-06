# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['getpaid_payu']

package_data = \
{'': ['*'], 'getpaid_payu': ['templates/getpaid_payu/*']}

install_requires = \
['django-getpaid>=2.0.0,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'swapper>=1.1.2,<2.0.0']

setup_kwargs = {
    'name': 'django-getpaid-payu',
    'version': '0.1.0',
    'description': 'Django-GetPaid plugin for PayU service.',
    'long_description': '===================\ndjango-getpaid-payu\n===================\n\nDjango-getpaid plugin for PayU service.\n\n.. note::\n\n    This is Alpha-quality software. You are more than welcome to `send PRs <https://github.com/django-getpaid/django-getpaid-payu>`_\n    with fixes and new features.\n\nInstallation\n============\n\nFirst make sure that `django-getpaid <https://django-getpaid.readthedocs.io/>`_ is installed and configured.\n\n.. code-block:: shell\n\n    pip install django-getpaid-payu\n\nThis should pull django-getpaid in case it\'s not installed yet.\n\n\nConfiguration\n=============\n\nAdd ``"getpaid_payu"`` to your ``INSTALLED_APPS`` and add plugin configuration.\n\n.. code-block:: python\n\n    # settings.py\n\n    INSTALLED_APPS = [\n        # ...\n        "getpaid",\n        "getpaid_payu",\n    ]\n\n    GETPAID_BACKEND_SETTINGS = {\n        "getpaid_payu": {\n            # take these from your merchant panel:\n            "pos_id": 12345,\n            "second_key": "91ae651578c5b5aa93f2d38a9be8ce11",\n            "client_id": 12345,\n            "client_secret": "12f071174cb7eb79d4aac5bc2f07563f",\n        },\n        # ...\n    }\n\n.. note::\n\n    If DEBUG setting is set to True, the plugin will use the sandbox API.\n\nThat should be enough to make your ``getpaid`` integration use new plugin\nand allow you to choose PayU for supported currencies.\n\nOther settings\n--------------\n\nYou can change additional settings for the plugin:\n\nconfirmation_method\n~~~~~~~~~~~~~~~~~~~\n\n* PUSH - paywall will send status updates to the callback endpoint hence updating status automatically\n* PULL - each Payment has to be verified by calling its ``fetch_and_update_status()``, eg. from a Celery task.\n\nDefault: PUSH\n\npaywall_method\n~~~~~~~~~~~~~~\n\n* REST - payment will be created using REST api call to paywall\n* POST - an extra screen will be displayed with a confirmation button that will\n  send all Payment params to paywall using POST. This is not recommended by PayU.\n\nLicence\n=======\n\nMIT\n\nAuthors\n=======\n\n`Dominik Kozaczko <https://github.com/dekoza/>`_\n',
    'author': 'Dominik Kozaczko',
    'author_email': 'dominik@kozaczko.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/django-getpaid/django-getpaid-paynow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
