#!/usr/bin/env python3
from __future__ import annotations
from datetime import datetime
from typing import List, Optional, Literal, Union, Any
import pydantic
from pydantic import StrictInt as Int, StrictStr as Str, Field, ValidationError, validator, PrivateAttr
from uuid import UUID
import jsonschema

from typing_extensions import Annotated # migrate to py3.9

A = Annotated
F = Field
ID_TYPE = A[Optional[Str], F()] # TODO: would be nice to require on show/update but not on create

Email = Str # TODO

from . import resource, BaseModel
from .resource import LaiRequest, ExternalLink, BdmTable

AnyResource = Annotated[Union[LaiRequest, ExternalLink, BdmTable], Field(discriminator='resource_type')]

coerce_to_unicode = lambda field: validator('field', allow_reuse=True)()

class _CkanDefaults(BaseModel):
    id: ID_TYPE
    name: Str

    title: Str
    type: Literal['dataset']
    notes: Optional[Str]
    author: Optional[Str]
    author_email: Optional[Email]
    maintainer: Optional[Str]
    maintainer_email: Optional[Email]
    state: Literal['active']
    license_id: Optional[Str]
    url: Optional[Str]
    version: Optional[Str]
    metadata_created: datetime
    metadata_modified: datetime
    creator_user_id: UUID
    private: bool
    license_title: Optional[Str]



    # Ckan Defaults Complex Fields
    num_resources: Int
    resources: List[AnyResource] = []
    groups: Any
    owner_org: UUID
    organization: Any
    num_tags: Int
    tags: Any

    relationships_as_object: Any
    relationships_as_subject: Any

    # throwaway field that is used to modify validators. You can think of it as an argument to validate function. Cant use prefix underscores on pydantic so used suffix to indicate this
    action__: Optional[Literal['package_show', 'package_create', 'package_update']] # TODO: after 2021-07-01 add exclude by default when issue is merged in master

    @validator('resources', pre=True)
    def resources_should_have_position_field(cls, resources):
        for idx, r in enumerate(resources):
            idx = str(idx) # need to be string cause ckan is dumb and will treat an int 0 as a false value causing problems in later validations
            assert 'position' not in r or str(r['position']) == idx
            r['position'] = idx
        return resources

    @validator('action__', pre=False)
    def ids_should_respect_action(cls, action, config, values, field):
        if not action: return
        if action in ('package_update', 'package_show'):
            assert values['id'] != None, f'package id is None on {action}'
            for idx, r in enumerate(values['resources']):
                assert r.id != None, f"resource {idx!r} id is None on {action}"
        elif action == 'package_create':
            assert values['id'] == None, 'package id is not None on package_create'
            for idx, r in enumerate(values['resources']):
                assert r.id == None, f"resource #{idx!r} id field not is None: {r.id!r} on package_create"



class Package(_CkanDefaults):
    # Custom fields
    download_type: Optional[Literal['Link Externo']] # field_name: download_type # validators: generate_download_type #TODO uncomment generates


# TODO: try to access fields on validation and get annotations on which fields are needed for each tier
