from bond_data_xml import get_interest_rates
import datetime
from bond_data_csv import get_10_y_bond_history
from tools import fix_date, change_year, get_dif_years
from bond_data_xml import get_interest_rates


# This class creates a bond with the necessary data to be calculated the sell or buy in the strategy
# Its used next in the make_bonds() function
class Bond:
    def __init__(self, coupon, fv, duration, issue_date=None):
        self.coupon_rate = float(coupon)
        self.face_value = float(fv)
        self.interest_rate = None
        self.set_interest_rate(get_interest_rates(), issue_date)
        self.issue_date = issue_date
        self.duration = int(duration)     # The duration is measured in years
        self.maturity_date = change_year(self.issue_date, self.duration)
        self.date_of_purchase = None
        self.time_to_maturity = duration
        self.price_at_purchase = self.face_value
        self.remaining_coupon = self.get_remaining_coupon()

    def calculate_price(self, current_date=None):
        if current_date is not None:
            self.set_time_to_maturity(current_date)
        price = self.coupon_rate * ((1-(1/((1+self.interest_rate)**self.time_to_maturity)))/self.interest_rate) + \
                self.face_value/((1+self.interest_rate)**self.time_to_maturity)
        return price

    def set_date_of_purchase(self, date_of_purchase):
        self.date_of_purchase = date_of_purchase

    def set_interest_rate(self, interest_rates, date):
        try:
            self.interest_rate = float(interest_rates[date])
        except Exception as e:
            print(e)

    def set_time_to_maturity(self, current_date):
        self.time_to_maturity = get_dif_years(current_date, self.maturity_date)

    def get_remaining_coupon(self):
        r_coupon = self.time_to_maturity * (self.face_value * self.coupon_rate)
        return r_coupon


def make_bonds():
    i_rates = get_interest_rates()
    first_month_i_rates = []
    made_bonds = []
    recent = 0
    coupons = get_10_y_bond_history()

    # The bellow for loop builds the first_month_i_rates where the first index is the first date of that month and
    # the second index is the interest rate in the beginning of that month.
    for i_date in i_rates:
        date = datetime.datetime.strptime(i_date, '%Y-%m-%d')
        month = date.month

        if recent != month:
            recent = month
            first_month_i_rates.append([i_date, i_rates[i_date]])
            firs_day = fix_date(i_date)
            made_bond = Bond(
                coupon=coupons[firs_day],
                fv=100,
                issue_date=i_date,
                duration=10
            )
            made_bond.interest_rate = (float(i_rates[i_date]) / 100)
            made_bond.calculate_price()
            made_bonds.append(made_bond)

    return made_bonds
