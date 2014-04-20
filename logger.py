"""
Logger handles saving messages to the logs (and possibly writing to terminal??)

Matthew Russell
April 19, 2014
"""
#system import
import time, os

class Logger:

    def __init__(self, filename):
    	#open file in append mode
    	path = os.path.join(os.path.dirname(__file__), "logs/%s.txt" % (filename))
        self.file = open(path, "a")

    def log(self, message):
        #Write a message to the file.
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write("%s %s\n" % (timestamp, message))
        self.file.flush()
        #Write a message to the terminal
        print "%s %s" % (timestamp, message)

    def close(self):
        self.file.close()