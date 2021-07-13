#!/usr/bin/env python3
from datetime import datetime
from typing import List, Optional, Literal, Union, Any, Dict
import pydantic
from pydantic import (
    StrictInt as Int,
    StrictStr as Str,
    Field,
    ValidationError,
    validator,
    PrivateAttr,
    root_validator,
)
from ckanext.basedosdados.validator.ckan_default import BaseModel


class Author(BaseModel):
    name: Str = Field(user_input_hint=["<nome>"])
    email: Str = Field(user_input_hint=["<email>"])


class Licence(BaseModel):
    name: Str = Field(user_input_hint=["MIT"])
    url: Str = Field(user_input_hint=["<url>"])


to_line = lambda description: "\n".join(description)


###################
### YAML FIELDS ###
###################

METADATA_MODIFIED_FIELD = Field(
    title="metadata_modified",
    user_input_hint=["<YYYY-MM-DD>"],
    description=to_line(["AUTO GENERATED"]),
    yaml_order={
        "id_before": None,
        "id_after": "dataset_id",
    },
)

DATASET_ID_FIELD = Field(
    title="dataset_id",
    user_input_hint=["<dataset_id>"],
    description=to_line(["AUTO GENERATED"]),
    yaml_order={
        "id_before": "metadata_modified",
        "id_after": "url_ckan",
    },
)

URL_CKAN_FIELD = Field(
    title="url_ckan",
    user_input_hint=["https://basedosdados.org/dataset/<dataset_id>"],
    description=to_line(["AUTO GENERATED"]),
    yaml_order={
        "id_before": "dataset_id",
        "id_after": "url_github",
    },
)

URL_GITHUB_FIELD = Field(
    title="url_github",
    user_input_hint=[
        "https://github.com/basedosdados/mais/tree/master/bases/<dataset_id>"
    ],
    description=to_line(["AUTO GENERATED"]),
    yaml_order={
        "id_before": "url_ckan",
        "id_after": "description",
    },
)

DESCRIPTION_FIELD = Field(
    title="description",
    user_input_hint=["<descrição>"],
    description=to_line(
        [
            "Descreva a base",
            "Ela é sobre o que?",
            "Quais as principais fontes de dados?",
            "Há links para FAQs e explicações?",
        ]
    ),
    yaml_order={
        "id_before": "url_github",
        "id_after": "organization",
    },
)

ORGANIZATION_FIELD = Field(
    title="organization",
    user_input_hint=["<organização>"],
    description=to_line(
        [
            "Qual organização disponibiliza os dados originais?",
            "Opções: escolher dessa lista -> https://basedosdados.org/api/3/action/organization_list=",
        ]
    ),
    yaml_order={
        "id_before": "description",
        "id_after": "author",
    },
)

AUTHOR_FIELD = Field(
    title="author",
    description=to_line(["Qual departamento/grupo/pessoa mantém os dados originais?"]),
    yaml_order={
        "id_before": "organization",
        "id_after": "website",
    },
)

WEBSITE_FIELD = Field(
    title="website",
    user_input_hint=["<website>"],
    description=to_line(["Onde encontrar os dados originais e mais informações?"]),
    yaml_order={
        "id_before": "author",
        "id_after": "groups",
    },
)

GROUPS_FIELD = Field(
    title="groups",
    user_input_hint=["<grupo>"],
    description=to_line(
        [
            "Quais grupos caracterizam a base?",
            "Opções: escolher dessa lista -> https://basedosdados.org/api/3/action/group_list",
        ]
    ),
    yaml_order={
        "id_before": "website",
        "id_after": "tags",
    },
)

TAGS_FIELD = Field(
    title="tags",
    user_input_hint=["<etiqueta>"],
    description=to_line(
        [
            "Quais etiquetas caracterizam a base?",
            "Opções: escolher dessa lista -> https://basedosdados.org/api/3/action/tag_list",
            "Caso crie etiquetas novas, as regras são:",
            "   - letras minúsculas",
            "   - sem acentos",
            "   - não repita nomes de grupos (ex. educacao, saude, meio ambiente, economia, etc.)",
        ]
    ),
    yaml_order={
        "id_before": "groups",
        "id_after": "languages",
    },
)

LANGUAGES_FIELD = Field(
    title="languages",
    user_input_hint=["<língua>"],
    description=to_line(
        [
            "Em quais línguas a base (ou a fonte original) está disponível?",
            "Regras: minúsculo, sem acentos.",
            "Opções: portugues, ingles, espanhol, frances, chines, russo, hindi, alemao, etc.",
        ]
    ),
    yaml_order={
        "id_before": "tags",
        "id_after": "free",
    },
)

FREE_FIELD = Field(
    title="free",
    user_input_hint=["<sim/não>"],
    description=to_line(["Os dados originais estão disponíveis de graça?"]),
    yaml_order={
        "id_before": "languages",
        "id_after": "microdata",
    },
)

MICRODATA_FIELD = Field(
    title="microdata",
    user_input_hint=["<sim/não>"],
    description=to_line(["Os microdados estão disponíveis para download?"]),
    yaml_order={
        "id_before": "free",
        "id_after": "API",
    },
)

API_FIELD = Field(
    title="API",
    user_input_hint=["<sim/não>"],
    description=to_line(["Existe uma API na fonte original?"]),
    yaml_order={
        "id_before": "microdata",
        "id_after": "registration",
    },
)

REGISTRATION_FIELD = Field(
    title="registration",
    user_input_hint=["<sim/não>"],
    description=to_line(
        ["É necessário registrar um usuário para baixar os dados originais?"]
    ),
    yaml_order={
        "id_before": "API",
        "id_after": "availability",
    },
)

AVAILABILITY_FIELD = Field(
    title="availability",
    user_input_hint=["<online/físico>"],
    description=to_line(["Como os dados originais estão disponibilizados?"]),
    yaml_order={
        "id_before": "registration",
        "id_after": "brazilian_IP",
    },
)

BRAZILIAN_IP_FIELD = Field(
    title="brazilian_IP",
    user_input_hint=["<sim/não>"],
    description=to_line(["A fonte original requer IP brasileiro para acesso?"]),
    yaml_order={
        "id_before": "availability",
        "id_after": "license",
    },
)

LICENSE_FIELD = Field(
    title="license",
    description=to_line(
        [
            "Essa base está sob qual licença?",
            "A licença MIT se aplica a bases públicas.",
            "Caso não seja pública, ver opções aqui: https://help.data.world/hc/en-us/articles/115006114287-Common-license-types-for-datasets",
        ]
    ),
    yaml_order={
        "id_before": "brazilian_IP",
        "id_after": None,
    },
)
