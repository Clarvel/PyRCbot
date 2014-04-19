"""
Matthew Russell
apr 7 2014

Main runfile
based on twistedmatrix's ircLogBot.py example: http://twistedmatrix.com/documents/current/words/examples/index.html

modable irc bot
"""
#system imports
import sys

#twisted imports
from twisted.python import log
from twisted.internet import reactor

#file imports
import settings, factory

if __name__ == '__main__':
    #start logging to terminal consider removing
    log.startLogging(sys.stdout)
    #initialize a factory protocol and application instance
    botInstance = factory.BotFactory()
    #connect factory instance to target host and port
    reactor.connectTCP(settings.SERVER, settings.IRC_PORT, botInstance)
    #run bot
    reactor.run()