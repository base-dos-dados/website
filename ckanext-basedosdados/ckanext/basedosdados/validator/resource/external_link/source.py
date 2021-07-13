from datetime import datetime
from typing_extensions import Annotated

from enum import Enum
from typing import List, Optional, Literal, Union, Set
from pydantic import (
    StrictInt as Int,
    StrictStr as Str,
    Field,
    ValidationError,
    validator,
)

from ckanext.basedosdados.validator.ckan_default import treat_scalar_as_single_value_set

from ckanext.basedosdados.validator.ckan_default.data_types import ObservationLevel, TemporalCoverage, IdType
from ckanext.basedosdados.validator.ckan_default.resource import _CkanDefaultResource, UpdateFrequencyEnum, LanguageEnum, AvailabilityEnum

YES_NO = Literal["yes", "no"]

class Resource(_CkanDefaultResource):
    spatial_coverage: Optional[Str] # Required for tier 1
    temporal_coverage: Optional[TemporalCoverage] # Required for tier 1
    update_frequency: Optional[UpdateFrequencyEnum] # Required for tier 1

class ExternalLink(Resource):
    resource_type:             Literal["external_link"]

    url:                       str                                                # Required for tier 1 # TODO: add check_url_is_alive validator check is url
    language:                  Optional[Set[LanguageEnum]] = Field( max_items=10) # Required for tier 1 # TODO: @dahis, serio q eh so no external link ?
    has_api:                   Optional[YES_NO]                                   # Required for tier 1 # TODO: data check
    free:                      Optional[YES_NO]                                   # Required for tier 1
    signup_needed:             Optional[YES_NO]                                   # Required for tier 1
    availability:              Optional[AvailabilityEnum]                         # Required for tier 1
    brazilian_ip:              Optional[YES_NO]                                   # Required for tier 1
    license_type:              Optional[Str]                                      # Required for tier 1

    _language_validator = treat_scalar_as_single_value_set('language')