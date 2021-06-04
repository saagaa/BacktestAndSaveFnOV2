import enum
from datetime import timedelta
class DataGranularity(enum.Enum):
    Daily = 0
    Hourly = 1
    Minutely = 2

    def GetTimeDelta( self ) -> timedelta:
        switcher = {
            DataGranularity.Daily.value: timedelta(days=+1),
            DataGranularity.Hourly.value: timedelta(hours=+1),
            DataGranularity.Minutely.value: timedelta(minutes=+1)
        }
        return switcher.get(self.value, None )

