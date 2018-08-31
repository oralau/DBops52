import calendar
import datetime


def getNextMonday():




    st = datetime.datetime.strptime(start_time,'%Y-%m-%d')
    oneday = datetime.timedelta(days = 1)
    m1 = calendar.SUNDAY

    while st.weekday() != m1:
        st += oneday

    nextMonday = today.strftime('%Y-%m-%d')

