from __future__ import absolute_import, division, print_function
# from __future__ import unicode_literalsim 
import os
from  cli import *
import exceptions
import sys,os
import packages.winapp as winapp
import packages.cam as cam
#import requests #facto standard for making HTTP requests in Python

# from twine(root folder) import exceptions(.py)
#                                exceptions.TwineException(  class TwineException(Exception): )

#    KeynoRobot\cli.py
#print(__version__)
def do_action(com):
    
    if   com=="win":        
        winapp.main()
    elif com=="web":
        print("web application loading")
    elif com=="cam":
        cam.main()    
    else:
        print("not correct command")

parser = argparse.ArgumentParser(prog="KeynoRobot main command")	
parser.add_argument("--version",action="version",
                    #version="%(prog)s version {} ({})".format(KeynoRobot.__version__,dep_versions(),),
                    )
parser.add_argument("command",help="name of commands")

def dispatch():
    #print("dispatch")
    # registered_commands = _registered_commands()
    
    #choices=registered_commands.keys(),)
    # parser.add_argument("args",help=argparse.SUPPRESS,nargs=argparse.REMAINDER,)
    args = parser.parse_args()
    # main = registered_commands[args.command].load()    
    print("you enter:",args.command,sys.argv[1:])
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
    sys.exit(main())#it will exit giving the system the return code that is the result of main()








# exception NameError Raised when a local or global name is not found
# exception TypeError Raised when an operation or function is applied to an object of inappropriate type
# exception ValueError Raised when an operation or function receives an argument that has the right type but an inappropriate value














