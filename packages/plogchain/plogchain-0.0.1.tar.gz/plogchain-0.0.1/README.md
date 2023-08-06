# Plogchain

[![Tests Status](https://github.com/gg-math/plogchain/workflows/pythonapp/badge.svg)](https://github.com/gg-math/plogchain/actions)
[![license](https://img.shields.io/badge/license-ISC-blue.svg)](https://github.com/gg-math/plogchain/blob/master/LICENSE)
[![Web page](https://img.shields.io/badge/website-github.io/plogchain-blue.svg)](https://gg-math.github.io/plogchain)


Python Logging based on blockchain

## Messages get chained
The current log line contains the signature of the previous line with your secret.
* detect lines deletion
* detect logs tampering

# Usage

## Init once in main
``` python
import ChainedLogger

# Obtained after the -vvv option of the program
verbosity = 3
theSecret = ChainedLogger.generateSecret()
ChainedLogger.init(verbosity, theSecret)

```

## Use everywhere with python logging module
``` python
import logging

logging.debug("My message")
logging.info("Some information")
```

## Check your logs integrity afterwards
``` python
import ChainedLogger

aLogChain = [
	"2020-03-30 13:38:00.782|0ec90b9839fdd964|TestChaining.py:20 test_logging_happy_case hello gg",
	"2020-03-30 13:38:00.782|2e3f1b4a7b946fb1|TestChaining.py:21 test_logging_happy_case voila1",
	"2020-03-30 13:38:00.782|10d1ab606618492a|TestChaining.py:22 test_logging_happy_case voila2",
	"2020-03-30 13:38:00.782|805757e144f4e385|TestChaining.py:23 test_logging_happy_case voila5",
	"2020-03-30 13:38:00.782|3bda90b5af77d3fe|TestChaining.py:24 test_logging_happy_case voila4"
]
isValid = ChainedLogger.verify(aLogChain, theSecret)
```

## Have a look at the [unit tests](https://github.com/gg-math/plogchain/tree/master/test)
