"""
Simple random dice mod for IRCbot
Matthew Russell
Apr 19, 2014
"""

class Dice():
    #system import
    import random
    #Dice import
    import settings

    def __init__(self):
        pass

    def roll(self, sender, string):
        #try to split for integers
        try:
            numbs = string.split('d')
        except:
            return "Invalid input: " + string
        #verify numbers are integers
        try:
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
        if (numbs[0] >= self.settings.MINROLLS and numbs[0] <= self.settings.MAXROLLS) and (numbs[1] >= self.settings.MINSIDES and numbs[1] <= self.settings.MAXSIDES):
            reply = sender + " rolled: [" + str(self.random.randint(1, numbs[1]))
            for i in range(1, numbs[0]):
                reply = reply + ", " + str(self.random.randint(1, numbs[1]))
            #reply with randomized integers
            return reply + "]"
        else:
            return limits(None, None)

    def limits(self, sender, string):
    	return "Numbers must be between: (" + str(self.settings.MINROLLS) + " <= NUM_ROLLS <= " + str(self.settings.MAXROLLS) + ") d (" + str(self.settings.MINSIDES) + " <= NUM_SIDES <= " + str(self.settings.MAXSIDES) + ")"
