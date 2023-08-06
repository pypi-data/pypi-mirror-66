import logging
import secrets
import hmac
from types import SimpleNamespace

from plogchain import formatters


VerbosityToLevel = {
	0: logging.ERROR,
	1: logging.WARNING,
	2: logging.INFO,
	3: logging.DEBUG,
}


class Result(SimpleNamespace):
	"""
	Class for reporting rich errors.
	Where a mere container would have been evaluated True,
	`Result` is evaluated like its `valid` argument.
	Extra information can be added as named arguments.
	"""
	def __init__(self, valid: bool, **kwargs):
		super().__init__(**kwargs)
		self.valid = valid

	def __bool__(self):
		return self.valid


class LogChainer:
	"""
	Entrypoint for initializing the log chain.
	"""

	def __init__(self, args = {}, **kwargs):
		"""
		@param args: dict
		"""

		defaultParams = {
			"stream": None,
			"formatterCls": formatters.Basic,
			"secret": secrets.token_urlsafe(128),
			"seed": secrets.token_urlsafe(),
			"format": "%(timestamp)s %(levelLetters)s %(fileLine)-15s %(funcName)-15s %(message)-60s |%(signature)s",
			"verbosity": 0,
			"timestampUtc": False,
			"timestampFmt": "iso", # or strftime
			"timestampPrecision": "milliseconds"
		}
		self.params = SimpleNamespace(**{**defaultParams, **args, **kwargs})
		self.formatter = self.params.formatterCls(self.params)


	def initLogging(self):
		aLevel = VerbosityToLevel.get(self.params.verbosity, logging.DEBUG)

		logging.basicConfig(level = aLevel, stream = self.params.stream)

		handler = logging.getLogger().handlers[0]
		handler.setFormatter(self.formatter)


	def verify(self, iLogChain):
		"""
		Check the consistency of a log chain with the secret.
		In case of failure, a tuple is returned with
		- check result: False
		- last consistent line
		- first inconsistent line
		"""
		extractFunc = getattr(self.params, "extractSignature", self.formatter.extractSignature)

		# TODO, verify the last line somehow
		for prevLine, line in zip(iLogChain, iLogChain[1:]):
			aStoredSign = extractFunc(line)
			aComputedSign = self.formatter.sign(prevLine, self.params.secret)

			isValid = hmac.compare_digest(aStoredSign, aComputedSign)

			if not isValid:
				#print("Inconsistency between lines:\nOK> %s\nKO> %s" % (prevLine, line))
				return Result(False, prevLine = prevLine, line = line)
		return Result(True)


def stopLogging():
	"""
	Cleanup if needed, inspired from the library source code.
	"""
	logger = logging.getLogger()
	for h in logger.handlers[:]:
		logger.removeHandler(h)
		h.close()
