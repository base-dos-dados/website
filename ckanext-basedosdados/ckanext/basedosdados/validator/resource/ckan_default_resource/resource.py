from datetime import datetime
from typing_extensions import Annotated

from . import BaseModel, treat_scalar_as_single_value_set
from enum import Enum
from typing import List, Optional, Literal, Union, Set
from pydantic import (
    StrictInt as Int,
    StrictStr as Str,
    Field,
    ValidationError,
    validator,
)
from .data_types import IdType
from .data_types.attr_enum import AttrEnum

YES_NO = Literal["yes", "no"]

F = Field

class UpdateFrequencyEnum(AttrEnum):
    second                        = {"label": "Second"}
    minute                        = {"label": "Minute"}
    hour                          = {"label": "Hour"}
    day                           = {"label": "Day"}
    week                          = {"label": "Week"}
    month                         = {"label": "Month"}
    quarter                       = {"label": "Quarter"}
    semester                      = {"label": "Semester"}
    one_year                      = {"label": "One Year"}
    two_years                     = {"label": "Two Years"}
    three_years                   = {"label": "Three Years"}
    four_years                    = {"label": "Four Years"}
    five_years                    = {"label": "Five Years"}
    ten_years                     = {"label": "Ten Years"}
    unique                        = {"label": "Unique"}
    recurring                     = {"label": "Recurring"}
    empty                         = {"label": "Empty"}
    other                         = {"label": "Other"}


class LanguageEnum(AttrEnum):
    german                        = {"label": "German"}
    arabic                        = {"label": "Arabic"}
    bahasa                        = {"label": "Bahasa"}
    bengali                       = {"label": "Bengali"}
    chinese                       = {"label": "Chinese"}
    spanish                       = {"label": "Spanish"}
    french                        = {"label": "French"}
    hebrew                        = {"label": "Hebrew"}
    hindi                         = {"label": "Hindi"}
    english                       = {"label": "English"}
    japanese                      = {"label": "Japanese"}
    malay                         = {"label": "Malay"}
    portuguese                    = {"label": "Portuguese"}
    russian                       = {"label": "Russian"}
    thai                          = {"label": "Thai"}
    urdu                          = {"label": "Urdu"}


class AvailabilityEnum(AttrEnum):
    online                        = {"label": "Online"}
    physical                      = {"label": "Physical (CD, DVD, paper, etc)"}
    in_person                     = {"label": "In Person"}


class StatusEnum(AttrEnum):
    processing                    = {"label": "Processing"}
    answered                      = {"label": "Answered"}
    denied                        = {"label": "Denied"}


RESOURCE_TYPES = ['bdm_table', 'external_link'] # TODO: add something that test that subclasses obey this constant

class _CkanDefaultResource(BaseModel):
    id: IdType
    name: Str
    description: Str
    position: int
    url: Optional[str] # reserved in ckan


