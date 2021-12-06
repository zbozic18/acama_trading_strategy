from bs4 import BeautifulSoup
import csv
import datetime


# NYU data source: http://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm


# This function takes the DailyTreasuryYieldCurveData.xml file and returns a dict object for a given bond (i.e. tag)
# The tag needs to be in one of the following:
# MONTHS: 'd:BC_1MONTH', 'd:BC_2MONTH', 'd:BC_3MONTH', 'd:BC_6MONTH'
# YRS: 'd:BC_1YEAR', 'd:BC_2YEAR', 'd:BC_3YEAR', 'd:BC_5YEAR', 'd:BC_7YEAR', 'd:BC_10YEAR', 'd:BC_20YEAR', 'd:BC_30YEAR'
def bond_csv_to_dict(tag):
    unsorted_bonds = {}
    bonds = {}
    duration = check_tag(tag)

    # The bellow with statement opens the xml file and assigns the data to the bs_data in a BeautifulSoup format
    # The bs_data is used to make a list of dates and a list of selected_bonds using the tag variable
    with open('asset_data/DailyTreasuryYieldCurveRateData.xml', 'r') as f:
        data = f.read()
    bs_data = BeautifulSoup(data, 'xml')
    bs_dates = bs_data.find_all('d:NEW_DATE')
    dates = []
    for bs_date in bs_dates:
        x = 0
        date = ''
        # The bellow for loop changes the datetime string to a date string
        for letter in bs_date.text:
            x += 1
            if x <= 10:
                date += letter
        dates.append(date)
    selected_bonds = bs_data.find_all(tag)

    # The while loop bellow uses a counter to create a dict object matching the date and coupon of the selected bond
    count = 0
    empty_coupons = 0
    while count < len(dates):
        bond = selected_bonds[count].text
        date = dates[count]
        if bond == '':
            unsorted_bonds[date] = bond
            empty_coupons += 1
        else:
            unsorted_bonds[date] = round(float(bond), 2)
        count += 1

    # The data set is unsorted, the bellow for loop sorts the dict keys and links them to the coupons in a sorted dict
    sorted_dates = sorted(unsorted_bonds)
    for date in sorted_dates:
        bonds[date] = {'coupon': unsorted_bonds[date], 'duration': duration}

    return bonds


# This function reads the historical interest dates from the csv file
# The data starts on the 1954-07-01
def get_interest_rates():
    with open('asset_data/fed-funds-rate-historical-chart.csv', 'r') as file:
        interest_data = csv.reader(file)
        rates = {}
        x = 0
        for line in interest_data:
            x += 1
            if x >= 17 and len(line) == 2:
                rates[line[0]] = line[1]
    return rates


# The function checks the tag of the bond (coming from the xml file) & returns the appropriate duration in years
def check_tag(tag):
    if tag == 'd:BC_1MONTH':
        x = 1 / 12
        return x
    elif tag == 'd:BC_2MONTH':
        x = 1 / 6
        return x
    elif tag == 'd:BC_3MONTH':
        x = 1 / 4
        return x
    elif tag == 'd:BC_6MONTH':
        x = 1 / 2
        return x
    elif tag == 'd:BC_1YEAR':
        return 1
    elif tag == 'd:BC_2YEAR':
        return 2
    elif tag == 'd:BC_3YEAR':
        return 3
    elif tag == 'd:BC_5YEAR':
        return 5
    elif tag == 'd:BC_7YEAR':
        return 7
    elif tag == 'd:BC_10YEAR':
        return 10
    elif tag == 'd:BC_20YEAR':
        return 20
    elif tag == 'd:BC_30YEAR':
        return 30
