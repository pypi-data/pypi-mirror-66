# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plogchain', 'plogchain.ChainedLogger']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.9,<0.10']

setup_kwargs = {
    'name': 'plogchain',
    'version': '0.0.1',
    'description': 'Python Logging based on blockchain',
    'long_description': '# Plogchain\n\n[![Tests Status](https://github.com/gg-math/plogchain/workflows/pythonapp/badge.svg)](https://github.com/gg-math/plogchain/actions)\n[![license](https://img.shields.io/badge/license-ISC-blue.svg)](https://github.com/gg-math/plogchain/blob/master/LICENSE)\n[![Web page](https://img.shields.io/badge/website-github.io/plogchain-blue.svg)](https://gg-math.github.io/plogchain)\n\n\nPython Logging based on blockchain\n\n## Messages get chained\nThe current log line contains the signature of the previous line with your secret.\n* detect lines deletion\n* detect logs tampering\n\n# Usage\n\n## Init once in main\n``` python\nimport ChainedLogger\n\n# Obtained after the -vvv option of the program\nverbosity = 3\ntheSecret = ChainedLogger.generateSecret()\nChainedLogger.init(verbosity, theSecret)\n\n```\n\n## Use everywhere with python logging module\n``` python\nimport logging\n\nlogging.debug("My message")\nlogging.info("Some information")\n```\n\n## Check your logs integrity afterwards\n``` python\nimport ChainedLogger\n\naLogChain = [\n\t"2020-03-30 13:38:00.782|0ec90b9839fdd964|TestChaining.py:20 test_logging_happy_case hello gg",\n\t"2020-03-30 13:38:00.782|2e3f1b4a7b946fb1|TestChaining.py:21 test_logging_happy_case voila1",\n\t"2020-03-30 13:38:00.782|10d1ab606618492a|TestChaining.py:22 test_logging_happy_case voila2",\n\t"2020-03-30 13:38:00.782|805757e144f4e385|TestChaining.py:23 test_logging_happy_case voila5",\n\t"2020-03-30 13:38:00.782|3bda90b5af77d3fe|TestChaining.py:24 test_logging_happy_case voila4"\n]\nisValid = ChainedLogger.verify(aLogChain, theSecret)\n```\n\n## Have a look at the [unit tests](https://github.com/gg-math/plogchain/tree/master/test)\n',
    'author': 'Gg Math',
    'author_email': 'g@gmath.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gg-math.github.io/plogchain',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.2,<4.0',
}


setup(**setup_kwargs)
