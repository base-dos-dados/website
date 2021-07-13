from typing_extensions import Annotated
from typing import Optional, List, Union, Literal

from pydantic import StrictInt as Int, Field, StrictStr as Str, BaseModel

from .observations import ObservationLevel

IdType = Annotated[ Optional[Str], Field() ]  # TODO: would be nice to require on show/update but not on create

# TemporalCoverage = List[Annotated[int, Field(ge=1970, le=2030)]]

class TemporalCoverageInt(BaseModel):
    __root__: int = Field(..., ge=1970, le=2030)

TemporalCoverage = List[Union[TemporalCoverageInt, Literal['CHECK']]]
