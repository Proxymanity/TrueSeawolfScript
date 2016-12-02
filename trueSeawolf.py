import ply, sys, os
import seawolf_parser
#Calvin Kwok ID: 109209504
def main():
    #print ('Number of arguments:', len(sys.argv), 'arguments.')
    #print ('Argument List:', str(sys.argv))
    if(len(sys.argv)) != 2:
       print("Invalid Input \nUsage: trueSeawolf.py [input file]")
       return
    else:
        if os.path.isfile(str(sys.argv[1])):
            inputFile = str(sys.argv[1])
            input = open(inputFile, "r")
            for line in input:
                try:
                    s = line
                except EOFError:
                    break
                if not s:
                    continue
                seawolf_parser.parser.parse(s)
            input.close()
        else:
            print("Input file " + str(sys.argv[1]) +" does not exist!")
            return

main()