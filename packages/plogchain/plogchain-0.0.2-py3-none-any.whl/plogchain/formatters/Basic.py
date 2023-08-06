import logging

# ISO 8601 timestamp
from datetime import datetime

class Basic(logging.Formatter):
	"""
	Base model for all custom formatters.
	"""
	def __init__(self, params):
		self.secret = params.secret
		self.prevLine = params.seed
		# Have a check for presence of signature ?
		logging.Formatter.__init__(self, fmt = params.format)

	def format(self, record):
		"""
		Shared method where the block-chain part is coded.
		"""
		record.signature = sign(self.prevLine, self.secret)
		record.timestamp = datetime.fromtimestamp(record.created).isoformat()
		record.levelLetters = record.levelname[:4]
		record.fileLine = record.filename  + ':' + str(record.lineno)
		logLine = self.stringify(record)
		self.prevLine = logLine
		return logLine

	def stringify(self, record):
		"""
		Specific method to transform the recod to string.
		"""
		return logging.Formatter.format(self, record)

import hashlib
import hmac
def sign(iMessageStr, iSecretStr, iLength = 16):
	"""
	Generates a truncated signature of the input message.
	@param iLength: controls the size of the signature, set it to None for full length.
	"""
	msg = bytes(iMessageStr, "utf-8")
	key = bytes(iSecretStr,  "utf-8")
	return hmac.new(key, msg, hashlib.sha256).hexdigest()[:iLength]
