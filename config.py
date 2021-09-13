'''
Author: Arsalan Azmi
Description: Config for the Equal Weight Index Fund engine.
Package: equal-weight-index-fund
Python Version: 3.9
Version: 1
Year: 2021
'''
CSV_TICKERS_FILE = 'sp_500_stocks.csv'
CSV_TICKERS_FILE_COLUMN = 'Ticker'

IEX_CLOUD_API_BASE_URL = 'https://sandbox.iexapis.com/stable'
IEX_CLOUD_API_CHUNK_SIZE = 100
IEX_CLOUD_API_TOKEN = '<your-token>'

OUTPUT_EXCEL_FILE_NAME = 'recommended_trades.xlsx'
PORTFOLIO_VALUE = 100_000_000