import ply, sys, os, seawolf_parser

def main():
    # print ('Number of arguments:', len(sys.argv), 'arguments.')
    # print ('Argument List:', str(sys.argv))
    if (len(sys.argv)) != 2:
        print("Invalid Input \nUsage: trueSeawolf.py [input file]")
        return
    else:
        if os.path.isfile(str(sys.argv[1])):
            inputFile = str(sys.argv[1])
            input = open(inputFile, "r")
            s = input.read()
            ast = seawolf_parser.parser.parse(s)
            if (not (ast is (None))):
                ast.execute();
            input.close()
        else:
            print("Input file " + str(sys.argv[1]) + " does not exist!")
            return
#    while True:
#        try:
#            s = input('$')  # Use raw_input on Python 2
#        except EOFError:
#            break
#        ast = seawolf_parser.parser.parse(s)
#        if(not(ast is (None))):
#            ast.execute();
main()
