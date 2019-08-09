

import tkinter,sys
import subprocess
import tkinter.messagebox as button

window = tkinter.Tk()

def helloCallBack():
    button.showinfo( "Hello Python title", "Hello World")
    


def main():
    print("win application loading")
    hello_button = tkinter.Button(window, text ="Hello", command = helloCallBack)
    coord = 10, 50, 240, 210
    canvas=tkinter.Canvas(window,bg="blue", height=250, width=300)
    arc_canvas=canvas.create_arc(coord, start=0, extent=150, fill="red")
    
    canvas.pack()
    hello_button.pack()
    window.mainloop()

if __name__ == "__main__":
    sys.exit(main())
""""
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('integers',      metavar='N', type=int, nargs='+',                           help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',const=sum,  default=max,    help='sum the integers (default: find the max)')
parser.add_argument("--query","-q",  metavar = "LOCATION", type = str, nargs = 1,default = "keyn", help = "Location") 
parser.add_argument("--days" ,"-d",  metavar = "DAYS"    ,type = str, nargs = 1, default = [1],  help = "Number of days")
args = parser.parse_args()

# python  winapp.py 1 2 3 4 5 -q q -d sun
print(dir(args)[-4:]) # ['accumulate', 'days', 'integers', 'query']
print("accumulate=",args.accumulate) # <built-in function max>
print("days",args.days) #[sun]
print("query",args.query) #[q]
print("integers",args.integers) # [1, 2, 3, 4, 5]

print("sum=",args.accumulate(args.integers))



ArgumentParser.add_argument(name or flags...[, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest]
usage: winapp.py [-h] [--sum] N [N ...]
Process some integers.
positional arguments:
    N           an integer for the accumulator
optional arguments:
    -h, --help  show this help message and exit
    --sum       sum the integers (default: find the max)
    
     name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action - The basic type of action to be taken when this argument is encountered at the command line.
    nargs - The number of command-line arguments that should be consumed.
    const - A constant value required by some action and nargs selections.
    default - The value produced if the argument is absent from the command line.
    type - The type to which the command-line argument should be converted.
    choices - A container of the allowable values for the argument.
    required - Whether or not the command-line option may be omitted (optionals only).
    help - A brief description of what the argument does.
    metavar - A name for the argument in usage messages.
    dest -  The name of  the attribute to be added to the object returned by parse_args().
   
"""