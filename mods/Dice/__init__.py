"""
Simple random dice mod for IRCbot
Matthew Russell
Apr 9, 2014
"""
#system import
import random
#Dice import
import settings


def help():
    return "Dice syntax: roll <x>d<y>\nwhere <x> and <y> are integers,\nreturns <x> rolls of d<y> dice."

def roll(sender, string):
    #try to split for integers
    try:
        numbs = string.split('d')
    except:
        return "Invalid input: " + string
    #verify numbers are integers
    try:
    	print numbs[0]
        numbs[0] = int(numbs[0])
    except ValueError:
        return "invalid number of dice"
    except AttributeError:
        return "Invalid input: ", string
    try:
        numbs[1] = int(numbs[1])
    except ValueError:
        return "invalid number of faces"
    except AttributeError:
    	return "Invalid input: ", string
    #verify they are inside the min and max int range
    if (numbs[0] >= settings.MINROLLS and numbs[0] <= settings.MAXROLLS) and (numbs[1] >= settings.MINSIDES and numbs[1] <= settings.MAXSIDES):
        reply = sender + " rolled: [" + str(random.randint(1, numbs[1]))
        for i in range(1, numbs[0]):
            reply = reply + ", " + str(random.randint(1, numbs[1]))
        #reply with randomized integers
        return reply + "]"
    else:
        return limits(None, None)

def limits(sender, string):
	return "Numbers must be between: (" + str(settings.MINROLLS) + " <= NUM_ROLLS <= " + str(settings.MAXROLLS) + ") d (" + str(settings.MINSIDES) + " <= NUM_SIDES <= " + str(settings.MAXSIDES) + ")"
