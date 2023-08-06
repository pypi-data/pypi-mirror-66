import sys
from giphy import get_gif

def main():
    sep = ' '
    query = sep.join(sys.argv[1:])
    get_gif.hook(query)

main()
