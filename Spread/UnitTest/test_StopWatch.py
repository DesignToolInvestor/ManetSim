#
# t e s t _ S t o p W a t c h . p y
#

from unittest import TestCase

from statistics import median

from StopWatch import StopWatch


class TestStopWatch(TestCase):
    def test_start(self):
        self.fail()

    def test_stop(self):
        self.fail()

    def test_seconds(self):
        self.fail()

    def test_delta(self):
        self.fail()

    def test_reset(self):
        self.fail()


    # It turns out that method call overhead is greater than the reoluiton of the clock
    def test_resolution(self):
        timer = StopWatch(running=True)

        time0 = timer.Seconds()
        time1 = timer.Seconds()

        res = time1 - time0
        self.assertTrue(res <= 1e-6)
