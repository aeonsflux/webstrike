'''
Created on Jul 24, 2012

@author: aeon
'''
import cmd
import os
import sys

if "." not in sys.path: sys.path.append(".")

import re
#import httplib
from utils import bcolors

class payload(object):
    
    def __init__(self):
        self.title          = ""
        self.description    = ""
        self.references     = ""
        self.opt_params     = {}
        self.opt_param_list = []
        self.type           = None
        
        
    def update_opt_param_list(self):
        for key in self.opt_params.iterkeys():
            self.opt_param_list.append(key)
            
            
    def set_exploit_opts(self, options):
        self.opt_params = options
        
    # to be overwritten by a payload module
    
    def get_payload_type(self):
        pass
    
    def gen_payload(self):
        pass
    
    def set_lport(self):
        pass

    def set_rport(self):
        pass
                   
    def set_title(self):
        pass

    def set_description(self):
        pass
    
    def set_author(self):
        pass
    
    def set_references(self):
        pass
    
    def register_options(self):
        pass
    
    def update_options(self):
        pass
    
    def set_platform(self):
        pass
    
        
# todo
class auxiliary(object):
    
    def __init__(self):
        self.lport = 0
        self.rport = 0
        self.title = ""
        self.description    = ""
        self.references     = ""
        self.opt_params     = {}
        self.opt_param_list = []
        
    # to be overwritten by a auxiliary module
    def set_lport(self):
        pass
    
    # not really an exploit, its 
    def exploit(self):
        pass

    def set_rport(self):
        pass
            
    def set_title(self):
        pass

    def set_description(self):
        pass
    
    def set_author(self):
        pass
    
    def set_references(self):
        pass
    
    def register_options(self):
        pass
    
    def update_options(self):
        pass
    
    def set_platform(self):
        pass

        
class exploit(object):
    """
    This is the super class for an exploit.
    it registers some parameters but can be modified by the exploit module
    """
    def __init__(self):
        
        # option parameters
        self.opt_params = {
                                #['lhost', '', 'The attackers machine to connect back to'],
                                "target":   ["", "The target machine that hosts the application"],
                                "uripath": ["", "The path to the web application"],
                                "attack":  ["0", "The default attack option to use"],
                                "tport":   ["80", "The default target port to use"],
                                "payload": ["", "The payload to use against the target"],
                           }
        
        # advanced parameters
        self.adv_params  = {
                                "ssl":   [False, "The SSL flag to run the exploit against a application using SSL"],
                                "proxy": ["", "The HTTP proxy server to set <IP:PORT>"],
                            }
        
        # option parameters List
        self.opt_param_list = ["target", "uripath", "attack", "tport", "payload"]
        
        # advanced parameters List
        self.adv_param_list = ["ssl", "proxy"]
        
        # parameters set by the loaded exploit module
        self.platform    = ""
        self.title       = ""
        self.description = ""
        self.author      = ""
        self.references  = ""
        self.payload     = None
        self.reference_links = {
                                    "edb"  :"http://www.exploit-db.com/exploits/",
                                    "bid"  :"http://www.securityfocus.com/bid/",
                                    "osvdb":"http://osvdb.org/",
                                }

    def update_options(self):
        for key in self.opt_params.iterkeys():
            if key not in self.opt_param_list:
                self.opt_param_list.append(key)

    def update_opt_param_list(self):
        pass
        
        
    def print_error(self, text):
        print "%s%s%s" % (bcolors.FAIL, text, bcolors.ENDC)
        
    def print_status(self, text):
        print "%s%s%s" % (bcolors.HEADER, text, bcolors.ENDC)

    def get_register_options(self):
        pass
    
    def gen_payload(self):
        
        #path = self.opt_params["payload"][0].split("/")
        #path = 
        
        module = self.opt_params["payload"][0]
        module_path = module.split("/")
            
        module_type = module_path[1]
        module_name = module_path[-1]
            
        module_path.pop()
        module_path = "/".join(module_path) + "/"
            
        # add the module path
        if module_path not in sys.path:
            sys.path.insert(0, module_path)
            
        #try:
        self.load_module = __import__("%s" % (module_name), fromlist=[])
            # payload handler
        self.payload = self.load_module.payload()
        self.payload.set_exploit_opts(self.opt_params)
        
        return self.payload.gen_payload()
        #except:
        #    self.print_error("\n(-) Failed to import module\n")
        #    return None
        #return None
        
    
    #def gen_payload(self):
    #    pass
        #if self.payload:
            
    def get_payload_type(self):
        #self.payload.set_payload_type()
        return self.payload.get_payload_type()
    
    # these will be overwritten with the exploit module
    def set_title(self):
        pass
    
    def set_author(self):
        pass

    def set_description(self):
        pass

    def register_options(self):
        pass
    
    def set_references(self):
        pass
    
    def exploit(self):
        pass


class module_commands(cmd.Cmd):
    '''
    This is the module commands class that handles all the commands
    when a module is loaded
    '''
    doc_header = "webstrike commands (type help <command>):"
    ruler = "%s-%s" % (bcolors.OKPURPLE, bcolors.ENDC)
    
    def print_error(self, text):
        print "%s%s%s" % (bcolors.FAIL, text, bcolors.ENDC)
        
    def print_success(self, text):
        print "%s%s%s" % (bcolors.OKPURPLE, text, bcolors.ENDC)
        
    def initialize(self, path, filename, payloads):
        
        # initialize
        self.exploit             = exploit()
        self.payload             = None #payload()
        self.path                = path
        self.filename            = filename
        self.loaded_module       = None
        self.load_module         = None
        self.load_payload_module = None
        self.loaded_payload      = None
        self.show_module_options = ["options", "opt", "advanced", "adv", "payloads", "pay"]
        self.module_type         = ""
        # list of available payloads
        self.payloads            = payloads
        #print "initializing"
        #
        
    # cleaner output    
    def default(self, line):
        """Called on an input line when the command prefix is not recognized.

        If this method is not overridden, it prints an error message and
        returns.

        """
        self.print_error("\n(-) Invalid parameter %s, use 'help' for more information\n" % (line))
        
    def emptyline(self):
        pass
    
    def import_exploit_module(self, mtype, mpath):

        # add the mpath
        if mpath not in sys.path:
            sys.path.insert(0, self.path)
            
        try:
            self.load_module = __import__("%s" % (self.filename), fromlist=[])
        except:
            self.print_error("\n(-) Failed to import module\n")
            sys.exit(1)
        
        # update the base exploit class
        self.module_type = mtype
        
        if mtype.lower() == "exp" or mtype.lower() == "exploits":
            try:
                self.loaded_module = self.load_module.exploit()
            except:
                self.print_error("(-) Module has a syntax error\n")
                sys.exit(1)
        elif mtype == "pay":
            try:
                self.loaded_module = self.load_module.payload()
            except:
                self.print_error("(-) Module has a syntax error\n")
                sys.exit(1)
            
            # set the type only for payload modules
            self.loaded_module.set_type()
            
        elif mtype == "aux":
            try:
                self.loaded_module = self.load_module.auxiliary()
            except:
                self.print_error("(-) Module has a syntax error\n")
                sys.exit(1)
            
        # initialize loading of the exploit/auxilery/payload module
        self.loaded_module.set_title()
        self.loaded_module.set_description()
        self.loaded_module.set_author()
        self.loaded_module.set_references()
        self.loaded_module.register_options()
        self.loaded_module.update_options()
        self.loaded_module.set_platform()
        
    def import_payload_module(self, payload):
            
        module = payload
        module_path = module.split("/")
                
        #module_type = module_path[1]
        module_name = module_path[-1]
                
        module_path.pop()
        module_path = "/".join(module_path) + "/"
                
            # add the module path
        if module_path not in sys.path:
            sys.path.insert(0, module_path)
                
        try:
            self.load_payload_module = __import__("%s" % (module_name), fromlist=[])
            # payload handler
            
        except:
            self.print_error("\n(-) Failed to import module\n")

        self.loaded_payload = self.load_payload_module.payload()
        self.loaded_payload.register_options()
        
        # set the type only for payload modules
        #self.loaded_payload._payload_type()

        # updated the loaded module list so we are all sweet
        self.loaded_module.opt_params = \
        dict(self.loaded_payload.opt_params.items() + self.loaded_module.opt_params.items())
        
        #self.loaded_module.
        
    def str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")
  
    def do_set(self, line):
        param = None
        if " " in line:
            param = line.split(" ")[0]
            value = line.split(" ")[1]
                    
            # if the payload is set as well as the exploit module
            if self.loaded_payload:
                
                if param.lower() in self.loaded_module.adv_params:
                    self.print_success("\n%s => %s\n" % (param, value))
                    if param.lower() == "ssl":
                        self.loaded_module.adv_params[param.lower()][0] = self.str2bool(value)
                    else:
                        self.loaded_module.adv_params[param.lower()][0] = value
                    #return True
                    
                self.loaded_payload.update_opt_param_list() 
                
                # append the payload advanced options   
                updated_opt_param_list = self.loaded_payload.opt_param_list + self.loaded_module.opt_param_list
            
            # if the exploit, payload or auxiliary module is loaded only
            elif not self.loaded_payload:

                if param.lower() in self.loaded_module.opt_params:
                    self.print_success("\n%s => %s\n" % (param, value))
                    self.loaded_module.opt_params[param.lower()][0] = value
                
                if param.lower() in self.loaded_module.adv_params:
                    self.print_success("\n%s => %s\n" % (param, value))
                    if param.lower() == "ssl":
                        self.loaded_module.adv_params[param.lower()][0] = self.str2bool(value)
                    else:
                        self.loaded_module.adv_params[param.lower()][0] = value
                        
                self.loaded_module.update_opt_param_list()
                updated_opt_param_list = self.loaded_module.opt_param_list
            
            if value in self.payloads:
                print "here??"
                if param.lower() not in updated_opt_param_list and \
                    param.lower() not in self.loaded_module.adv_params:
                    self.print_error("\n(-) Invalid parameter '%s' for the set command, use 'help set' for more information\n" % (param))
                
                elif param.lower() in updated_opt_param_list:
                    print updated_opt_param_list
                    print "\n%s => %s\n" % (param, value)
                    
                    # set the parameters here
                    self.loaded_module.opt_params[param.lower()][0] = value
                
        elif " " not in line:
            if line.lower() not in self.loaded_module.opt_param_list:
                self.print_error("\n(-) Invalid parameter '%s' for the set command, use 'help set' for more information" % (line))
            

        if param == "payload" or param == "pay":
            if value in self.payloads:
                self.import_payload_module(value)
            else:
                self.print_error("\n(-) Invalid payload type")
        elif not param:
            self.print_error("(-) unspecfied value for parameter '%s'\n" % line)

    # ok, lets exploit the target....  
    
    def help_exploit(self):
        self.print_success("\n(+) Attempts to exploit the target using the current module and its settings\n")

    def help_info(self):
        self.print_success("\n(+) Displays module information and available options\n")
        
    def help_set(self):
        self.print_success("\n(+) Sets an available option to a specified value\n")
        
    def help_show(self):
        #self.print_success("\n(+) Shows the available options\n")
        self.print_success("\n(+) show a specific set of options/modules/ using:\n")
        for module_type in self.show_module_options:
            self.print_success("\tshow %s" % (module_type))
        self.print_success("")

    def help_exit(self):
        self.print_success("\n(+) Exits this loaded module\n")
        
    def help_help(self):
        self.print_success("\n(+) Displays the available commands!\n")

    def help_unload(self):
        self.print_success("\n(+) Unloads the currently loaded module\n")
        
    def do_exploit(self, line):
        
        derivedclass = str(type(self.loaded_module))
        derivedclass = re.search ("<class '(.*)'>", derivedclass)
        ihateregex = derivedclass.group(0).split(".")[1]
        ihateregex = ihateregex[:-2]
        
        if ihateregex == "exploit":
            if self.loaded_payload:
                self.loaded_module.exploit()
            else:
                self.print_error("\n(-) Please specify a payload for exploitation\n")
        elif ihateregex == "payload":
            #print "payload"
            outputname = raw_input('\n(+) Please specify the output name: ')
            if len(outputname) > 0:
                try:
                    shell = open(outputname,"w") 
                except:
                    self.print_error("\n(-) Cannot write to the path %s, check your permissions\n" % outputname)
                    return True
                payload = "<?php %s ?>" % (self.loaded_module.gen_payload())
                shell.write(payload)
                #os.getcwd()
                print "(+) Written %s to %s/%s\n" % (self.loaded_module.title, os.getcwd(), outputname)
                shell.close()
                
        else:
            print "non exploit, non payload %s" % (ihateregex)
            
            

    def show_options(self):
        print ""
        print "\tExploit"
        print "\t-------\n"
        # http://stackoverflow.com/questions/5084743/how-to-print-pretty-string-output-in-python
        template = "\t{0:10}{1:35}{2:20}" # column widths: 8, 10, 15, 7, 10
        print template.format("OPTION", "VALUE", "DESCRIPTION") # header
        print template.format("------", "-----", "-----------") # header
        
        for opt,val in self.loaded_module.opt_params.iteritems():
            
            # http://stackoverflow.com/questions/3501382/checking-whether-a-variable-is-an-integer-or-not
            if isinstance( val[0], int ):
                val[0] = "%s" % (val[0])
            
            # make it align to the table header
            if len(val) == 2:
                val.insert(0,opt)
            print template.format(*val)
            val.pop(0)
            
        if self.loaded_payload:
            print ""
            print "\tPayload"
            print "\t-------\n"
            print template.format("OPTION", "VALUE", "DESCRIPTION") # header
            print template.format("------", "-----", "-----------") # header
            #print "payload is loaded.. show its options..."
            for opt,val in self.loaded_payload.opt_params.iteritems():
                # http://stackoverflow.com/questions/3501382/checking-whether-a-variable-is-an-integer-or-not
                if isinstance( val[0], int ):
                    val[0] = "%s" % (val[0])
                
                # make it align to the table header
                if len(val) == 2:
                    val.insert(0,opt)
                print template.format(*val)
                val.pop(0)
            
            
    def show_advanced_options(self):
        print ""
        # http://stackoverflow.com/questions/5084743/how-to-print-pretty-string-output-in-python
        template = "\t{0:10}{1:20}{2:20}" # column widths: 8, 10, 15, 7, 10
        print template.format("OPTION", "VALUE", "DESCRIPTION") # header
        print template.format("------", "-----", "-----------") # header
        
        for opt,val in self.loaded_module.adv_params.iteritems():
                
            # http://stackoverflow.com/questions/3501382/checking-whether-a-variable-is-an-integer-or-not
            if isinstance( val[0], int ):
                val[0] = "%s" % (val[0])
                
            # make it align to the table header
            if len(val) == 2:
                val.insert(0,opt)
            print template.format(*val)
            val.pop(0)
    
    def show_payloads(self):
        print ""
        print ""
        print "\t======= Payload Modules ======="
        print ""  
        i = 0
        for r,d,f in os.walk("modules"):
            for files in f:
                if self.loaded_module.platform:
                    if files.endswith(".py") and self.loaded_module.platform in os.path.join(r,files[:-3]):
                        i += 1
                        print "\t%d. %s" % (i,os.path.join(r,files[:-3]))

    def do_show(self, line):
        
        line = line.lower()
        if line == "options" or line == "opt":
            self.show_options()
        elif line == "advanced" or line == "adv":    
            self.show_advanced_options()
        elif line == "payloads" or line == "pay":    
            self.show_payloads()
        print ""
        
    def do_info(self, line):
        
        print "\n\t%s" % (self.loaded_module.title)
        print "\t" + "=" * len(self.loaded_module.title)
        
        print "\n\tDescription:"
        print "\t============"
        print self.loaded_module.description
        
        print "\n\tAuthor(s):"
        print "\t=========="
        for author in self.loaded_module.author:
            author_name    = author[0]
            author_contact = author[1]
            print "\t%s %s" % (author_name, author_contact)
        
        print ""
        
        if len(self.loaded_module.references) > 0:
            print "\tReference(s):"
            print "\t============="
            for ref in self.loaded_module.references:
                #print "%s" % (ref)
                
                uri = self.exploit.reference_links[ref[0]]
                
                uri = "\t%s%s" % (uri,ref[1])
                print uri
        print ""
        
        if len(self.loaded_module.opt_params) > 0:
            print "\tAvailable options:"
            print "\t=================="
            self.show_options()
            print ""
        
    # unload the module and return to our command prompt
    def do_unload(self, line):
        print ""
        return True

    # unload the module and return to our command prompt
    def do_exit(self, line):
        return True
    
    # auto complete the search command
    def complete_set(self, text, line, start_index, end_index):
        
        # if the payload is loaded, we will update the option list and display it back
        if self.loaded_payload:
            self.loaded_payload.update_opt_param_list()    
            updated_opt_param_list = self.loaded_payload.opt_param_list + self.loaded_module.opt_param_list
            if text:
                return [i for i in updated_opt_param_list if i.startswith(text)]
            else:
                return updated_opt_param_list
            
        elif not self.loaded_payload:
            if text:
                return [i for i in self.loaded_module.opt_param_list if i.startswith(text)]
            else:
                return self.loaded_module.opt_param_list
            

    # auto complete the search command
    def complete_show(self, text, line, start_index, end_index):
        if text:
            return [i for i in self.show_module_options if i.startswith(text)]
        else:
            return self.show_module_options

# derived cmd.Cmd class
class core_commands(cmd.Cmd):
    '''
    This is the core commands class that handles all the commands
    when no module is loaded
    '''

    doc_header = "webstrike commands (type help <command>):"
    ruler = "%s-%s" % (bcolors.OKPURPLE, bcolors.ENDC)
        
    #http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-in-python
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    def initialise(self):
        # we need this for the tab complete
        self.module_list    = ["exp", "exploits", "aux", "auxiliary", "pay", "payloads", "all"]
        self.command_options = ['...', 'wordpress', 'joomla', 'sugarcrm']
        self.module_name_dict = {
                                    "exploits":  "exploit",
                                    "exp":       "exploit",
                                    "auxiliary": "auxiliary",
                                    "aux":       "auxiliary",
                                    "payloads":  "payload",
                                    "pay":       "payload",
                                    "all":       "Available"
                                }
        # get lists of all modules 
        self.payload_modules   = []
        self.exploit_modules   = []
        self.auxiliary_modules = []
        self.all_modules       = []
        for r,d,f in os.walk("modules"):
            for files in f:
                if files.endswith(".py") and "/exploits/" in os.path.join(r,files[:-3]):
                    self.exploit_modules.append(os.path.join(r,files[:-3]))
                elif files.endswith(".py") and "/payloads/" in os.path.join(r,files[:-3]):
                    self.payload_modules.append(os.path.join(r,files[:-3]))
                elif files.endswith(".py") and "/auxiliary/" in os.path.join(r,files[:-3]):
                    self.auxiliary_modules.append(os.path.join(r,files[:-3]))
                
                if files.endswith(".py") and files != "__init__.py":
                    self.all_modules.append(os.path.join(r,files[:-3]))
        
        # now lets store them in a hash map
        self.module_dict = {
                                "exploits":  self.exploit_modules,
                                "exp":       self.exploit_modules,
                                "auxiliary": self.auxiliary_modules,
                                "aux":       self.auxiliary_modules,
                                "payloads":  self.payload_modules,
                                "pay":       self.payload_modules,
                                "all":       self.all_modules,
                            }
        
    def test_import(self):

        print "\n(+) Validating modules\n"
        template = "\t{0:80}{1:6}" # column widths: 8, 10, 15, 7, 10
        print template.format("Module", "Status") # header
        print template.format("------", "------") # header
        
        for module in self.all_modules:
            
            module_to_load = "%s.py" % module
            try:
                module_dir, module_file = os.path.split(module_to_load)
                module_name, module_ext = os.path.splitext(module_file)
                save_cwd = os.getcwd()
                #print "dir: %s" % module_dir
                os.chdir(module_dir)
                module_obj = __import__(module_name)
                
                module_obj.__file__ = module_to_load
                globals()[module_name] = module_obj
                os.chdir(save_cwd)
                module = module.replace("modules/","")
                print template.format(module, "[OK]")
            except ImportError, e:
                print template.format(module, "[FAIL]")
                print "\n(-) failed to load module: %s. reason: %s" % (module, e)
        
        
    def print_error(self, text):
        print "%s%s%s" % (bcolors.FAIL, text, bcolors.ENDC)
        
    def print_success(self, text):
        print "%s%s%s" % (bcolors.OKPURPLE, text, bcolors.ENDC)
        
    # cleaner output    
    def default(self, line):
        """Called on an input line when the command prefix is not recognized.

        If this method is not overridden, it prints an error message and
        returns.

        """
        self.print_error("\n(-) Invalid parameter %s, use 'help' for more information\n" % (line))

    # do the search against all modules
    def do_search(self, line):
        """
        searches the all_modules lists and matches a module based on its path/name 
        and contents 
        """
        i = 0
        print ""
        print "\t======= Matching Modules ======="
        print "" 
        for module in self.all_modules:
            
            f = open("%s.py" % module)
            if line in module:
                i += 1
                print "\t%d. %s" % (i,module)
            elif line in f.read():
                i += 1
                print "\t%d. %s" % (i,module)
        print ""

    def do_exit(self, line):
        return True

    def do_intro(self, line):
        print '\nwelcome to webstrike'
        print '===================='
        print 'webstrike is a framework for application specific web attacks and comes pre-packaged with'
        print 'exploits and auxiliary modules targeting a variety of applications. It has a custom persistant'
        print 'trojan called \'ronin\' which you can use to setup usermode rootkit. You can choose to develop' 
        print 'modules or use the existing ones. If you are going to develop modules then please build them to'
        print 'the specifications outlined in docs/DEVELOP.\n'

    def do_load(self, line):

        # load by name
        #elif not self.is_number(line):
        #print self.all_modules
        mod_name = "modules/%s" % line
        if mod_name in self.all_modules:
            #if line in self.all_modules:
            i = module_commands()
            module_path = mod_name.split("/")
            module_name = module_path[-1]
            module_type = module_path[1] # type will always be the same
                        
            i.prompt = self.prompt[:-3]+' %s(%s%s%s) > ' % \
            (module_type, bcolors.OKBLUE, module_name, bcolors.ENDC)
                        
            module_path.pop()
            module_path = "/".join(module_path) + "/"

            i.initialize(module_path, module_name, self.payload_modules)
            i.import_exploit_module(module_type, module_path)
            i.cmdloop()
        
    def do_unload(self, line):
        return True
        
        
    def emptyline(self):
        pass
        
    # shows the generic subset of available code
    def do_show(self, line):
        
        line = line.lower()
        
        if line not in self.module_dict:
            self.print_error("\n(-) Invalid parameter %s, use 'help show' for more information" % (line))
        elif line in self.module_dict:
            print ""
            print "\t======= %s%s Modules =======" \
                % (self.module_name_dict[line][0].capitalize(), self.module_name_dict[line][1:])
            print ""
            i = 0
            for module in self.module_dict[line]:
                i += 1
                print "\t%d. %s" % (i,module)
        print ""

        
    # do help
    
    def help_intro(self):
        self.print_success("\n(+) Displays the introduction to webstrike\n")
        
        
    def help_search(self):
        print "\n(+) search for a specific module\n"

    def help_show(self):
        print "\n(+) show a specific set of modules using:\n"
        for module_type in self.module_list:
            print "\tshow %s" % (module_type)
            
        print ""

    def help_help(self):
        print "\n(+) lists the available commands\n"

    def help_exit(self):
        print "\n(+) exits from the console\n"

    def help_load(self):
        print "\n(+) loads a module by specifying the module name\n"

    def help_unload(self):
        print "\n(+) unloads a module\n"
        
    # auto complete the search command
    def complete_search(self, text, line, start_index, end_index):
        
        if text:
            return [i for i in self.command_options if i.startswith(text)]
        else:
            return self.command_options

    # auto complete the show_module_options command
    def complete_show(self, text, line, start_index, end_index):
        
        if text:
            return [i for i in self.module_list if i.startswith(text)]
        else:
            return self.module_list

    # auto complete the show_module_options command
    def complete_load(self, text, line, start_index, end_index):
        
        if text:
            return [i for i in self.module_list if i.startswith(text)]
        else:
            return self.module_list

        
