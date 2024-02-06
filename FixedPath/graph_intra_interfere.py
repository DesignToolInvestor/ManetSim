#
# g r a p h _ i n t r a _ i n t e r f e r e . p y
#



def Circle(cent, r, nPoint):
    x,y = cent
    theta = [k * 2*pi/nPoint for k in range(nPoint)]
    theta.append(0)
    point = [(x + r*cos(t), y + r*sin(t)) for t in theta]

    return point

if __name__ == "__main__":
    # start new graph
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    ax.set_aspect('equal')

    # plot just the node along the path
    fadeNode = 'blue'
    pathLoc = Sub(nodeLoc, path)
    x, y = UnZip(pathLoc)
    plot.plot(x, y, 'o', fillstyle='none', color=fadeNode, markersize=5, zorder=0)

    # plot links along the path
    fadeLink = 'red'
    plot.plot(x, y, '--', color=fadeLink, zorder=-1)

    # show link nodes
    pathLinkLoc = Sub(nodeLoc, pathLink)
    linkCent = [Cent(seg) for seg in pathLinkLoc]

    x, y = UnZip(linkCent)
    plot.plot(x, y, 'o', color='saddlebrown', markersize=8, zorder=1)

    # do circles for exclusion zone
    destLoc = pathLoc[1:]
    snir = 10 ** (snirDb / 20)
    exR = [ExcludeDist(Dist(*link), snir, 2) for link in pathLinkLoc]
    print(f'exR = {exR}')
    circL = [Circle(cent, r, nPointCirc) for (cent, r) in zip(destLoc, exR)]

    for circ in circL:
        plot.plot(*UnZip(circ), 'g--')

    fileName = f'Figures/shortest_{nNode}_{rhoStr}_{seed}_rings.png'
    plot.savefig(fileName, dpi=200)

    plot.show()