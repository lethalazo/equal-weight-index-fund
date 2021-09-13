'''
Author: Arsalan Azmi
Description: Engine to calculate stock weights and generate trades.
Package: equal-weight-index-fund
Python Version: 3.9
Version: 1
Year: 2021
'''
# === IMPORTS ===
import calculator as _calc
from config import IEX_CLOUD_API_BASE_URL, IEX_CLOUD_API_CHUNK_SIZE, IEX_CLOUD_API_TOKEN
import functools as _functools
import numpy as _np
import pandas as _pd
import requests as _req


# === CLASS DEFINITIONS ===
class EqualWeightIndexFundEngine:
    '''
    Class for the Equal Weight Index Fund engine.
    '''
    def __init__(self, symbols):
        '''
        Parameters
        ----------
        symbols : list of str
            List of stock tickers to get quotes and generate trades for.
        '''
        self.__columns = ['Ticker', 'Price', 'Market Capitalization', 'No. of Shares to Buy']
        self.__numStocksInPortfolio = len(symbols)
        self.__symbols = symbols
        self.__tradesDf = _pd.DataFrame(columns=self.__columns)

    # Public API
    def calculateWeights(self, portfolioValue):
        '''
        Calculate the long position for each symbol in the portfolio provided a portfolio value and update trades.

        Parameters
        ----------
        portfolioValue : float
            The total value of the portfolio to generate trades for.
        '''
        columns = self.__columns
        numStocksInPortfolio = self.__numStocksInPortfolio

        calculator = _calc.EqualWeightIndexFundCalculator(numStocksInPortfolio, portfolioValue)

        quotes = self.__getQuotesFromIEXCloud()

        prices = [quote['quote']['latestPrice'] for quote in quotes.values()]
        marketCap = [quote['quote']['marketCap'] for quote in quotes.values()]
        shareQuantity = [calculator.calcSharesToBuy(price) for price in prices]

        rows = [[symbol, prices[i], marketCap[i], shareQuantity[i]] for i, symbol in enumerate(quotes)]
        self.__tradesDf = _pd.DataFrame(rows, columns=columns)

    def saveTradesToExcel(self, fileName):
        '''
        Write the recently generated trades (recommended long positions for each symbol) to a formatted excel file.

        Parameters
        ----------
        fileName : str
            Name of the excel file to write.
        '''
        tradesDf = self.__tradesDf

        writer = _pd.ExcelWriter(fileName, engine='xlsxwriter')
        tradesDf.to_excel(writer, 'Recommended Trades', index = False)

        bgColor = '#0a0a23'
        fontColor = '#ffffff'

        stringFormat = writer.book.add_format({
            'font_color': fontColor,
            'bg_color': bgColor,
            'border': 1
        })

        dollarFormat = writer.book.add_format({
            'num_format': '$#,###.####',
            'font_color': fontColor,
            'bg_color': bgColor,
            'border': 1
        })

        integerFormat = writer.book.add_format({
            'num_format': '#.####',
            'font_color': fontColor,
            'bg_color': bgColor,
            'border': 1
        })

        columnFormats = {
            'A': ['Ticker', stringFormat],
            'B': ['Price', dollarFormat],
            'C': ['Market Capitalization', dollarFormat],
            'D': ['No. of Shares to Buy', integerFormat]
        }

        sheet = writer.sheets['Recommended Trades']

        for column in columnFormats:
            sheet.write(f'{column}1', columnFormats[column][0], columnFormats[column][1])
            
        for column in columnFormats:
            sheet.set_column(f'{column}:{column}', 20, columnFormats[column][1])

        writer.save()

    def getTradesDataframe(self):
        '''
        Returns
        -------
        pandas.DataFrame
            DataFrame containing the recently generated trades data.
        '''
        return self.__tradesDf
    
    # Private API
    @_functools.cache
    def __getQuotesFromIEXCloud(self):
        '''
        Get quotes for each symbol from the IEX cloud API.

        Returns
        -------
        dict of str -> dict
            A dict mapping symbols to quote data.
        '''
        numStocksInPortfolio = self.__numStocksInPortfolio
        symbols = self.__symbols    
        
        # Perform a batch API call with chunks of tickers.
        numChunks = numStocksInPortfolio / IEX_CLOUD_API_CHUNK_SIZE + 1
        chunks = _np.array_split(symbols, numChunks)

        data = {}
        for chunk in chunks:
            chunkStr = ','.join(chunk)
            batchAPICall = f'/stock/market/batch?symbols={chunkStr}&types=quote&token={IEX_CLOUD_API_TOKEN}'
            data.update(_req.get(IEX_CLOUD_API_BASE_URL + batchAPICall).json())

        return data