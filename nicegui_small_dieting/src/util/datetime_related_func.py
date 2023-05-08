import datetime
import pytz


def get_today_date() -> str:
    tz = pytz.timezone('Asia/Tokyo')
    date: str = datetime.datetime.now(tz).strftime('%Y-%m-%d')
    return date