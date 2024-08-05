from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def calc_password(current_date=datetime.now()):
    # Format the date as YYYYMM and convert to integer
    di = int(current_date.strftime("%Y%m"))
    di = di**7 + 342*di**6 + 2345*di**5 + 2701*di**4 + 345464*di**3 + 854341*di**2 + 5687894*di + 345742943
    return str((di % 9160721) % 10000).zfill(4)

def calc_password_for_next_n_days(n):
    passwords = {}
    current_date = datetime.now()
    for i in range(n):
        date = current_date + relativedelta(months=i)
        password = calc_password(date)
        passwords[date.strftime("%Y-%m")] = password

    return passwords

# Example usage:
n = 100
passwords = calc_password_for_next_n_days(n)
for date, password in passwords.items():
    print(f"Date: {date}, Password: {password}")
