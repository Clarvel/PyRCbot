"""
Matthew Russell
last updated April 19, 2014
a client class for IRCbot
handles how the bot client runs and calls mods

"""
#system import
import time

#twisted import
from twisted.words.protocols import irc
from twisted.internet import protocol

#file input
import settings
from logger import Logger
from modloader import ModLoader
from console import Console


class Bot(irc.IRCClient):
    #initialization
    def __init__(self):
        self.nickname = settings.NICKNAME
        self.channels = settings.CHANLIST
        self.server = settings.SERVER
        # open logger to server.txt
        self.logger = Logger(settings.SERVER)
        # open bot to console input
        self.console = Console(self)
        # load mods
        self.mods = ModLoader()

    #default message sender and autologger
    def sendMsg(self, channel, msg):
        self.msg(channel, msg)
        self.logger.log("[%s] <%s> %s" % (channel, self.nickname, msg))
    
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger.log("[connected at %s]" % time.asctime(time.localtime(time.time())))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" % time.asctime(time.localtime(time.time())))


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        for channel in settings.CHANLIST:
            self.join(channel)
        self.logger.log("[" + self.nickname + " has joined %s]" % self.server)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.logger.log("[" + self.nickname + " has joined %s]" % channel)

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        self.logger.log("[%s] * %s %s" % (channel, user, msg))

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("%s is now known as %s" % (old_nick, new_nick))

    # For fun, override the method that determines how a nickname is changed on
    # collisions. The default method appends an underscore.
    def alterCollidedNick(self, nickname):
        """
        Generate an altered version of a nickname that caused a collision in an
        effort to create an unused related name for subsequent registration.
        """
        return "_" + nickname

    
    def privmsg(self, user, channel, msg):
        #This will get called when the bot receives any message.
        user = user.split('!', 1)[0] #user is the person sending the message
        #log the message
        self.logger.log("[%s] <%s> %s" % (channel, user, msg))
        # Check to see if it is a command message
        reply = []
        if msg.startswith(settings.ALERTCHR):
            #if it is a command, set new variable to command name and trim message
            msg = msg.split(settings.ALERTCHR)
            msg.remove('')
            for a in msg:
                command = a.split(' ')[0]
                try:
                    message = a.split(command + ' ')[1]
                except IndexError:
                    pass
                else:
                    reply.append(self.mods.callMod(user, message, command))
        elif self.nickname in msg:
            reply.append(self.mods.callMod(user, msg, "@n"))
        else:
            reply.append(self.mods.callMod(user, msg, "@a"))
        #once messages gotten from mod, reply
        for msgs in reply:
            self.sendMsg(channel, msgs)
        







