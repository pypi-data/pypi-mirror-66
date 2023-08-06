import logging
from datetime import datetime, timezone

import hashlib
import hmac


class Basic(logging.Formatter):
	"""
	Base model for all custom formatters.
	"""
	def __init__(self, params):
		self.secret = params.secret
		self.prevLine = params.seed
		#self.signTrunc = getattr(params, "signTrunc", 16)

		# Have a check for presence of signature ?
		logging.Formatter.__init__(self, fmt = params.format)
		self.timestampFmt = params.timestampFmt
		self.timestampUtc = params.timestampUtc
		self.timestampPrecision = params.timestampPrecision


	def format(self, record):
		"""
		Shared method where the block-chain part is coded.
		"""
		record.signature = Basic.sign(self.prevLine, self.secret)
		record.levelLetters = record.levelname[:4]
		record.fileLine = record.filename  + ':' + str(record.lineno)
		record.timestamp = self.makeTimestamp(record)

		logLine = self.stringify(record)
		self.prevLine = logLine
		return logLine


	def makeTimestamp(self, record):
		"""
		Because formatTime called internally by logging.Formatter.format,
		we prefer a custom timestamp generation + an explicit `timestamp` name.
		We can customize the timezone, the decimal separator and number of digits.
		"""
		ts = datetime.fromtimestamp(record.created)

		if self.timestampUtc:
			ts = ts.astimezone(tz = timezone.utc).replace(tzinfo = None)

		if self.timestampFmt == "iso":
			return ts.isoformat(sep = ' ', timespec = self.timestampPrecision)
		else:
			# TODO, apply only if %f present
			aTrunc = 3 if self.timestampPrecision == "milliseconds" else None
			return ts.strftime(self.timestampFmt)[:aTrunc]


	def stringify(self, record):
		"""
		Specific method to transform the recod to string.
		"""
		return logging.Formatter.format(self, record)

	@staticmethod
	def sign(iMessageStr, iSecretStr, iLength = 16):
		"""
		Generates a truncated signature of the input message.
		@param iLength: controls the size of the signature, set it to None for full length.
		"""
		msg = bytes(iMessageStr, "utf-8")
		key = bytes(iSecretStr,  "utf-8")
		return hmac.new(key, msg, hashlib.sha256).hexdigest()[:iLength]

	@staticmethod
	def extractSignature(line):
		return line[line.rindex('|') + 1:]
