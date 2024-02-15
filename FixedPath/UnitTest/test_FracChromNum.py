#
# t e s t _ F r a c C h r o m N u m . p y
#

from unittest import TestCase

from FracChromNum import FracChromNum
from LocMath import RealToFrac

class Test(TestCase):
    def test_GradChromNum(self):
        subSet = [[0], [1], [2], [3], [4], [0,2], [0,3], [1,3], [2,4]]
        nSubSet = len(subSet)

        result = FracChromNum(5, subSet)
        
        for i in range(nSubSet):
            print(f'{subSet[i]}:  {result[i]}')
        print()

        print(f'Node 0:  {result[0] + result[5] + result[6]}')
        print(f'Node 1:  {result[1] + result[7]}')
        print(f'Node 2:  {result[2] + result[5] + result[8]}')
        print(f'Node 3:  {result[3] + result[6] + result[7]}')
        print(f'Node 4:  {result[4] + result[8]}')

        chormNum = RealToFrac(sum(result))
        print(f'Chrom. Num. = {chormNum.numerator}/{chormNum.denominator}')