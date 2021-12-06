from bonds import make_bonds
from tools import fix_date, save_trade_to_csv
from bond_data_xml import get_interest_rates


bonds_db = make_bonds()
intrests = get_interest_rates()
starting_date = '2015-12-01'


# The bond strategy is based on the Acama trading strategy manual
# The bellow strategy uses the Bond class for its operations
def bond_strategy(start_date, bondsdb):
    bond = None
    intrest = None
    for i in bondsdb:
        if fix_date(i.issue_date) == fix_date(start_date):
            bond = i

    exit_price = bond.remaining_coupon + bond.price_at_purchase
    for intr in intrests:
        bond.set_interest_rate(intrests, intr)
        bond_price = bond.calculate_price(fix_date(intr))
        if bond_price >= exit_price:
            save_trade_to_csv(bond)
            return intr
        intrest = intr

    return intrest


active = True   # This variable decides weather the trader is active or not
while active:
    starting_date = bond_strategy(starting_date, bonds_db)
    if starting_date == '2021-11-30':
        active = False
