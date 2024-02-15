#
# U n i t T e s t / t e s t _ L o c U t i l . p y
#

from unittest import TestCase

import math
from random import randint

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
        list_ = [randint(0, MAX_NUM - 1) for _ in range(N)]
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
            cat = randint(0, N_CATEGORY - 1)
            data = randint(0, 99)

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

            n0 = randint(minListSize, maxListSize - 1)
            n1 = randint(minListSize, maxListSize - 1)
            nMin = min(n0, n1)

            LocUtil.SetSeed(seed)
            list0 = [randint(0, maxInt) for _ in range(n0)]

            LocUtil.SetSeed(seed)
            list1 = [randint(0, maxInt) for _ in range(n1)]

            self.assertEqual(list0[:nMin], list1[:nMin])

    def test_Partition(self):
        num = [15, 35, 95, 89, 23, 99, 59, 43, 14, 66, 50, 58]

        isPrime = lambda n: not any((n % i) == 0 for i in range(2, n))
        prime, notPrime = LocUtil.Partition(isPrime, num)

        self.assertEqual(prime, [89, 23, 59, 43])
        self.assertEqual(notPrime, [15, 35, 95, 99, 14, 66, 50, 58])

    def test_UnZip(self):
        case0 = [('a',5), ('b', 3), ('c', 7)]
        alpha,num = LocUtil.UnZip(case0)
        self.assertEqual(['a','b','c'], alpha)
        self.assertEqual([5,3,7], num)

        case1 = [('a',5,-1), ('b', 3,-2), ('c', 7,-3)]
        alpha,num,neg = LocUtil.UnZip(case1)
        self.assertEqual(['a','b','c'], alpha)
        self.assertEqual([5,3,7], num)
        self.assertEqual([-1,-2,-3], neg)

        case2 = [1,2,3,4,5,6,7,8,9,10]
        num = LocUtil.UnZip(case2)
        self.assertEqual(case2, num)

    def test_Index(self):
        list0 = [('a',5), ('b', 3), ('c', 7), ('d', 3)]
        resultA = LocUtil.Index(list0, ('b',3))
        self.assertEqual(1, resultA)

    def test_ListMinus(self):
        list0 = [0,1,2,3,4,5,6,7,8,9,10]
        list1 = [0,1,2,3,math.pi,5,7]

        result = LocUtil.ListMinus(list0,list1)
        ans = [4,6,8,9,10]

        self.assertEqual(ans, result)

    def test_FlattenA(self):
        # test 0
        list0 = [[0,1], [2,3], [3,4]]
        ans0 = [0, 1, 2, 3, 3, 4]

        result = LocUtil.Flatten(list0)
        self.assertEqual(ans0, result)

        # test 1
        list1 = [[[0,1], [2,3]], [[4,3], [3,4]]]
        ans1 = [[0,1], [2,3], [4,3], [3,4]]

        result = LocUtil.Flatten(list1)
        self.assertEqual(ans1, result)

        # test 2
        list2 = [[[0,1], [2,3]], [[4,3], [3,4]]]
        ans2 = [0,1,2,3,4,3,3,4]

        result = LocUtil.Flatten(list2, 0)
        self.assertEqual(ans2, result)

        # test 3
        list3 = [[[[[7,6], 5], 4], 3], 1]
        ans3 = [[[7, 6], 5], 4, 3, 1]

        result = LocUtil.Flatten(list3, 2)
        self.assertEqual(ans3, result)

    def test_FlattenB(self):
        # test 0
        list0 = [(0,1), (2,3), (2,1)]
        ans0 = [0, 1, 2, 3, 2, 1]

        result = LocUtil.Flatten(list0)
        self.assertEqual(ans0, result)

        # test 1
        list1 = [{(0,1), (2,3)}, {(3,1), (5,4)}, {(0,1), (6,5)}]
        ans1 = [(0,1),(2,3),(3,1),(5,4),(0,1),(6,5)]

        result = LocUtil.Flatten(list1)
        self.assertEqual(ans1, result)

    def test_BinInA(self):
        # constants
        listSize = 200
        maxNum = 500 - 1

        seed = LocUtil.SetSeed()

        # set up ground truth
        inList = sorted([randint(0,maxNum) for _ in range(listSize)])
        inIndex = [n in inList for n in range(maxNum + 1)]

        # do test
        for i in range(maxNum + 1):
            if LocUtil.BinIn(inList, i) != inIndex[i]:
                self.fail(f'seed = {seed}')

    def test_BinInB(self):
        # constants
        listSize = 10
        maxNum = 4

        seed = LocUtil.SetSeed()

        # set up ground truth
        inList = sorted([(randint(0,maxNum), randint(0,maxNum)) for _ in range(listSize)])
        inIndex = [[(i1,i0) in inList for i0 in range(maxNum + 1)] for i1 in range(maxNum + 1)]

        # do test
        for i0 in range(maxNum + 1):
            for i1 in range(maxNum + 1):
                if LocUtil.BinIn(inList, (i0,i1)) != inIndex[i0][i1]:
                    self.fail(f'seed = {seed}')