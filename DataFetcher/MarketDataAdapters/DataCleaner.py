from datetime import datetime

class DataCleaner:
    @staticmethod
    def CleanDateTime( dt : datetime) -> datetime:
        return dt.replace(tzinfo=None)
