from datetime import datetime
from typing import TypedDict


class ParamsDateRange(TypedDict):
    start_date: datetime
    end_date: datetime
