#!/usr/bin/python
'''
Created on Jul 24, 2012

@author:  aeon
@contact: aeon.s.flux@gmail.com
@license: GPLv3

Please keep this code private.
'''

import sys
    
from core.core import core_commands
from core.utils import bcolors
from random import choice


if __name__ == '__main__':
    
    # create a new commands module
    cc = core_commands()
    cc.initialise()
    
    sayings = ["'A journey of a thousand miles begins with a single step.' ~ Lao Tzu",
               "'You have to believe in yourself.' ~ Sun Tzu",
               "'For the wise man looks into space and he knows there is no limited dimensions.' ~ Lao Tzu",
               "'Opportunities multiply as they are seized.' ~ Sun Tzu",
               "'Music in the soul can be heard by the universe.' ~ Lao Tzu",
               "'Know thy self, know thy enemy. A thousand battles, a thousand victories' ~ Sun Tzu"]

    # set the command prompt
    
    cc.test_import()
    
    cc.prompt = "webstrike > "
    header = """%s
                     __       __      _ __      
         _    _____ / /  ___ / /_____(_) /_____ 
        | |/|/ / -_) _ \(_-</ __/ __/ /  '_/ -_)
        |__,__/\__/_.__/___/\__/_/ /_/_/\_\\__/ 
                                                

  %s""" % (bcolors.OKBLUE, bcolors.ENDC)
    
    banner = """%s    by aeon <aeon.s.flux@gmail.com>

%s\n""" % (header, choice(sayings))

    # random saying to start with ;)
    cc.cmdloop(banner)
