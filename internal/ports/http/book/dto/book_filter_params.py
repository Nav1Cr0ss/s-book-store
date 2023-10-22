from datetime import date
from typing import Any, Optional

from pydantic import model_validator, BaseModel

from internal.domain.book import Genre


class BookParamRequest(BaseModel):
    genre: Optional[Genre] = None
    author_id: Optional[int] = None
    date_start: Optional[date] = None
    date_end: Optional[date] = None

    @model_validator(mode='after')
    def check_date_range(self, data: Any) -> Any:
        start_date = self.date_start
        end_date = self.date_end
        if 1 == sum(x is None for x in (start_date, end_date)):
            raise ValueError("Both date_start and date_end must be provided")
        if start_date and end_date and start_date > end_date:
            raise ValueError("Start date cannot be later than end date")
        return data
