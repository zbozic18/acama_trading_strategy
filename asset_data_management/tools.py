import datetime


# The month variable has to be in the |example: 'Jan'| format
def find_str_month(date):
    month = str(date[0]) + str(date[1]) + str(date[2])
    if month == 'Jan':
        return '01'
    if month == 'Feb':
        return '02'
    if month == 'Mar':
        return '03'
    if month == 'Apr':
        return '04'
    if month == 'May':
        return '05'
    if month == 'Jun':
        return '06'
    if month == 'Jul':
        return '07'
    if month == 'Aug':
        return '08'
    if month == 'Sep':
        return '09'
    if month == 'Oct':
        return '10'
    if month == 'Nov':
        return '11'
    if month == 'Dec':
        return '12'


def make_date_time(year, day='01', month='01'):
    date_str = f'{year}-{month}-{day}'
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return date


def get_year(date):
    year = str(date[4]) + str(date[5]) + str(date[6]) + str(date[7])
    return year


def fix_date(date):
    new_date = ''
    for i in date:
        new_date += i
        if len(new_date) == 8:
            break
    new_date += '01'
    fixed = str(datetime.datetime.strptime(new_date, '%Y-%m-%d').date())
    return fixed


def change_year(date, change):
    year_ch = int(date[2] + date[3])
    year = date[0] + date[1] + str(year_ch + change)
    new_date = year + date[4] + date[5] + date[6] + date[7] + date[8] + date[9]
    return new_date


def get_dif_years(date1, date2):
    year1 = date1[0] + date1[1] + date1[2] + date1[3]
    year2 = date2[0] + date2[1] + date2[2] + date2[3]
    diff = int(year2) - int(year1)
    return diff


def save_trade_to_csv(bond):
    print(bond.__dict__)


def find_date(df_stock, date):
    dates = df_stock['Date'].to_list()
    if date in dates:
        return dates.index(date)
    else:
        return None
