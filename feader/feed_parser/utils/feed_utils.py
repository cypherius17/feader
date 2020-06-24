from datetime import datetime
from time import mktime


class FeedUtils:
    @staticmethod
    def datetime_from_pub_date(pub_date):
        return datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")

    @staticmethod
    def write_to_log_file(log_file, log):
        with open(log_file, 'a') as f:
            f.write(log)
