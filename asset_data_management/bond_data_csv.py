import csv
from asset_data_management.tools import make_date_time, find_str_month, get_year


def get_10_y_bond_history():
    with open('asset_data_management/asset_data/histoical_bond_coupons.csv', 'r') as file:
        data = csv.reader(file)
        bond_data = {}

        first = True
        for line in data:
            if not first:
                year = get_year(line[0])
                month = find_str_month(line[0])
                date = make_date_time(year=year, month=month).date()
                bond_data[str(date)] = float(line[5]) / 100
            first = False
        return bond_data
