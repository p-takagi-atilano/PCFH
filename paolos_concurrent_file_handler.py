import os
import time

# PCFH stands for Paolo's Concurrent File Handler
# fname is file name
# typ is handler type ('r', 'w', 'a', etc)
# delay is hyperparameter, see open function
class PCFH:
	def __init__(self, fname, typ, delay=0.01):
		self.fname = fname
		self.lock = fname + '.lock'
		self.typ = typ
		self.delay = delay
		self.handler = None

	# Returns if this PCFH instance has opened a file already
	# If not, will wait to open file until lock file deleted
	# Waits self.delay seconds between iterations
	def open(self):
		if not self.handler:
			while os.path.isfile(fname + '.lock'):
				time.sleep(self.delay)
			with open(self.lock) as f:
				pass
			self.handler = open(self.fname, self.typ)
			return True
		return False

	# Returns whether this PCFH instance locked the file
	# If so, will remove lock file, and close and rest handler
	def close(self):
		if self.handler:
			os.remove(self.lock)
			self.handler.close()
			self.handler = None
			return True
		return False

	# Returns whether this PCFH instance locked the file
	# Will write s (str) to file only if handler can
	# Otherwise, throws io.UnsupportedOperation
	def write(self, s):
		if self.handler:
			self.handler.write(s)
			return True
		return False

	# Returns false if this PCFH instance hasn't locked the file
	# Reads next i characters of file
	def read(self, i):
		if self.handler:
			return self.handler.read(i)
		return False

	# This is not recommended
	def get_handler(self):
		return self.handler

	'''
	def readline():
		if self.handler:
			return self.handler.readline()
		return False
	'''

	# Returns whether or not file is locked
	def is_locked(self):
		return os.path.isfile(self.lock)

	# Returns whether or not file locked by this PCFH instance
	def is_locked_by_me(self):
		return bool(os.path.isfile(self.lock) and self.handler)
