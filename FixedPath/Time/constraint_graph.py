#
# c o n s t r a i n t _ g r a p h . p y
#

from math import exp, log
import matplotlib.pyplot as plot
from scipy import stats

from LocUtil import Grid1, Select, UnZip

######################################
def GraphNSubSet(nHop,nSubSet):
    fig, ax = plot.subplots()
    plot.semilogy(nHop,nSubSet, 'ro', markersize=5)

    # fit to data
    logNSubSet = [log(n) for n in nSubSet]
    fit = stats.linregress(nHop, logNSubSet)

    xL = Grid1(0,40, 30)
    # yL = [exp(fit[0]*x + fit[1]) for x in xL]
    yL = [2**(1/3) * (3**(1/3))**x for x in xL]
    plot.plot(xL,yL, 'b', linewidth=2)

    plot.text(22,100e3, "$\\sqrt[3]{2}\\cdot (\\sqrt[3]{3})^n$")

    # show target zone
    plot.plot([0,40], [3e6,3e6], 'g--')
    plot.plot([0,40], [300e3,300e3], 'g--')

    # set axis
    tickVal = [1, 10, 100, 1e3, 10e3, 100e3, 1e6]
    ticklabel = ['1', '10', '100', '1K', '10K', '100K', '1M']
    plot.yticks(ticks=tickVal, labels=ticklabel)

    # annotate
    plot.xlabel("Num. of Hops")
    plot.ylabel("Num. Independent Subsets")
    plot.title(f'Rho = {rho}')

    # save figure
    plot.savefig('constraint_subset.png')
    # plot.show()
    plot.close()


######################################
def GraphSetUp(nHop,setUpTime):
    fig, ax = plot.subplots()
    plot.semilogy(nHop,setUpTime, 'ro', markersize=5)

    # # fit to data
    logTime = [log(t) for t in setUpTime]
    fit = stats.linregress(nHop, logTime)

    xL = Grid1(7,40, 30)
    yL = [exp(fit[0]*x + fit[1]) for x in xL]
    plot.plot(xL,yL, 'b', linewidth=2)

    plot.text(18,100e3, '$%.2f\\mu s \cdot (%.2f)^n$'%(exp(fit[1])*1e6, exp(fit[0])))

    # show target zone
    plot.plot([7,40], [10*60,10*60], 'g--')
    plot.plot([7,40], [10,10], 'g--')

    # set axis
    tickVal = [1e-3, 1, 60, 60*60, 24*60*60, 7*24*60*60, 365*24*60*60]
    ticklabel = ['1ms', '1s', '1m', '1h', '1d', '1w', '1y']
    plot.yticks(ticks=tickVal, labels=ticklabel)

    # annotate
    plot.xlabel("Num. of Hops")
    plot.ylabel("Setup Time (old computer)")
    plot.title(f'Rho = {rho}')

    # save figure
    plot.savefig('constraint_setup.png')
    # plot.show()
    plot.close()


######################################
def GraphSolve(nHop,solveTime):
    fig, ax = plot.subplots()
    plot.semilogy(nHop,solveTime, 'ro', markersize=5)

    # fit to data
    logTime = [log(n) for n in solveTime]
    fit = stats.linregress(nHop, logTime)

    xL = Grid1(0,40, 30)
    yL = [exp(fit[0]*x + fit[1]) for x in xL]
    plot.plot(xL,yL, 'b', linewidth=2)

    plot.text(28,3, '$%.2fms \cdot (%.2f)^n$'%(exp(fit[1])*1e3, exp(fit[0])))

    # show target zone
    plot.plot([0,40], [30*60,30*60], 'g--')
    plot.plot([0,40], [30,30], 'g--')

    # set axis
    tickVal = [10e-3, 1, 10, 60, 10*60]
    ticklabel = ['10ms', '1s', '10s', '1m', '10m']
    plot.yticks(ticks=tickVal, labels=ticklabel)

    # annotate
    plot.xlabel("Num. of Hops")
    plot.ylabel("Solve Time (old computer)")
    plot.title(f'Rho = {rho}')

    # save figure
    plot.savefig('constraint_solve.png')
    # plot.show()
    plot.close()

###########################################################
if __name__ == "__main__":
    # constants
    fileName = "prune.log"
    # FileName = "slow.log"

    # read data
    with open(fileName, "r") as file:
        lineL = file.readlines()
    info = [eval(line) for line in lineL]

    netInfo,setUpInfo,solveInfo = UnZip(info)
    nHop,nSubSet,setUpTime = UnZip(setUpInfo)
    chromNum,solveTime = UnZip(solveInfo)
    _, rho, _ = netInfo[0]

    # do graphs
    GraphNSubSet(nHop,nSubSet)

    filtData = [(n,t) for (n,t) in zip(nHop,setUpTime) if (10e-6 < t) and (12 < n)]
    GraphSetUp(*UnZip(filtData))

    GraphSolve(nHop,solveTime)
