import numpy as np

_y,_m,_d = "M8[Y]", "M8[M]", "M8[D]"

def create_date(year, month=1, day=1):
    return ((np.asarray(year-1970, dtype=_y) 
               + np.timedelta64(month-1, "M")).astype(_d) 
           + day-1)

def day(dt):
    """1-31"""
    return dt.astype(int) - dt.astype(_m).astype(_d).astype(int) + 1

def month(dt):
    """1-12"""
    return dt.astype(_m).astype(int) % 12 + 1

def year(dt):
    return dt.astype(_y).astype(int) + 1970

def weekday(dt):
    """Mon..Sun: 1..7"""
    return (dt.astype(int) - 4) % 7 + 1

def is_weekday(dt, wd):
    return weekday(dt) == wd

def is_monthbegin(dt):
    return day(dt) == 1

def is_monthend(dt):
    return day(dt+1) == 1

def add_bdays(dt, n, calendar):
    return np.busday_offset(dt, 
                            n-(n>0)*(1-np.is_busday(dt,busdaycal=calendar)), # Hack - counter that np.busday_offset will move forward to first valid bus day before applying offset
                            roll="following",
                            busdaycal=calendar)

def add_weeks(dt, n, ref):
    """Ref: 1-7 (Mon..Sun)"""
    return dt+(ref-1-((dt-4).astype(int)%7))%7+7*(n-(weekday(dt)!=ref)*(n>0))

def add_months(dt, n):
    new_month = dt.astype(_m) + n
    days_in_new_month = day((new_month+1).astype(_d) - 1)
    new_day = np.minimum(day(dt), days_in_new_month)
    return new_month.astype(_d) + new_day - 1

def islastbdayinmonth(dt, calendar):
    return dt.astype(_m) != add_bdays(dt,1,calendar).astype(_m)

def add_months_end_end(dt, n, calendar):
    islastbday = islastbdayinmonth(dt, calendar)
    dt = np.array(add_months(dt,n))
    dt[islastbday] = add_bdays(add_monthbegins(dt,1),-1,calendar)
    return dt

def add_monthbegins(dt, n):
    return (dt.astype(_m)+n+np.logical_not(is_monthbegin(dt))*(n<=0)).astype(_d)

def add_monthends(dt, n):
    return (dt.astype(_m)+1+n-np.logical_not(is_monthend(dt))*(n>0)).astype(_d)-1
   
