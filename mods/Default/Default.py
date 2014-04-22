"""
default mod
"""
import settings
# Default's commands can be called directly because they are listed in settings.py for Default
class Default():
	def __init__(self):
		self.a = AnotherClass()
		#self.settings = settings

	def alert(self, sender, message):
		return "I have recieved %i messages that were not commands or mentions" % (self.a.ret())

	def nick(self, sender, message):
		return "%s mentioned me! :D" % (sender)

	def all(self, sender, message):
		self.a.inc()

# AnotherClass cannot be called directly from IRC
class AnotherClass():
	def __init__(self):
		self.counter = 0

	def inc(self):
		self.counter = self.counter + 1

	def ret(self):
		return self.counter
