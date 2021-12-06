from finance_classes.bonds import make_bonds
from asset_data_management.tools import fix_date, save_trade_to_csv
from asset_data_management.bond_data_xml import get_interest_rates
import pandas as pd

bonds_db = make_bonds()
intrests = get_interest_rates()
starting_date = '2015-12-01'


# The bond strategy is based on the Acama trading strategy manual
# The bellow strategy uses the Bond class for its operations
def bond_strategy(start_date, bondsdb):
    bond = None
    intrest = None
    track = []
    for i in bondsdb:
        if fix_date(i.issue_date) == fix_date(start_date):
            bond = i

    for intr in intrests:
        bond.set_interest_rate(intrests, intr)
        bond_price = bond.calculate_price(fix_date(intr))
        bond.remaining_coupon = bond.get_remaining_coupon()
        exit_price = bond.remaining_coupon + bond.price_at_purchase
        if bond_price >= exit_price:
            track.append([intr, bond_price, bond.interest_rate, exit_price])
            save_trade_history(track)
            save_trade_to_csv(bond)
            return intr
        intrest = intr
        track.append([intr, bond_price, bond.interest_rate, exit_price])

    save_trade_history(track)
    print(bond.__dict__)

    return intrest


def save_trade_history(track):
    history_df = pd.DataFrame(track, columns=['Date', 'Bond Price', 'Interest Rate', 'Exit Price'])
    history_df.to_excel('bond_sim.xlsx')


active = True   # This variable decides weather the trader is active or not
while active:
    starting_date = bond_strategy(starting_date, bonds_db)
    if starting_date == '2021-11-30':
        active = False
