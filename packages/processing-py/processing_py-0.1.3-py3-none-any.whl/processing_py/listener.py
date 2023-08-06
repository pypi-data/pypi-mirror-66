from threading import Thread
import sys
class Listener(Thread):
    def __init__(self,channel):
        Thread.__init__(self)
        self.channel = channel
        self.start()
    def run(self):
        while(True):
            msg = self.channel.readline().decode('utf-8')
            if msg != '':
                print('>> '+msg,file=sys.stderr)
                
    