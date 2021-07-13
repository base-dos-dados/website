from datetime import datetime
from typing import List, Optional, Literal, Union, Any
from pydantic import StrictInt as Int, StrictStr as Str, Field, ValidationError, validator, PrivateAttr, root_validator

from ckanext.basedosdados.validator.bdm.metadata_definitions.dataset_definitions import *
from ckanext.basedosdados.validator.ckan_default.package import _CkanDefaults

class BdmDataset(_CkanDefaults):
    # Generated Fields
    # temporal_coverage: TemporalCoverage
    # spatial_coverage: Str
    # observation_level: List[ObservationLevel] = Field(max_items=10)
    # auxiliary_files_url: List[Str]

    download_type: Optional[Literal['Link Externo', 'BD Mais']] # TODO: generate this automatically

    # Ckan Defaults with description
    author           : Optional[Str]      = AUTHOR_FIELD # This field have name and email in YAML
    metadata_modified: Optional[datetime] = METADATA_MODIFIED_FIELD

    # Ckan Defaults Complex Fields
    groups      : Any = GROUPS_FIELD
    organization: Any = ORGANIZATION_FIELD
    tags        : Any = TAGS_FIELD
    
    # TODO: Remove optional from required fields bellow
    # New dataset fields
    dataset_id  : Optional[Str]     = DATASET_ID_FIELD
    url_ckan    : Optional[Str]     = URL_CKAN_FIELD
    url_github  : Optional[Str]     = URL_GITHUB_FIELD
    website     : Optional[Str]     = WEBSITE_FIELD
    languages   : Optional[Str]     = LANGUAGES_FIELD
    free        : Optional[Str]     = FREE_FIELD
    microdata   : Optional[Str]     = MICRODATA_FIELD
    API         : Optional[Str]     = API_FIELD
    availability: Optional[Str]     = AVAILABILITY_FIELD
    brazilian_IP: Optional[Str]     = BRAZILIAN_IP_FIELD
    license     : Optional[Licence] = LICENSE_FIELD
    

    
# TODO: try to access fields on validation and get annotations on which fields are needed for each tier