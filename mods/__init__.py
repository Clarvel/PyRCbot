"""
imports all mods indicated in IRCBot/settings.py and sets up an array of their names
Matthew Russell
Apr 9, 2014

Inefficient, would like to set up a refrence table for all commands in the mods, 
refrence mod name by that instead of searching through all the mods
"""
#system imports
import sys, importlib

#IRCbot settings import, for activated mods list
import settings

class ModLoader():
	def __init__(self):
		self.loadMods()

	#load all mods listed in IRCBot/settings.py
	def loadMods(self):
		self.loadedMods = []
		self.basiccmds = []
		self.nickcmds  = []
		self.msgscmds  = []
		for modName in settings.MODS:
			try:
				mod = __import__(modName, globals(), locals(), [], -1)
			except ImportError as error:
				print "Import of mod '%s' failed: %s" % (modName, error)
			else:
				self.loadedMods.append(mod)
				index = len(self.loadedMods) - 1
				#import command into one of the lists with an integer indexing the mod
				try:
					for command in mod.settings.COMMANDS:
						temp = [command, index]
						self.basiccmds.append(temp)
				except AttributeError as error:
					pass
				try:
					for command in mod.settings.NICKCMDS:
						temp = [command, index]
						self.nickcmds.append(temp)
				except AttributeError as error:
					pass
				try:
					for command in mod.settings.ALLMSGS:
						temp = [command, index]
						self.msgscmds.append(temp)
				except AttributeError as error:
					pass
		print "Loaded mods: ", self.loadedMods

	#finds the mod the command originated form, returns the run command
	def callMod(self, sender, MSG, command):
		#search through the mods to find the relevant command, if found return that string
		"""
		could use work, rather ugly
		"""
		if command == "@n":
			for listcmd in self.nickcmds:
				mod = self.loadedMods[listcmd[1]] 
				# try running the command and return
				try:
					print "From Mod: ", mod.__name__, " excecuting: ", listcmd[0], " on message: ", MSG
					temp = getattr(mod, listcmd[0])(sender, MSG)
				except AttributeError as error:
					print "Mod function error: %s" % (error)
				else:
					return temp
		elif command == "@a":
			for listcmd in self.msgscmds:
				mod = self.loadedMods[listcmd[1]] 
				# try running the command and return
				try:
					print "From Mod: ", mod.__name__, " excecuting: ", listcmd[0], " on message: ", MSG
					temp = getattr(mod, listcmd[0])(sender, MSG)
				except AttributeError as error:
					print "Mod function error: %s" % (error)
				else:
					return temp
		else:
			for listcmd in self.basiccmds:
				if listcmd[0] == command:
					# mod found
					mod = self.loadedMods[listcmd[1]] 
					# try running the command and return
					try:
						print "From Mod: ", mod.__name__, " excecuting: ", command, " on message: ", MSG
						temp = getattr(mod, listcmd[0])(sender, MSG)
					except AttributeError as error:
						print "Mod function error: %s" % (error)
					else:
						return temp










