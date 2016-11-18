import ply, sys, os, seawolf_parser

def main():
    #print ('Number of arguments:', len(sys.argv), 'arguments.')
    #print ('Argument List:', str(sys.argv))
    while True:
        try:
            s = input('$')  # Use raw_input on Python 2
        except EOFError:
            break
        ast = seawolf_parser.parser.parse(s)
        if(not(ast is (None))):
            ast.execute();
main()
