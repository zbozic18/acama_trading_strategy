import pandas as pd
from dataclasses import dataclass
from asset_data_management.yahoo_finance_data import get_tickers
from asset_data_management.tools import find_date


@dataclass
class Period:
    start_date: str
    end_date: str


@dataclass
class Trade:
    ticker: str
    entry_price: float
    current_price: float


# This class is a trade simulator based on historical data
# As input variables it requires:
#      - period variable which is a Period dataclass object
#      - ticker variable which is a Ticker dataclass object
class HistoryTrader:
    def __init__(self, period, tickers):
        self.period = period
        self.tickers = tickers

    # This function returns top 10 stocks in the selection
    def get_top_performers(self):
        stocks = {}
        top_stocks = {}
        for ticker in self.tickers:
            ticker = ticker[0]
            dividend = self.check_for_dividend(ticker)
            if dividend is not None:
                closing_price_entry = get_closing_price(self.period.start_date, ticker, dividend)
                closing_price_current = get_closing_price(self.period.end_date, ticker, dividend)
                if closing_price_current is not None and closing_price_entry is not None:
                    net_gain = closing_price_current - closing_price_entry
                    stocks[ticker] = net_gain / closing_price_entry

        # Bellow three lines sort the stocks dict base on returns, highest to lowest
        stocks_list = sorted(stocks.items(), key=lambda x: x[1], reverse=True)
        stocks_sorted = dict(stocks_list)

        # Creates a dictionary with top 10 stocks
        for stock in stocks_sorted:
            top_stocks[stock] = stocks_sorted[stock]
            if len(top_stocks) == 31:
                break

        return top_stocks

    @staticmethod
    def check_for_dividend(tick):
        df_stock = pd.read_csv(f'asset_data_management/asset_data/ticker_data/{tick}')
        dividend_indexes = []
        try:
            dividends = df_stock['Dividends'].to_list()
            for dividend in dividends:
                if dividend > 0:
                    dividend_indexes.append(dividends.index(dividend))
            if len(dividend_indexes) > 0:
                return dividend_indexes[len(dividend_indexes)-1]
        except Exception as e:
            print(e, tick)
            return None
        return None


# Finds the closing price for the set date and submitted ticker
# If the ticker existed on that date, the func will return the closing price, otherwise it will be None
def get_closing_price(date, ticker, dividend_index):
    df_stock = pd.read_csv(f'asset_data_management/asset_data/ticker_data/{ticker}')
    index = find_date(df_stock, date)
    if index is not None:
        if index <= dividend_index:
            closing_price = df_stock.loc[find_date(df_stock, date), 'Close']
            return closing_price


# The code bellow creates excel docs for backtracking of all the selected periods.
# It gets the top performers for the periods which have to be manually backtracked then based on the strategy.
# If we want to fully automatise, we need to use ClemTrader from clem_stock-trading
crisis_period = Period('2018-08-01', '2019-01-31')
recovery_period = Period('2019-02-01', '2019-07-31')
volatile_period = Period('2015-12-01', '2016-05-31')
pre_covid_period = Period('2017-04-03', '2017-10-02')
stable_period = Period('2012-06-01', '2012-11-30')

periods = [crisis_period, recovery_period, volatile_period, pre_covid_period, stable_period]
all_tickers = get_tickers('asset_data/s&p_tickers.csv')


for per in periods:
    print(per)
    history_trader = HistoryTrader(period=per, tickers=all_tickers)
    top_performers = history_trader.get_top_performers()
    performer_list = []
    for i in top_performers:
        performer_list.append([i, top_performers[i]])
    df = pd.DataFrame(performer_list, columns=['Ticker', 'Gain'])
    df.to_excel(f'results/{per.start_date}.xlsx')
