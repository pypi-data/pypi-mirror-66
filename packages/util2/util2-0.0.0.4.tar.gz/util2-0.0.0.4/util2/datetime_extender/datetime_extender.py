# -*- coding: uTf-8 -*-
import datetime as dt
from dateutil.relativedelta import relativedelta
import calendar

class DatetimeExtender():
    def last_date(self, date):
        return date.replace(day=calendar.monthrange(date.year, date.month)[1])

    def first_date(self, date):
       return date.replace(day=1)

    ##
    # @fn month_first_last_date
    # @brief get month first and last date.指定した日時の月初め、月末の時間を返します。
    # @param first_date Datetime-First date.最初の月初めの日時。
    # @param last_date Datetime-Last date.最初の月末の日時。
    # @param month_num Integer-Month num.月数。
    # @param date_format String-Datetime format(default:'%Y-%m-%d %H:%M:%S').Datetime型のフォーマット。
    # @retval dist["first_dates"] Dictionary-First date times list(Datetime).月初めの日時データが月数分だけリスト化。
    # @retval dist["last_dates"] Dictionary-Last date times list(Datetime).月末の日時データが月数分だけリスト化。
    # @retval dist["first_dates_string"] Dictionary-First date times list(String).月初めの日時データが月数分だけリスト化。
    # @retval dist["last_dates_string"] Dictionary-Last date times list(String).月末の日時データが月数分だけリスト化。
    def month_first_last_date(self, first_date, last_date, month_num, date_format='%Y-%m-%d %H:%M:%S'):
        if type(first_date) is str:
            first_date = dt.datetime.strptime(first_date, date_format)
        if type(last_date) is str:
            last_date = dt.datetime.strptime(last_date, date_format)
        first_dates = []
        last_dates = []
        first_dates_string = []
        last_dates_string = []

        # 指定した月日の月初めと月末を計算
        first_date = self.first_date(first_date)
        last_date = self.last_date(last_date)
        first_dates.append(first_date)
        last_dates.append(last_date)
        first_dates_string.append(first_date.strftime(date_format))
        last_dates_string.append(last_date.strftime(date_format))

        for cnt in range(month_num):
            tmp_first_date = first_date + relativedelta(months=1)
            tmp_last_date = last_date + relativedelta(months=1)
            first_date = self.first_date(tmp_first_date)
            last_date = self.last_date(tmp_last_date)
            first_dates.append(first_date)
            last_dates.append(last_date)
            first_dates_string.append(first_date.strftime(date_format))
            last_dates_string.append(last_date.strftime(date_format))

        return {"first_dates": first_dates,
                "last_dates": last_dates,
                "first_dates_string": first_dates_string,
                "last_dates_string": last_dates_string}


def main():
    FIRST_DATE = "2019-04-01 00:00:00"
    LAST_DATE = "2019-04-30 00:00:00"
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    MONTH_NUM = 11

    dtex = DatetimeExtender()
    result = dtex.month_first_last_date(
        FIRST_DATE, LAST_DATE, MONTH_NUM, date_format=DATE_FORMAT)
    print(result)


if __name__ == "__main__":
    main()

    """
    {'first_dates': [datetime.datetime(2019, 4, 1, 0, 0), datetime.datetime(2019, 5, 1, 0, 0), datetime.datetime(2019, 6, 1, 0, 0), datetime.datetime(2019, 7, 1, 0, 0), datetime.datetime(2019, 8, 1, 0, 0), datetime.datetime(2019, 9, 1, 0, 0), datetime.datetime(2019, 10, 1, 0, 0), datetime.datetime(2019, 11, 1, 0, 0), datetime.datetime(2019, 12, 1, 0, 0), datetime.datetime(2020, 1, 1, 0, 0), datetime.datetime(2020, 
    2, 1, 0, 0), datetime.datetime(2020, 3, 1, 0, 0)], 'last_dates': [datetime.datetime(2019, 4, 30, 0, 0), datetime.datetime(2019, 5, 31, 0, 
    0), datetime.datetime(2019, 6, 30, 0, 0), datetime.datetime(2019, 7, 31, 0, 0), datetime.datetime(2019, 8, 31, 0, 0), datetime.datetime(2019, 9, 30, 0, 0), datetime.datetime(2019, 10, 31, 0, 0), datetime.datetime(2019, 11, 30, 0, 0), datetime.datetime(2019, 12, 31, 0, 0), datetime.datetime(2020, 1, 31, 0, 0), datetime.datetime(2020, 2, 29, 0, 0), datetime.datetime(2020, 3, 31, 0, 0)], 'first_dates_string': ['2019-04-01 00:00:00', '2019-05-01 00:00:00', '2019-06-01 00:00:00', '2019-07-01 00:00:00', '2019-08-01 00:00:00', '2019-09-01 00:00:00', '2019-10-01 00:00:00', '2019-11-01 00:00:00', '2019-12-01 00:00:00', '2020-01-01 00:00:00', '2020-02-01 00:00:00', '2020-03-01 00:00:00'], 'last_dates_string': ['2019-04-30 00:00:00', '2019-05-31 00:00:00', '2019-06-30 00:00:00', '2019-07-31 00:00:00', '2019-08-31 00:00:00', '2019-09-30 00:00:00', '2019-10-31 00:00:00', '2019-11-30 00:00:00', '2019-12-31 00:00:00', '2020-01-31 00:00:00', '2020-02-29 00:00:00', '2020-03-31 00:00:00']}
    """
