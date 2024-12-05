from enum import Enum

from beanie import SortDirection


class EnumOrderBy(str, Enum):
    ASCENDING = "A"
    DESCENDING = "D"

    A = "A"
    D = "D"


DATETIME_BY_X_FORMAT = {
    "_by_year": "%Y",
    "_by_month": "%m",
    "_by_day": "%d",
    "_by_hour": "%H",
    "_by_minute": "%M",
    "_by_second": "%S",
    "_by_year_month": "%Y-%m",
    "_by_year_month_day": "%Y-%m-%d",
    "_by_year_month_day_hour": "%Y-%m-%d %H",
    "_by_year_month_day_hour_minute": "%Y-%m-%d %H:%M",
    "_by_year_month_day_hour_minute_second": "%Y-%m-%d %H:%M:%S",
}

ASCENDING = SortDirection.ASCENDING.value
DESCENDING = SortDirection.DESCENDING.value