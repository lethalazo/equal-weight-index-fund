'''
Author: Arsalan Azmi
Description: Runs the Equal Weight Index Fund engine.
Package: equal-weight-index-fund
Python Version: 3.9
Version: 1
Year: 2021
'''
# === IMPORTS ===
from config import CSV_TICKERS_FILE, CSV_TICKERS_FILE_COLUMN, OUTPUT_EXCEL_FILE_NAME, PORTFOLIO_VALUE
import engine as _engine
import pandas as _pd

# === CLASS DEFINITIONS ===
class Main:
    '''
    Main runner class.
    '''
    def __init__(self):
        symbols = self.__parseSymbolsFromCsv(CSV_TICKERS_FILE, CSV_TICKERS_FILE_COLUMN)
        self.__engine = _engine.EqualWeightIndexFundEngine(symbols)

    # Public API
    def run(self):
        engine = self.__engine
        engine.calculateWeights(PORTFOLIO_VALUE)
        engine.saveTradesToExcel(OUTPUT_EXCEL_FILE_NAME)
        
    # Private API
    def __parseSymbolsFromCsv(self, fileName, column):
        '''
        Parse symbols from provided CSV file and column name.

        Parameters
        ----------
        fileName : str
            CSV file name to read.
        column : str
            Column name containing ticker data.
        '''
        return _pd.read_csv(fileName)[column].values.tolist()

# Runner
runner = Main()
runner.run()