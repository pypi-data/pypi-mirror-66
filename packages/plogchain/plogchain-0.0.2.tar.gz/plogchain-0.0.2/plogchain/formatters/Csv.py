

class Csv:

	def stringify(self, record):
		# TODO: use cvs package
		return ';'.join(record.values())
