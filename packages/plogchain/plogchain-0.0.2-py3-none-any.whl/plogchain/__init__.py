import logging
import time

import secrets
import hashlib
import hmac

from types import SimpleNamespace

from plogchain import formatters

VerbosityToLevel = {
	0: logging.ERROR,
	1: logging.WARNING,
	2: logging.INFO,
	3: logging.DEBUG,
}


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
			"format": "%(timestamp)s %(levelLetters)s %(fileLine)-15s %(funcName)-15s %(message)-64s |%(signature)s",
			"extractSignature": lambda l: l[l.rindex('|') + 1:],
			"verbosity": 0,
			"utctime": False
		}
		self.params = SimpleNamespace(**{**defaultParams, **args, **kwargs})
		self.formatter = self.params.formatterCls(self.params)


	def initLogging(self):
		aLevel = VerbosityToLevel.get(self.params.verbosity, logging.DEBUG)

		logging.basicConfig(level = aLevel, stream = self.params.stream)

		handler = logging.getLogger().handlers[0]
		handler.setFormatter(self.formatter)
		if self.params.utctime:
			self.formatter.converter = time.gmtime


	def verify(self, iLogChain):
		"""
		Check the consistency of a log chain with the secret.
		In case of failure, a tuple is returned with
		- check result: False
		- last consistent line
		- first inconsistent line
		"""
		prevLine = iLogChain[0]

		for line in iLogChain[1:]:
			#extractFunc = getattr(self.params, "extractSignature", self.formatter.extractSignature)
			extractFunc = self.params.extractSignature
			aStoredSign = extractFunc(line)
			aComputedSign = Chainer.sign(prevLine, self.params.secret)
			isValid = hmac.compare_digest(aStoredSign, aComputedSign)

			if not isValid:
				#print("Inconsistency between lines:\nOK> %s\nKO> %s" % (prevLine, line))
				return (False, prevLine, line)
			prevLine = line
		return (True,)


class Chainer:

	def __init__(self, params):
		self.secret = params.secret
		self.prevLine = params.seed
		# Have a check for presence of signature ?
		# Use key from self registration ?
		self.formatter = params.formatter.cls(self, **params.formatter.params)

	def chainLogs(self, record):
		# That's the block-chain part!
		record.signature = Chainer.sign(self.prevLine, self.secret)
		logLine = self.formatter.stringify(record)
		self.prevLine = logLine
		return logLine

	def sign(iMessageStr, iSecretStr, iLength = 16):
		"""
		Generates a truncated signature of the input message.
		@param iLength: controls the size of the signature, set it to None for full length.
		"""
		msg = bytes(iMessageStr, "utf-8")
		key = bytes(iSecretStr,  "utf-8")
		return hmac.new(key, msg, hashlib.sha256).hexdigest()[:iLength]
