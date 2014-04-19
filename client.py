"""
a client class for IRCbot
handles how the bot client runs and calls mods

"""
#system import
import time, sys, os
#twisted import
from twisted.words.protocols import irc
from twisted.internet import protocol

#setup system path for mods input
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

#file input
import settings, logs
from PyRCbot.mods import ModLoader


class Bot(irc.IRCClient):
    #initialization
    def __init__(self):
        self.nickname = settings.NICKNAME
        self.channels = settings.CHANLIST
        self.server = settings.SERVER
        # open logger to server.txt
        self.logger = logs.Logger(settings.SERVER)
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
        reply = None
        if msg.startswith(settings.ALERTCHR):
            #if it is a command, set new variable to command name and trim message
            cmdName = msg.split(' ')
            try:
                msg = cmdName[1]
            except:
                msg = ""
            cmdName = cmdName[0].split(settings.ALERTCHR)
            cmdName = cmdName[1]
            reply = self.mods.callMod(user, msg, cmdName)
        elif self.nickname in msg:
            reply = self.mods.callMod(user, msg, "@n")
        else:
            reply = self.mods.callMod(user, msg, "@a")
        #once message gotten from mod, reply
        if reply != None:
            self.sendMsg(channel, reply)
        






