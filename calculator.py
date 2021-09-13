'''
Author: Arsalan Azmi
Description: Calculator to calculate stock weights.
Package: equal-weight-index-fund
Python Version: 3.9
Version: 1
Year: 2021
'''
# === IMPORTS ===
import functools as _functools
import math as _math


# === CLASS DEFINITIONS ===
class EqualWeightIndexFundCalculator:
    '''
    Class for the Equal Weight calculator.
    '''
    def __init__(self, numStocksInPortfolio, portfolioValue):
        '''
        Parameters
        ----------
        numStocksInPortfolio : str
            Number of stocks in the portfolio.
        portfolioValue : float
            Total value of the portfolio.
        '''
        self.__spendPerShare = portfolioValue / numStocksInPortfolio

    # Public API
    @_functools.cache
    def calcSharesToBuy(self, price):
        spendPerShare = self.__spendPerShare
        # Get upto 4 decimal places of fractional shares.
        return _math.floor((spendPerShare / price) * 10_000) / 10_000