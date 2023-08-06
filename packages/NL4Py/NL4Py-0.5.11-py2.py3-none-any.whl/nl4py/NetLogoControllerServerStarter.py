'''NL4Py, A NetLogo controller for Python
Copyright (C) 2018  Chathika Gunaratne

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

from py4j.java_gateway import JavaGateway
from py4j.protocol import Py4JNetworkError
from py4j.protocol import Py4JError
import subprocess
import threading
import os
import atexit
import sys
import logging
import time
import psutil
import math
import platform
import glob
import pkg_resources
from os import listdir
from os.path import isfile, join


##############################################################################
'''Responsible for starting and stopping the NetLogo Controller Server'''
class NetLogoControllerServerStarter:
    SERVER_PATH = pkg_resources.resource_filename('nl4py', 'nl4pyServer/')
    __gw = None# New gateway connection 
    ##server is in netlogo app folder
    
    
    def __init__(self):
        self.__gw = JavaGateway()
        self.shutdownServer()
        #atexit.register(self.shutdownServer)
    '''Internal method to start JavaGateway server. Will be called by starServer on seperate thread'''
    def __runServer(self,netlogo_home): 
        __server_name = "nl4py.server.NetLogoControllerServer"
        nl_path = ""
        if netlogo_home == None:
            #Following is legacy for 0.3.0 support and is deprecated with 0.3.1
            try:
                nl_home = os.environ['NETLOGO_HOME']
                if(platform.system() == "Darwin"):
                    nl_path = os.path.join(nl_home,"Java")
                else:
                    nl_path = os.path.join(nl_home,"app")
            except KeyError:            
                try:
                    nl_path = os.environ['NETLOGO_APP']
                except KeyError:
                    #looks like the NETLOGO_APP variable isn't set... 
                    #Trying to use os dependent defaults
                    print("NETLOGO_APP was not set, trying to find NetLogo .jar files")
                    if(platform.system() == "Windows"):
                        nl_path = "C:/Program Files/NetLogo 6.0.2/app"
                    if(platform.system() == "Darwin"):
                        nl_path = "/Applications/NetLogo 6.0.2/Java"
                    pass
                pass
            #End
        else:
            if(platform.system() == "Darwin"):
                nl_path = os.path.join(netlogo_home,"Java")
            else:
                nl_path = os.path.join(netlogo_home,"app")
        if len(glob.glob(os.path.join(nl_path,"netlogo-[0-9]*.jar"))) == 0:
            print("NetLogo not found! Please provide netlogo_home directory to nl4py.startServer()")
            return
        else:
            ver_info = os.path.split(glob.glob(os.path.join(nl_path,"netlogo-[0-9]*.jar"))[0])[-1].split(".")
            major = float(ver_info[0].split("-")[-1])
            minor = float("0." + ver_info[1])
            major_minor = major + minor
            if major_minor < 6.1:
                os.environ['NL4Py_NetLogo_Ver'] = "6.1"
                self.SERVER_PATH = os.path.join(self.SERVER_PATH,"NetLogo6.0")
            else: 
                os.environ['NL4Py_NetLogo_Ver'] = "6.0"
                self.SERVER_PATH = os.path.join(self.SERVER_PATH,"NetLogo6.1")
        #else:
            #print("NetLogo found")
        nl_docs = "-Dnetlogo.docs.dir=" + os.path.join(nl_path,"docs")
        nl_extensions = "-Dnetlogo.extensions.dir=" + os.path.join(nl_path,"extensions")
        nl_models = "-Dnetlogo.docs.dir=" + os.path.join(nl_path,"models")
        if(platform.system() == "Darwin"):
            nl_docs = "-Dnetlogo.docs.dir=" + os.path.join(nl_path,"../docs")
            nl_extensions = "-Dnetlogo.extensions.dir=" + os.path.join(nl_path,"../extensions")
            nl_models = "-Dnetlogo.docs.dir=" + os.path.join(nl_path,"../models")
        nl_path = os.path.join(os.path.abspath(nl_path),"*")
        server_path = os.path.join(os.path.abspath(self.SERVER_PATH),"*")
        classpath = nl_path + os.pathsep + server_path 
        xmx = psutil.virtual_memory().available / 1024 / 1024 / 1024
        xms = "-Xms" + str(int(math.floor(xmx - 2))) + "G"
        xmx = "-Xmx" + str(int(math.floor(xmx))) + "G"
        levelspace = "-Dorg.nlogo.preferHeadless=true"
        subprocess.call(["java",levelspace,xmx,"-XX:-UseGCOverheadLimit","-cp", classpath,nl_docs,nl_extensions,nl_models,__server_name])
                
    '''Starts JavaGateway server'''
    def startServer(self, netlogo_home):
        #Fire up the NetLogo Controller server through python
        thread = threading.Thread(target=self.__runServer, args=[netlogo_home])
        thread.start()
        time.sleep(3)
        
    '''Send shutdown signal to the JavaGateway server. No further communication is possible unless server is restarted'''
    def shutdownServer(self):
         if(self.__gw != None):    
            try:
                logging.disable(logging.CRITICAL)
                __bridge = self.__gw.entry_point
                __bridge.shutdownServer()
                self.__gw.close(keep_callback_server=False, close_callback_server_connections=True)
                self.__gw = None
            except Exception as e:
                pass