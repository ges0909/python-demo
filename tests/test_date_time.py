from datetime import datetime, timedelta


# date is within a period of: 1 year
def test_subtract_time_delta():
    now = datetime.now()
    delta = timedelta(days=365)
    one_year_before_now = now - delta
    print(one_year_before_now)


def test_from_iso_format():
    datetime_str = "2020-06-22T08:17:47.669+02:00"
    datetime_obj = datetime.fromisoformat(datetime_str)  # raises ValueError and TypeError
    assert datetime_obj <= datetime.now(tz=datetime_obj.tzinfo)
