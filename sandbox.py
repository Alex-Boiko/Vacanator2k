from datetime import date

def diff_month(d1, d2):
    return (d1.year - d2.year)*12 + d1.month - d2.month

print abs(diff_month(date(2010,10,1), date(2011,3,1)))
assert diff_month(date(2010,10,1), date(2009,10,1)) == 12
assert diff_month(date(2010,10,1), date(2009,11,1)) == 11
assert diff_month(date(2010,10,1), date(2009,8,1)) == 14