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

    def test_setSeed(self):
        # define constants
        numLoop = 10
        minListSize = 5
        maxListSize = 15
        maxInt = 999

        testSeed = None

        # do tests
        for k in range(numLoop):
            seed = LocUtil.SetSeed(testSeed)

            n0 = random.randint(minListSize, maxListSize - 1)
            n1 = random.randint(minListSize, maxListSize - 1)
            nMin = min(n0,n1)

            LocUtil.SetSeed(seed)
            list0 = [random.randint(0,maxInt) for _ in range(n0)]

            LocUtil.SetSeed(seed)
            list1 = [random.randint(0,maxInt) for _ in range(n1)]

            self.assertEqual(list0[:nMin], list1[:nMin])

    def test_Partition(self):
        num = [15, 35, 95, 89, 23, 99, 59, 43, 14, 66, 50, 58]

        isPrime = lambda n: not any((n % i) == 0 for i in range(2,n))
        prime,notPrime = LocUtil.Partition(isPrime, num)

        self.assertEqual(prime, [89, 23, 59, 43])
        self.assertEqual(notPrime, [15, 35, 95, 99, 14, 66, 50, 58])