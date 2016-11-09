import ply, sys, os
import seawolf_parser
def main():
    #print ('Number of arguments:', len(sys.argv), 'arguments.')
    #print ('Argument List:', str(sys.argv))
    while True:
        try:
            s = input('$')  # Use raw_input on Python 2
        except EOFError:
            break
        seawolf_parser.parser.parse(s)

main()