"""
botFactory class
makes a bot instance for each server the program will connect to
reconnects in exponential time delay
"""
#twisted input
from twisted.internet import protocol, reactor
#file input
from client import Bot

class BotFactory(protocol.ReconnectingClientFactory):
    """
    A factory for Bots.
    A new protocol instance will be created each time we connect to a server.
    """

    def buildProtocol(self, addr):
        a = Bot()
        a.factory = self
        return a

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()