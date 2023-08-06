# Any changes to the distributions library should be reinstalled with
#  pip install --upgrade .

# For running unit tests, use
# /usr/bin/python -m unittest test

import unittest

from BBKnapsack import BBKnapsack
from HSKnapsack import HSKnapsack

capacity = 50
weights = [31, 10, 20, 19, 4, 3, 6]
profits = [70, 20, 39, 37, 7, 5, 10]
max_profit = 107
min_profit = 98

class TestHSKnapsackClass(unittest.TestCase):
    def setUp(self):
    	pass

    def test_maximize(self):
        knapsack = HSKnapsack(capacity, profits, weights)
        cal_profit, cal_solution = knapsack.maximize()
        self.assertEqual(cal_profit, max_profit, 'calculated maximum profit not as expected')
        profit = 0
        for i in range(knapsack.nb_items):
            if cal_solution[i] == 1:
                profit += knapsack.profits[i]
        self.assertEqual(profit, max_profit, 'calculated profit from solution not as expected')

    def test_minimize(self):
        knapsack = HSKnapsack(capacity, profits, weights)
        cal_profit, cal_solution = knapsack.minimize()
        self.assertEqual(cal_profit, min_profit, 'calculated maximum profit not as expected')
        profit = 0
        for i in range(knapsack.nb_items):
            if cal_solution[i] == 1:
                profit += knapsack.profits[i]
        self.assertEqual(profit, min_profit, 'calculated profit from solution not as expected')

class TestBBKnapsackClass(unittest.TestCase):
    def setUp(self):
    	pass

    def test_maximize(self):
        knapsack = BBKnapsack(capacity, profits, weights)
        cal_profit, cal_solution = knapsack.maximize()
        self.assertEqual(cal_profit, max_profit, 'calculated maximum profit not as expected')
        profit = 0
        for i in range(knapsack.nb_items):
            if cal_solution[i] == 1:
                profit += knapsack.profits[i]
        self.assertEqual(profit, max_profit, 'calculated profit from solution not as expected')

    def test_minimize(self):
        knapsack = BBKnapsack(capacity, profits, weights)
        cal_profit, cal_solution = knapsack.minimize()
        self.assertEqual(cal_profit, min_profit, 'calculated maximum profit not as expected')
        profit = 0
        for i in range(knapsack.nb_items):
            if cal_solution[i] == 1:
                profit += knapsack.profits[i]
        self.assertEqual(profit, min_profit, 'calculated profit from solution not as expected')


if __name__ == '__main__':
    unittest.main()
