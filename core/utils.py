'''
Created on Sep 17, 2012

@author: aeon
more colors here if needed
http://www.siafoo.net/snippet/88
'''

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OKPURPLE = '\033[1;35m'
    #ENDC = '\033[1;m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
