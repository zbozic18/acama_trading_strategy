import openpyxl


# This is a data class holding all the information of the stock
# The information is used by the trading logic in ClemTrader
class Stock:
    def __init__(self, stock, ticker, market_cap, pe, dividend, beta):
        self.stock = stock
        self.ticker = ticker
        self.market_cap = market_cap
        self.pe = pe
        self.dividend = dividend
        self.beta = beta


# ClemTrader class holds le logic for Clem's trading strategy.
# The variables that define the class are the filters.
class ClemTrader:
    def __init__(self, stocks):
        self.stocks = stocks
        self.market_cap_min = 30000000000
        self.pe_min = 17
        self.dividend_min = 0.023
        self.beta_min = 0.2
        self.beta_max = 1.1

    # This function uses self.check_boundaries func to perform the filter.
    def filter_stocks(self):
        selection = []
        for stock in self.stocks:
            if self.check_boundaries(stock):
                selection.append(stock)
                print(stock.__dict__)
        return selection

    # This function checks a Stock's attribute based on the strategy's filters.
    # If the function returns True, then its a buy.
    def check_boundaries(self, stock):
        if stock.market_cap > self.market_cap_min:
            if stock.pe > self.pe_min:
                if stock.dividend > self.dividend_min:
                    if stock.beta > self.beta_min:
                        if stock.beta < self.beta_max:
                            return True
        return False


# This function is used to read the database of stocks in the excel file.
# The function returns a list of Stocks.
def make_stocks():
    ps = openpyxl.load_workbook('asset_data/stock_selection_acama.xlsx')
    sheet1 = ps['Sheet1']
    print(sheet1.values)
    stocks = []
    for row in range(1, sheet1.max_row + 1):
        stock = sheet1['b' + str(row)].value
        ticker = sheet1['a' + str(row)].value
        market_cap = sheet1['c' + str(row)].value
        pe = sheet1['d' + str(row)].value
        dividend = sheet1['i' + str(row)].value
        beta = sheet1['g' + str(row)].value
        stock = Stock(
            stock=stock,
            ticker=ticker,
            market_cap=market_cap,
            pe=pe,
            dividend=dividend,
            beta=beta
        )
        stocks.append(stock)

    return stocks
