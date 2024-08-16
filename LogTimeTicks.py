#
# L o g T i m e T i c k s . p y
#

from math import log


def FindStep(val, stepL):
  logStep = [log(v) for v in stepL]
  logVal = log(val)
  
  index = 0
  minDiff = abs(logVal - logStep[0])

  for i in range(1, len(logStep)):
    diff = abs(logVal - logStep[i])
    if diff < minDiff:
      index = i
      minDiff = diff

  return index
  

# TODO:  This should have a hierarchy of magic number for when the skip is larger
def LogTimeTicks(valRange, goalNumTick):
  # set up time units
  unitName = ['us', 'ms', 's', 'mn', 'hr', 'dy', 'wk', 'mo', 'yr', 'dec']
  nUnit = len(unitName)
  mult = [1e3, 1e3, 60, 60, 24, 7, 365.25 / 12, 12, 10]

  unitVal = [1e-6]
  for m in mult:
    unitVal.append(m * unitVal[len(unitVal) - 1])

  majicNum = [
    [1,2,3,5,10, 20,30,50, 100,200,300,500],
    [1,2,3,5,10, 20,30,50, 100,200,300,500],
    [1,2,4,8,15,30],
    [1,2,4,8,15,30],
    [1,2,3,6,12],
    [1,2,4],
    [1,2],
    [1,2,4,6],
    [1,2,3,5],
    [1,2,3,5, 10,20,30,50]
  ]

  stepVal = []
  stepName = []
  for i in range(nUnit):
    stepVal.extend([num * unitVal[i] for num in majicNum[i]])
    stepName.extend([f'{num} {unitName[i]}' for num in majicNum[i]])

  # figure tick values
  low,high = valRange

  lowStep = FindStep(low, stepVal)
  highStep = FindStep(high, stepVal)
  nStep = highStep - lowStep

  # This places the tick approximately uniformly
  # skip = max(1, round(nStep / (goalNumTick - 1)))
  # tickVal = [stepVal[i] for i in range(lowStep, highStep + 1, skip)]
  # tickName = [stepName[i] for i in range(lowStep, highStep + 1, skip)]

  # This place the ticks at each end
  numTick = min(nStep, goalNumTick)
  stepNum = [round(k * (nStep / (numTick - 1))) for k in range(numTick)]

  tickVal = [stepVal[i] for i in stepNum]
  tickName = [stepName[i] for i in stepNum]

  return (tickVal, tickName)