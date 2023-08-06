import json
from .Basic import Basic

class Json(Basic):

	def __init__(self, params):
		"""
		['msg',
		'levelno', 'levelname',
		'module',
		'pathname',
		'filename',
		'lineno',
		'funcName',
		'exc_info', 'exc_text',
		'stack_info',
		'created', 'msecs', 'relativeCreated',
		'thread', 'threadName',
		'process', 'processName',
		'signature', 'timestamp', 'levelLetters', 'fileLine']
		"""
		super().__init__(params)

		defaultFields = ["signature", "timestamp", "levelno", "fileLine", "msg",
		                 "process", "processName", "thread", "threadName"]

		self.fields = sorted(getattr(params, "fields", defaultFields) + getattr(params, "extraFields", []))

	def stringify(self, record):
		subRecord = {f: record.__dict__[f] for f in self.fields}
		return json.dumps(subRecord, ensure_ascii = False)

	def extractSignature(line):
		return json.loads(line)["signature"]
