import datetime
from typing_extensions import Annotated

from . import BaseModel
from enum import Enum
from typing import List, Optional, Literal, Union
from pydantic import (
    StrictInt as Int,
    StrictStr as Str,
    Field,
    ValidationError,
    validator,
)
from .data_types import ObservationLevel, TemporalCoverage, IdType

YES_NO = Literal["yes", "no"]


class UpdateFrequencyEnum(str, Enum):
    second = "second"  # "Second"
    minute = "minute"  # "Minute"
    hour = "hour"  # "Hour"
    day = "day"  # "Day"
    week = "week"  # "Week"
    month = "month"  # "Month"
    quarter = "quarter"  # "Quarter"
    semester = "semester"  # "Semester"
    one_year = "one_year"  # "One Year"
    two_years = "two_years"  # "Two Years"
    three_years = "three_years"  # "Three Years"
    four_years = "four_years"  # "Four Years"
    five_years = "five_years"  # "Five Years"
    ten_years = "ten_years"  # "Ten Years"
    unique = "unique"  # "Unique"
    recurring = "recurring"  # "Recurring"
    empty = "empty"  # "Empty"
    other = "other"  # "Other"


class LanguageEnum(str, Enum):
    german = "german"  # "German"
    arabic = "arabic"  # "Arabic"
    bahasa = "bahasa"  # "Bahasa"
    bengali = "bengali"  # "Bengali"
    chinese = "chinese"  # "Chinese"
    spanish = "spanish"  # "Spanish"
    french = "french"  # "French"
    hebrew = "hebrew"  # "Hebrew"
    hindi = "hindi"  # "Hindi"
    english = "english"  # "English"
    japanese = "japanese"  # "Japanese"
    malay = "malay"  # "Malay"
    portuguese = "portuguese"  # "Portuguese"
    russian = "russian"  # "Russian"
    thai = "thai"  # "Thai"
    urdu = "urdu"  # "Urdu"


class AvailabilityEnum(str, Enum):
    online = "online"  # Online
    physical = "physical"  # Physical (CD, DVD, paper, etc)
    in_person = "in_person"  # In Person


class StatusEnum(str, Enum):
    processing = "Processing"
    answered = "Answered"
    denied = "Denied"


RESOURCE_TYPES = ['lai_request', 'bdm_table', 'external_link'] # TODO: add something that test that subclasses obey this constant

class Resource(BaseModel):
    id: IdType
    name: Str
    description: Str
    spatial_coverage: Str
    temporal_coverage: TemporalCoverage
    update_frequency: UpdateFrequencyEnum
    position: int
    url: Optional[str] # reserved in ckan


# TODO: Remove only_on_types, required
# Required for later
"""
class LaiRequest(Resource):
    resource_type: Literal["lai_request"]
    
    origin: Str  # Validators  required_on_types(lai_request)
    protocol_number: Str  # Validators  required_on_types(lai_request)
    superior_organ: Str  # Validators  required_on_types(lai_request)
    linked_organ: Str  # Validators  required_on_types(lai_request)
    start_date: datetime.date  # Validators  required_on_types(lai_request) scheming_required isodate convert_to_json_if_date
    who_requested: Str  # Validators  # required_on_types(lai_request)
    status: StatusEnum  # Validatos  required_on_types(lai_request) scheming_required scheming_choices
    request_url: Str  # Validators  required_on_types(lai_request) ignore_missing unicode remove_whitespace
    data_url: Str  # Validators  ignore_missing unicode remove_whitespace #required_on_types(lai_request)
    observations: Str  # Validators  # required_on_types(lai_request)
    lai_n: int
"""

class BdmTable(Resource):
    resource_type: Literal["bdm_table"]

    table_id: Str  # Validator only on types
    auxiliary_files_url: Optional[
        Str
    ]  # Validators ignore_missing unicode remove_whitespace
    treatment_description: Optional[Str]
    observation_level: Optional[List[ObservationLevel]] = Field(max_items=10) # Required for tier 1
    columns: Optional[Str] # Required for tier 1
    primary_keys: Optional[Str] # Required for tier 1
    version: Optional[Str] # Required for tier 1
    publisher: Optional[Str] # Required for tier 1
    publisher_email: Optional[Str] # Required for tier 1
    publisher_github: Optional[Str] # Required for tier 1
    publisher_website: Optional[Str] # Required for tier 1

    # TODO: implement this
    def table_id_should_be_a_valid_bigquery_identifier(cls, value):
        pass

class ExternalLink(Resource):
    resource_type: Literal["external_link"]

    url: str  # Validators ignore_missing unicode remove_whitespace # TODO: add check_url_is_alive validator
    language: List[LanguageEnum] = Field(
        max_items=10
    )  # TODO: @dahis, serio q eh so no external link ?
    has_api: YES_NO  # Validators scheming_required scheming_choices # TODO: data check
    free: YES_NO  # Validators scheming_required scheming_choices
    signup_needed: YES_NO  # Validators scheming_required scheming_choice
    availability: AvailabilityEnum  # Validators scheming_required scheming_choices
    brazilian_ip: YES_NO  # Validators scheming_required scheming_choices
    license_type: Str