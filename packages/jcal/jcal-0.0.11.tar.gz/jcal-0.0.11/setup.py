# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jcal']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['jcal = jcal:main']}

setup_kwargs = {
    'name': 'jcal',
    'version': '0.0.11',
    'description': '`jcal` is a package for Japanese holiday.',
    'long_description': '`jcal` is a package for Japanese holiday.\n::\n\n   print(sorted(holiday(2019)))\n   >>>\n   [datetime.date(2019, 1, 1), datetime.date(2019, 1, 14), datetime.date(2019, 2, 11),\n    datetime.date(2019, 3, 21), datetime.date(2019, 4, 29), datetime.date(2019, 4, 30),\n    datetime.date(2019, 5, 1), datetime.date(2019, 5, 2), datetime.date(2019, 5, 3),\n    datetime.date(2019, 5, 4), datetime.date(2019, 5, 5), datetime.date(2019, 5, 6),\n    datetime.date(2019, 7, 15), datetime.date(2019, 8, 12), datetime.date(2019, 9, 16),\n    datetime.date(2019, 9, 23), datetime.date(2019, 10, 14), datetime.date(2019, 10, 22),\n    datetime.date(2019, 11, 4), datetime.date(2019, 11, 23)]\n\nRequirements\n------------\n* Python 3\n\nFeatures\n--------\n* nothing\n\nSetup\n-----\n::\n\n   $ pip install jcal\n\nHistory\n-------\n0.0.1 (2016-2-5)\n~~~~~~~~~~~~~~~~~~\n* first release\n',
    'author': 'Saito Tsutomu',
    'author_email': 'tsutomu7@hotmail.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
