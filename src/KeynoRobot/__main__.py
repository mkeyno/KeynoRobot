#!/usr/bin/python3
from __future__ import absolute_import, division, print_function
# from __future__ import unicode_literalsim 
import os
from  cli import *
import exceptions
import sys,os
#import packages.winapp as winapp
from  packages.main import mainApp
import packages.cam as cam
 
def do_action(com):
    
    if   com=="win":        
        pass #winapp.main()
    elif com=="web":
        print("web application loading");	mainApp()
    elif com=="cam":
        cam.main()    
    else: print("web started");	            mainApp()

parser = argparse.ArgumentParser(prog="KeynoRobot main command")	
parser.add_argument("--version",action="version")
parser.add_argument("--command",help="name of commands",default="web")

def dispatch():
    #print("dispatch")
    # registered_commands = _registered_commands()
    
    #choices=registered_commands.keys(),)
    # parser.add_argument("args",help=argparse.SUPPRESS,nargs=argparse.REMAINDER,)
    args = parser.parse_args()
    # main = registered_commands[args.command].load()    
    print("you enter:",args.command)
    do_action(args.command.lower())#main(args.args)
    #return True
    
def main():
    
    print("Please Enter Application Mode (Web,Windows,Async)")
    dispatch()
    #try:
        #return dispatch(sys.argv[1:]) #user_args = sys.argv[1:] # get everything after the script name
    #except (exceptions.KeynoException, Exception) as exc:
        #return '{}: {}'.format(exc.__class__.__name__, exc.args[0])
    print("END")


if __name__ == "__main__":
     main() 








# exception NameError Raised when a local or global name is not found
# exception TypeError Raised when an operation or function is applied to an object of inappropriate type
# exception ValueError Raised when an operation or function receives an argument that has the right type but an inappropriate value














