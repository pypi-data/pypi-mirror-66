# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plogchain', 'plogchain.formatters']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.9,<0.10']

setup_kwargs = {
    'name': 'plogchain',
    'version': '0.0.2',
    'description': 'Python Logging based on blockchain',
    'long_description': '# Plogchain\n\n[![Tests Status](https://github.com/gg-math/plogchain/workflows/pythonapp/badge.svg)](https://github.com/gg-math/plogchain/actions)\n![Dependencies](https://img.shields.io/badge/dependencies-0-blue.svg)\n[![license](https://img.shields.io/badge/license-ISC-blue.svg)](https://github.com/gg-math/plogchain/blob/master/LICENSE)\n[![Web page](https://img.shields.io/badge/website-github.io/plogchain-blue.svg)](https://gg-math.github.io/plogchain)\n\n\nPython Logging based on blockchain.\n\n## Messages get chained\nThe current log line contains the signature of the previous line with your secret.\n* detect lines deletion\n* detect logs tampering\n\n## Philosophy\nThe package is intended to be a **lightweight** util for generating **incorruptible** logs.\n\nFor this pupose we rely as much as possible on standard packages.\n\n\n# Usage\n\n## Install\n``` bash\npip install plogchain\n```\n\n## Init once in main\n``` python\nimport ChainedLogger\n\n# Obtained after the -vvv option of the program\nverbosity = 3\ntheSecret = ChainedLogger.generateSecret()\nChainedLogger.init(verbosity, theSecret)\n```\n\n## Use everywhere with python logging module\n``` python\nimport logging\n\nlogging.debug("My message")\nlogging.info("Some information")\n```\n\n## Check your logs integrity afterwards\n``` python\nimport ChainedLogger\n\naLogChain = [\n\t"2020-03-30 13:38:00.782|0ec90b9839fdd964|TestChaining.py:20 test_logging_happy_case hello gg",\n\t"2020-03-30 13:38:00.782|2e3f1b4a7b946fb1|TestChaining.py:21 test_logging_happy_case voila1",\n\t"2020-03-30 13:38:00.782|10d1ab606618492a|TestChaining.py:22 test_logging_happy_case voila2",\n\t"2020-03-30 13:38:00.782|805757e144f4e385|TestChaining.py:23 test_logging_happy_case voila5",\n\t"2020-03-30 13:38:00.782|3bda90b5af77d3fe|TestChaining.py:24 test_logging_happy_case voila4"\n]\nisValid = ChainedLogger.verify(aLogChain, theSecret)\n```\n\n## Apply you own logging format (WIP)\nThe package is suitable for server logging which context changes from one transaction to another.\nHere is an example of setting contextual information throughout the lifecycle of a server:\n\n``` python\n# Static formatting at program startup...\nChainedLogger.setFormat(\n\t# Standard python logging fields\n\ttimestamp = "%(asctime)s.%(msecs)03d",\n\tfileLine  = "%(filename)s:%(lineno)d",\n\tmessage   = "%(message)s",\n\n\t# Custom fields\n\tprocessId = <current PID>\n)\n\n# ... then dynamic formatting with runtime context.\nChainedLogger.updateFormat(transactionId = <current transactionId>\n```\n\n# Contributing\n\n## Install\nSimply clone and submit pull requests.\n\n## Testing\nThe unit tests are located in the [test folder](https://github.com/gg-math/plogchain/tree/master/test)\nwhich contains the `__main__.py` entrypoint.\n\n``` bash\n# Run all\npython test\n\n# Get additional options\npython test --help\n```\n\n## Delivery\nUse to the awesome [Poetry tool](https://python-poetry.org) for this purpose:\n\n``` bash\npoetry publish\n```\n',
    'author': 'Gg Math',
    'author_email': 'code@gmath.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gg-math.github.io/plogchain',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.2,<4.0',
}


setup(**setup_kwargs)
