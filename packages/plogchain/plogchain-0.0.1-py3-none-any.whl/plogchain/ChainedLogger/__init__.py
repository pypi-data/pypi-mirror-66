#! /usr/bin/env python3

import logging
import secrets

import hashlib
import hmac

kVerbosityToLevel = {
	0: logging.ERROR,
	1: logging.WARNING,
	2: logging.INFO
}

class ChainedFormatter(logging.Formatter):
	def __init__(self, iSecret):
		self.secret = iSecret
		self.prevLine = secrets.token_urlsafe() # Init with random string
		aLogFormat = "%(asctime)s.%(msecs)03d|%(signature)s|%(filename)s:%(lineno)d %(funcName)-15s %(message)s"
		logging.Formatter.__init__(self, aLogFormat, datefmt = "%F %T")

	def format(self, record):
		record.signature = sign(self.prevLine, self.secret)
		logLine = logging.Formatter.format(self, record)
		self.prevLine = logLine
		return logLine

def sign(iMessageStr, iSecretStr, iLength = 16):
	"""
	Generates a truncated signature of the input message.
	"""
	msg = bytes(iMessageStr, "utf-8")
	key = bytes(iSecretStr, "utf-8")
	return hmac.new(key, msg, hashlib.sha256).hexdigest()[:iLength]

def extractSignature(iLine):
	return iLine.split("|")[1]

def verify(iLogChain, iSecretStr):
	"""
	Check the consistency of a log chain with the secret.
	In case of failure, a tuple is returned with
	- check result: False
	- last consistent line
	- first inconsistent line
	"""
	prevLine = iLogChain[0]

	for line in iLogChain[1:]:
		aStoredSign = extractSignature(line)
		aComputedSign = sign(prevLine, iSecretStr)
		isValid = hmac.compare_digest(aStoredSign, aComputedSign)

		if not isValid:
			#print("Inconsistency between lines:\nOK> %s\nKO> %s" % (prevLine, line))
			return (False, prevLine, line)
		prevLine = line
	return (True)

def generateSecret(iLength = 128):
	"""
	For convenience
	"""
	return secrets.token_urlsafe(iLength)

def init(iVerbosity, iSecret, iStream = None):
	"""
	Entrypoint for initializing the log chain.
	"""
	aLevel = kVerbosityToLevel.get(iVerbosity, logging.DEBUG)
	logging.basicConfig(level = aLevel, stream = iStream)
	handler = logging.getLogger().handlers[0]
	handler.setFormatter(ChainedFormatter(iSecret))
