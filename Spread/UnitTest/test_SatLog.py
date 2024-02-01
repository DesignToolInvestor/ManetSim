#
# t e s t _ S a t L o g . p y
#

from unittest import TestCase

# system level imports
import sys

# special local imports
sys.path.append('../Data')
import SatLog

class Test(TestCase):
    def test_ReadSatLog(self):
        # constants
        groudTruth = [
            [121, 1, 2.880251038584576], [121, 2, 7.655525264991066 / 2],
            [121, 3, 8.318603919332672 / 2], [121, 4, 11.941373600550257 / 3],
            [121, 5, 16.93117291771693 / 3], [121, 6, 17.752053853845098 / 3],
            [121, 7, 21.90722164039041 / 3], [121, 8, 28.799961926652422 / 3],
            [121, 9, 33.24482411698429 / 4], [121, 10, 35.92894729392401 / 4],
            [121, 11, 37.43572991352445 / 4], [121, 12, 39.3959130065323 / 4]]

        fileName = "SatLogA1.log"

        eps = sys.float_info.epsilon

        # do test
        entL = SatLog.ReadSatLog(fileName)
        nEnt = len(entL)

        for k in range(nEnt):
            self.assertEqual(entL[k].nNode, groudTruth[k][0])
            self.assertEqual(entL[k].nStream, groudTruth[k][1])
            self.assertTrue(abs(entL[k].AgFlow() - groudTruth[k][2]) < 10*eps)