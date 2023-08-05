# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['cronparse']
setup_kwargs = {
    'name': 'cronparse',
    'version': '0.1.0',
    'description': 'A small tool for processing crontab syntax',
    'long_description': "# Cronparse\n\nA simple tool for testing [crontab](https://en.wikipedia.org/wiki/Cron) like syntax.\n\n## Usage\n\n    >>> from cronparse import Cron\n    >>> c = Cron('*/5 * * * 0')  # Matches only on Mondays, every 5th minute\n    >>> from datetime import datetime\n    >>> d = datetime(2020, 4, 13, 11, 5)\n    >>> c.matches(d)\n    True\n    >>> d = d.replace(minute=6)\n    >>> c.matches(d)\n    False\n    >>> d = d.replace(day=14, minute=5)\n    >>> c.matches(d)\n    False\n    >>> c.why(d) # Ask which fragment of the rule did not match\n    [True, True, True, True, False]\n\n## crontab rule syntax\n\n### Supported syntax:\n\n1. \\* - match any value\n2. 1 - match exact value\n3. \\*/5 - match every 5th value\n4. 1,3,4 - match values from list\n5. 1-3 - match values in a range\n6. 1-3,7,\\*/2 - combinations!\n7. @yearly, @annually, @monthly, @weekly, @daily, @midnight, @hourly\n\n### Unsupported syntax:\n\n- Day names\n- Month names\n- @reboot\n\n## Timezone Support\n\nOptionally, you can pass a `datetime.tzinfo` as the second argument. It\ndefaults to `datetime.timezone.utc`.\n\nAny `datetime` passed for testing will first be moved to that timezone.\n",
    'author': 'Curtis Maloney',
    'author_email': 'curtis@tinbrain.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
