# Plogchain

[![Tests Status](https://github.com/gg-math/plogchain/workflows/unittests/badge.svg)](https://github.com/gg-math/plogchain/actions)
![Dependencies](https://img.shields.io/badge/dependencies-0-blue.svg)
[![license](https://img.shields.io/badge/license-ISC-blue.svg)](https://github.com/gg-math/plogchain/blob/master/LICENSE)

[![Web page](https://img.shields.io/badge/website-github.io/plogchain-blue.svg)](https://gg-math.github.io/plogchain)
[![Package](https://img.shields.io/badge/PIP-plogchain-blue.svg)](https://pypi.org/project/plogchain)

Python Logging based on blockchain 📜 ⛓️.

## Logs get chained
The current log line contains the signature of the previous line with your secret.
* detect lines deleted / lost
* detect logs tampering

## Philosophy
The package is intended to be a **lightweight** util for generating **incorruptible** logs.

For this pupose we rely as much as possible on standard packages: few dependencies, high quality.

The formatters are easy **extensible** by simply deriving from `Basic`.


# Usage

## Install
``` bash
pip install plogchain
```

## Choose your log type

Many types of logs are supported out-of-the-box:
- `Basic` raw text, relying on the standard formatter
- `Json` structured log lines with static & dynamic fields
- `CSV` work in progress

You can write a custom formatter in 20-ish lines.

## Init once in main
``` python
from plogchain import LogChainer

# Initialize a default chainer.
theLogger = LogChainer()

# Register the formatter to the logger.
theLogger.initLogging()
```

Have a look at [the comprehensive guide of constructor parameters](#constructor-parameters).

## Use everywhere with python logging module
``` python
import logging

logging.debug("My message")
logging.info("Some information")
```

## Check your logs integrity afterwards
``` python
from plogchain import LogChainer

aLogChain = [
	"2020-03-30 13:38:00.782|0ec90b9839fdd964|TestChaining.py:20 test_logging_happy_case hello gg",
	"2020-03-30 13:38:00.782|2e3f1b4a7b946fb1|TestChaining.py:21 test_logging_happy_case voila1",
	"2020-03-30 13:38:00.782|10d1ab606618492a|TestChaining.py:22 test_logging_happy_case voila2",
	"2020-03-30 13:38:00.782|805757e144f4e385|TestChaining.py:23 test_logging_happy_case voila5",
	"2020-03-30 13:38:00.782|3bda90b5af77d3fe|TestChaining.py:24 test_logging_happy_case voila4"
]
result = LogChainer.verify(aLogChain)

if not result:
	print("Last good line", result.prevLine)
	print("First bad line", result.line)
else:
	print("All right")
```

## Constructor parameters

They are passed as a dict and/or named arguments.
``` python
from plogchain import LogChainer

theLogger = LogChainer(verbosity = 3, secret = "mySignatureKey")

params = {"verbosity": 3, "secret": "mySignatureKey"}
theLogger = LogChainer(params, timestampFmt = "iso")
```

| Param | Default value | Description |
| ----- | ------------- | ----------- |
| formatterCls | formatters.Basic | Type of logging to perform, raw text, json, custom |
| format | see below | Placeholder string used by raw-text loggers |
| secret | secrets.token_urlsafe(128) | Signature key to compute the line signature |
| seed | secrets.token_urlsafe() | Random string to sign into the first log line |
| timestampFmt | "iso" | iso for 8601 or `strftime` compatible placeholders |
| timestampPrecision | "milliseconds" | `timespec` element used by [the datetime library](https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat) |
| timestampUtc | False | Transform the timestamp to its value in UTC |
| stream | cout | Where the logs are sent, file/console/custom stream |
| verbosity | 0 | Number [0..5] mapped to a logging.level |

The default format is `%(timestamp)s %(levelLetters)s %(fileLine)-15s %(funcName)-15s %(message)-60s |%(signature)s`. It relies on some extra fields like the signature at its end.


## Plogchain extra logging fields
We enrich the standard logging record with some handy fields:

| Name | Description |
| ---- | ----------- |
| fileLine | Widespread `filename:lineno` |
| levelLetters | 4 first letters of logging level names: short and unambiguous |
| signature | The digital signature of the previous line. Include it in all your lines to benefit from the chaining |
| timestamp | Improved version of `asctime`, see below |


The `timestamp` field offers more flexibility than `asctime` in regards to:
- the precision; can go up to the micro seconds (`msecs` cannot)
- the decimal separator; you choose, '.' by default
- utc or local timezone
- customize the format only in one place: `timestampFmt`

## Dynamic logging fields (WIP)
The package is suitable for server logging which context changes from one transaction to another.
Here is an example of setting contextual information throughout the lifecycle of a server:

``` python

	def startServer(containerName)
		# Static formatting at program startup...
		theLogger = LogChainer(formatterCls = formatters.Json)
		theLogger.initLogging()
		theLogger.setField(containerName = containerName)

	def handleTransaction(transactionId, userId):
		# More contextual data later on
		theLogger.setField(uId = userId, trxId = transactionId)

```

----

# Contributing

## Install
Simply clone and submit pull requests.

## Testing
The unit tests are located in the [test folder](https://github.com/gg-math/plogchain/tree/master/test)
which contains the `__main__.py` entrypoint.

``` bash
# Run all
python test

# Get additional options
python test --help
```

## Delivery
Use to the awesome [Poetry tool](https://python-poetry.org) for this purpose:

``` bash
poetry build
poetry publish
```
