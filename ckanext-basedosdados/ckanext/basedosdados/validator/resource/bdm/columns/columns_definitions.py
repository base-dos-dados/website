from pydantic import Field

from ckanext.basedosdados.validator.ckan_default import BaseModel

to_line = lambda description: "\n".join(description)


COLUMNS_FIELD = Field(
    title="columns",
    description=to_line(
        [
            "Quais são as colunas? Certifique-se de escrever uma boa descrição, as pessoas vão gostar",
            "para saber sobre o que é a coluna.",
            "Adicionar todas as colunas manualmente pode ser bastante cansativo, por isso, quando",
            "inicializando este arquivo de configuração, você pode apontar a função para uma amostra de dados que",
            "preencherá automaticamente as colunas.",
            "Algumas colunas existirão apenas na tabela final, você as construirá em `publish.sql`.",
            "Para esses, defina is_in_staging como False.",
            "Além disso, você deve adicionar as colunas de partição aqui e definir is_partition como True.",
        ]
    ),
)


NAME_FIELD = Field(
    title="columns-name",
    user_input_hint=["<primeira_coluna>"],
    description=to_line(
        [
            "nome da coluna",
        ]
    ),
)

DESCRIPTION_FIELD = Field(
    title="columns-description",
    user_input_hint=["<descrição>"],
    description=to_line(
        [
            "descrição da coluna",
        ]
    ),
)

IS_IN_STAGING_FIELD = Field(
    title="columns-is_in_staging",
    user_input_hint=["<True/False>"],
    description=to_line(
        [
            "Bool [True, False], se a coluna está na tabela staging",
        ]
    ),
)

IS_PARTITION_FIELD = Field(
    title="columns-is_partition",
    user_input_hint=["<True/False>"],
    description=to_line(
        [
            "Bool [True, False], se a coluna é uma partição.",
        ]
    ),
)
