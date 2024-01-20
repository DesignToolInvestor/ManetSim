#
# U n i t T e s t / t e s t _ L o c U t i l . p y
#

from unittest import TestCase

import random

import LocUtil


class Test(TestCase):
    def test_unique(self):
        def MakeMask(list_, maxNum):
            result = [False for _ in range(maxNum)]
            for i in list_:
                result[i] = True
            return result

        # define constants
        MAX_NUM = 100
        N = 150

        seed = LocUtil.SetSeed()

        # generate list with repeats
        list_ = [random.randint(0, MAX_NUM - 1) for _ in range(N)]
        uniqueList = LocUtil.Unique(list_)
        
        # compute ground truth
        if MakeMask(uniqueList, MAX_NUM) != MakeMask(list_, MAX_NUM):
            print(f'Seed = {seed}')
            self.fail()

    def test_group(self):
        # define constants
        N_CATEGORY = 15
        N_ELEM = 20

        # pick seed
        seed = LocUtil.SetSeed()

        # build test case
        catLet = [chr(k + ord('A')) for k in range(N_CATEGORY)]

        list_ = []
        mask = [[] for i in range(N_CATEGORY)]
        for i in range(N_ELEM):
            cat = random.randint(0, N_CATEGORY - 1)
            data = random.randint(0,99)

            mask[cat].append(data)
            list_.append([catLet[cat], data])

        # test LocUtil.Group
        result = LocUtil.Group(lambda elem: elem[0], list_)

        # check result
        temp = [[[catLet[cat], d] for d in mask[cat]] for cat in range(N_CATEGORY)]
        answer = LocUtil.Select(lambda g: g != [], temp)
        self.assertEqual(result, answer)