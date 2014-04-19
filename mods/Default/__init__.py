"""
Default mod, introduces the basics of mod integration into PyCbot.


"""
import settings # import the mod's settings.py

def __init__(self):
	self.a = basicClass()

def alert(sender, message):
	return self.a.b(message)

def nickMessage(sender, message):
	return "I recieved " + message

def allMessages(sender, message):
	return self.a.c()

class basicClass():
	def __init__(self):
		counter = 0

	def b(self, message):
		return "this is an alert"

	def c(self):
		counter = counter + 1
		return str(counter)

