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


class PublishedBy(BaseModel):
    name: Str = Field(user_input_hint=["<nome [você]>"])
    code_url: Str = Field(
        user_input_hint=[
            "https://github.com/basedosdados/mais/tree/master/bases/<dataset_id>/code"
        ]
    )
    website: Str = Field(user_input_hint=["<website>"])
    email: Str = Field(user_input_hint=["<email>"])


class TreatedBy(BaseModel):
    name: Str = Field(user_input_hint=["<nome>"])
    code_url: Str = Field(user_input_hint=["<onde encontrar código de tratamento>"])
    website: Str = Field(user_input_hint=["<onde encontrar os dados tratados>"])
    email: Str = Field(user_input_hint=["<email>"])


class TreatedBy(BaseModel):
    name: Str = Field(user_input_hint=["<nome>"])
    code_url: Str = Field(user_input_hint=["<onde encontrar código de tratamento>"])
    website: Str = Field(user_input_hint=["<onde encontrar os dados tratados>"])
    email: Str = Field(user_input_hint=["<email>"])


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
        "id_after": "table_id",
    },
)

TABLE_ID_FIELD = Field(
    title="table_id",
    user_input_hint=["<table_id>"],
    description=to_line(["AUTO GENERATED"]),
    yaml_order={
        "id_before": "dataset_id",
        "id_after": "source_bucket_name",
    },
)

SOURCE_BUCKET_NAME_FIELD = Field(
    title="source_bucket_name",
    user_input_hint=["<source_bucket_name>"],
    description=to_line(["AUTO GENERATED"]),
    yaml_order={
        "id_before": "table_id",
        "id_after": "project_id_staging",
    },
)

PROJECT_ID_STAGING = Field(
    title="project_id_staging",
    user_input_hint=["<project_id_staging>"],
    description=to_line(["AUTO GENERATED"]),
    yaml_order={
        "id_before": "source_bucket_name",
        "id_after": "project_id_prod",
    },
)

PROJECT_ID_PROD_FIELD = Field(
    title="project_id_prod",
    user_input_hint=["<project_id_prod>"],
    description=to_line(["AUTO GENERATED"]),
    yaml_order={
        "id_before": "project_id_staging",
        "id_after": "url_ckan",
    },
)

# TODO: remove this field?
URL_CKAN_FIELD = Field(
    title="url_ckan",
    user_input_hint=["<https://basedosdados.org/dataset/<dataset_id>"],
    description=to_line(["AUTO GENERATED"]),
    yaml_order={
        "id_before": "project_id_prod",
        "id_after": "url_github",
    },
)

URL_GITHUB: Str = Field(
    title="url_github",
    user_input_hint=[
        "<https://github.com/basedosdados/mais/tree/master/bases/<dataset_id>"
    ],
    description=to_line(["AUTO GENERATED"]),
    yaml_order={
        "id_before": "url_ckan",
        "id_after": "version",
    },
)

VERSION: Str = Field(
    title="version",
    user_input_hint=["<vA.B>"],
    description=to_line(["Exemplo versão v1.0"]),
    yaml_order={
        "id_before": "url_github",
        "id_after": "description",
    },
)

DESCRIPTION_FIELD = Field(
    title="description",
    user_input_hint=["<descrição>"],
    description=to_line(
        [
            "Descreva a tabela. Essas são as primeiras frases que um usuário vai ver.",
            "Você não precisa ser muito conciso. Sinta-se a vontade para dar exemplos de",
            "como usar os dados.",
            "Se souber, liste também aplicações: pesquisa, apps, etc. que usem os dados.,",
        ]
    ),
    yaml_order={
        "id_before": "version",
        "id_after": "published_by",
    },
)

# TODO: DITC TYPE
PUBLISHED_BY_FIELD = Field(
    title="published_by",
    user_input_hint=["<nome>"],
    description=to_line(["Quem está completando esse arquivo config?"]),
    yaml_order={
        "id_before": "description",
        "id_after": "treated_by",
    },
)

# TODO: DITC TYPE
TREATED_BY_FIELD = Field(
    title="treated_by",
    user_input_hint=["<nome>"],
    description=to_line(
        [
            "Qual organização/departamento/pessoa tratou os dados?",
            "As vezes há um ponto intermediário entre os dados originais e subir na Base dos Dados.",
            "Se essa pessoa é você, preencha abaixo com suas informações.",
        ]
    ),
    yaml_order={
        "id_before": "published_by",
        "id_after": "treatment_description",
    },
)

TREATMENT_DESCRIPTION_FIELD = Field(
    title="treatment_description",
    user_input_hint=["<CEPESP fez X. Eu fiz K>"],
    description=to_line(
        [
            "Se houve passos de tratamento, limpeza e manipulação de dados, descreva-os aqui."
        ]
    ),
    yaml_order={
        "id_before": "treated_by",
        "id_after": "update_frequency",
    },
)

UPDATE_FREQUENCY_FIELD = Field(
    title="update_frequency",
    user_input_hint=["<frequência>"],
    description=to_line(
        [
            "Com qual frequência a base é atualizada?",
            "Opções: hora | dia | semana | mes | 1 ano | 2 anos | 5 anos | 10 anos | unico | recorrente",
        ]
    ),
    yaml_order={
        "id_before": "treatment_description",
        "id_after": "observation_level",
    },
)

OBSERVATION_LEVEL_FIELD = Field(
    title="observation_level",
    user_input_hint=["<primeira coluna>"],
    description=to_line(
        [
            "Nível da observação (qual é a granularidade de cada linha na tabela)",
            "Escolha todas as opções necessárias.",
            "Regras:",
            "  - minúsculo, sem acento, singular.",
            "  - em portugues (ou seja, não use os nomes de colunas abaixo)",
            "Exemplos: pais, estado, municipio, cidade, hora, dia, semana, mes, ano, etc.",
        ]
    ),
    max_items=10,
    yaml_order={
        "id_before": "update_frequency",
        "id_after": "primary_keys",
    },
)

PRIMARY_KEYS_FIELD = Field(
    title="primary_keys",
    user_input_hint=["<primeira coluna>"],
    description=to_line(
        [
            "Quais colunas identificam uma linha unicamente?",
            "Preencha com os nomes de colunas. Ex: id_municipio, ano.",
            "Pode ser vazio pois certas tabelas não possuem identificadores.",
        ]
    ),
    yaml_order={
        "id_before": "observation_level",
        "id_after": "spatial_coverage",
    },
)

SPATIAL_COVERAGE_FIELD = Field(
    title="spatial_coverage",
    user_input_hint=[
        "<admin0 - pais>",
        "<admin1 - estados/regioes/etc>",
        "<admin2 - municipios/counties/etc>",
        "<admin3 - distritos/subdistritos/etc>",
    ],
    description=to_line(
        [
            "Qual é a cobertura espacial da tabela?",
            "Regras:",
            "  - minúsculo, sem acento, singular",
            "  - descer até o menor nível administrativo cuja cobertura abaixo seja 'todos'",
            "Exemplo 1: tabela que cubra todos os municípios nos estados de SP e GO",
            "  - brasil",
            "  - SP, GO",
            "Exemplo 2: tabela que cubra países inteiros na América Latina",
            "  - brasil, argentina, peru, equador",
        ]
    ),
    yaml_order={
        "id_before": "primary_keys",
        "id_after": "temporal_coverage",
    },
)

TEMPORAL_COVERAGE_FIELD = Field(
    title="temporal_coverage",
    user_input_hint=["<ano 1>", "<ano 2>"],
    description=to_line(
        [
            "Qual é a cobertura temporal (em anos) da tabela?",
            "Opções: ..., 1990, 1991, ..., 1999, 2000, 2001, ..., 2019, 2020, ...",
        ]
    ),
    yaml_order={
        "id_before": "spatial_coverage",
        "id_after": "partitions",
    },
)
PARTITIONS_FIELD = Field(
    title="partitions",
    user_input_hint=["<primeira partição>"],
    description=to_line(
        [
            "Liste as colunas da tabela que representam partições.",
            "Não esqueça de deletar essas colunas nas tabelas .csv na hora de subir para o BigQuery.",
            "Isso poupará muito tempo e dinheiro às pessoas utilizando essa tabela.",
            "Se não houver partições, não modifique abaixo.",
        ]
    ),
    yaml_order={
        "id_before": "temporal_coverage",
        "id_after": "None",
    },
)
