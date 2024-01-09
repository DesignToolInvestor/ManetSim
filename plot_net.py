#
# p l o t _ n e t . p y
#

# TODO:  Create a description of the arguments that can bu used when invoking this program

# system imports
import argparse
import scanf

# local imports
import Net
import Visual

def ParseArgs():
    parser = argparse.ArgumentParser(
        prog='plot_net',
        description='This program will graph a network.'
    )

    parser.add_argument('fileName', type=str)
    parser.add_argument('-size', type=str, default='(3.5,3.5)')
    parser.add_argument('-ln', type=bool, default=False)
    parser.add_argument('-ll', type=bool, default=False)

    args = parser.parse_args()

    size = scanf.scanf("(%f,%f)", args.size)

    return [args.fileName, size, args.ln, args.ll]


if __name__ == '__main__':
    fileName,size,labelNode,labelLink = ParseArgs()

    net,direct = Net.ReadNet(fileName)

    if direct:
        Visual.GraphDirNet(net)
    else:
        Visual.GraphBiNet(net)