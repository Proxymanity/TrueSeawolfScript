import ply
import seawolf_parser
while(True):
    try:
        s= input('$ ')
    except EOFError:
        break
    if not s:
        continue
    result = seawolf_parser.parser.parse(s)