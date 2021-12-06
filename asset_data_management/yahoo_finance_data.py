import yfinance as yahooFinance
import csv


def get_fin_info(ticker):
    ticker_info = yahooFinance.Ticker(ticker)
    return ticker_info.history(period='max')


def get_stocks_movements(ticker_names):
    ticker_count = 0
    progress = (str(ticker_count / 500) * 100) + '%'
    for ticker_name in ticker_names:
        print(progress)
        df_stock = get_fin_info(ticker_name)
        df_stock.to_csv(f'asset_data/ticker_data/{ticker_name}')
        ticker_count += 1


def get_tickers(tickers_csv):
    ticker_names = []
    with open(tickers_csv, 'r') as file:
        ticker_names_csv = csv.reader(file)
        for ticker_name in ticker_names_csv:
            ticker_names.append(ticker_name)

    return ticker_names
