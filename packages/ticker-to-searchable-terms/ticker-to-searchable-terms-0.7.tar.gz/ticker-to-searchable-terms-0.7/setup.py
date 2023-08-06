# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ticker_to_searchable_terms']

package_data = \
{'': ['*'], 'ticker_to_searchable_terms': ['DB/*']}

setup_kwargs = {
    'name': 'ticker-to-searchable-terms',
    'version': '0.7',
    'description': 'This is used to generate searchable terms for companies listed on NASDAQ NYSE. Includes',
    'long_description': 'This package is used to pull searchable terms from company ticker.\n\ncompany_obj = Company("AAPL")\ncompany_obj.terms\n\n\nprint(get_terms("AAPL")\n\n\n',
    'author': 'Henry Becket Trotter',
    'author_email': 'beckettrotter@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BecketTrotter/ticker_to_searchable_terms',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
