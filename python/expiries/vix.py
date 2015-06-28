import datetime as dt


def get_expiry_date_for_month(curr_date):
    """
    http://cfe.cboe.com/products/spec_vix.aspx

    TERMINATION OF TRADING:

    Trading hours for expiring VIX futures contracts end at 7:00 a.m. Chicago
    time on the final settlement date.

    FINAL SETTLEMENT DATE:

    The Wednesday that is thirty days prior to the third Friday of the
    calendar month immediately following the month in which the contract
    expires ("Final Settlement Date"). If the third Friday of the month
    subsequent to expiration of the applicable VIX futures contract is a
    CBOE holiday, the Final Settlement Date for the contract shall be thirty
    days prior to the CBOE business day immediately preceding that Friday.
    """
    # Date of third friday of the following month
    if curr_date.month == 12:
        third_friday_next_month = dt.date(curr_date.year + 1, 1, 15)
    else:
        third_friday_next_month = dt.date(curr_date.year,
                                          curr_date.month + 1, 15)

    one_day = dt.timedelta(days=1)
    thirty_days = dt.timedelta(days=30)
    while third_friday_next_month.weekday() != 4:
        # Using += results in a timedelta object
        third_friday_next_month = third_friday_next_month + one_day

    # TODO: Incorporate check that it's a trading day, if so move the 3rd
    # Friday back by one day before subtracting
    return third_friday_next_month - thirty_days
