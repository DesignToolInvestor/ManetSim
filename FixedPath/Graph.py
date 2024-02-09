#
# G r a p h . p y
#

# This library contains functions for manipulating graphs, which are just a collection of links.

def ReadGraph(fileName):
    with open(fileName, 'r') as file:
        first,*rest = file.readlines()

    nNode = int(first)
    link = [eval(line) for line in rest]

    return (nNode,link)