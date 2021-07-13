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
from ckanext.basedosdados.validator.bdm.metadata_definitions.table_definitions import *

from ckanext.basedosdados.validator.ckan_default.data_types import ObservationLevel, TemporalCoverage, IdType
from ckanext.basedosdados.validator.ckan_default.resource import _CkanDefaultResource, UpdateFrequencyEnum



class Resource(_CkanDefaultResource):
    spatial_coverage: Optional[Str] # Required for tier 1
    temporal_coverage: Optional[TemporalCoverage] # Required for tier 1
    update_frequency: Optional[UpdateFrequencyEnum] # Required for tier 1


class BdmTable(Resource):
    resource_type:           Literal["bdm_table"]

    table_id             : Str                              = TABLE_ID_FIELD
    auxiliary_files_url  : Optional[Str]
    treatment_description: Optional[Str]                    = TREATMENT_DESCRIPTION_FIELD
    observation_level    : Optional[Set[ObservationLevel]]  = OBSERVATION_LEVEL_FIELD      # Required for tier 1
    columns              : Optional[Str]                                                   # Required for tier 1
    primary_keys         : Optional[Str]                    = PRIMARY_KEYS_FIELD           # Required for tier 1
    version              : Optional[Str]                    = VERSION                      # Required for tier 1
    publisher            : Optional[Str]                                                   # Required for tier 1
    publisher_email      : Optional[Str]                                                   # Required for tier 1
    publisher_github     : Optional[Str]                                                   # Required for tier 1
    publisher_website    : Optional[Str]                                                   # Required for tier 1

    _observation_level_validator = treat_scalar_as_single_value_set('observation_level')

    bdm_file_size: Union[int, None, Literal['Unavailable', '']] # should not be editable in form, also, check what use is Unavailable

    # Resource fields
    spatial_coverage : Optional[Str]                 = SPATIAL_COVERAGE_FIELD    # Required for tier 1
    temporal_coverage: Optional[TemporalCoverage]    = TEMPORAL_COVERAGE_FIELD   # Required for tier 1
    update_frequency : Optional[UpdateFrequencyEnum] = UPDATE_FREQUENCY_FIELD    # Required for tier 1
    
    # TODO: Remove optional from required fields bellow
    # New YAML FIELDS
    metadata_modified  : Optional[datetime]    = METADATA_MODIFIED_FIELD
    dataset_id         : Optional[Str]         = DATASET_ID_FIELD
    source_bucket_name : Optional[Str]         = SOURCE_BUCKET_NAME_FIELD
    project_id_staging : Optional[Str]         = PROJECT_ID_STAGING
    project_id_prod    : Optional[Str]         = PROJECT_ID_PROD_FIELD
    url_ckan           : Optional[Str]         = URL_CKAN_FIELD
    url_github         : Optional[Str]         = URL_GITHUB
    description        : Optional[Str]         = DESCRIPTION_FIELD
    published_by       : Optional[PublishedBy] = PUBLISHED_BY_FIELD
    treated_by         : Optional[TreatedBy]   = TREATED_BY_FIELD
    partitions         : Optional[Str]         = PARTITIONS_FIELD

    
    
    @validator('bdm_file_size')
    def null_string_is_none(cls, value): # TODO: check why this is not working, as it is still failing when we pass a ''. Had to add '' to type signature
        if value == '':
            return None

    # TODO: implement this
    def table_id_should_be_a_valid_bigquery_identifier(cls, value):
        pass