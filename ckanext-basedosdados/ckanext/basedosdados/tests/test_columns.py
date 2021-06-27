from ckanext.basedosdados.validator.package import Package, ValidationError
import jsonschema

import pytest
from pytest import raises


@pytest.fixture()
def data():
    DATE = "1990-01-01T00:00:00"
    return {
        "id": "123",
        "name": "123",
        "title": "123",
        "type": "dataset",
        "state": "active",
        "private": False,
        "metadata_created": DATE,
        "metadata_modified": DATE,
        "num_resources": 1,
        "num_tags": 1,
        "resources": [{}],
        "temporal_coverage": [2020],
        "creator_user_id": "123e4567-e89b-12d3-a456-426614174000",
        "owner_org": "123e4567-e89b-12d3-a456-426614174000",
    }


def test_column_validation_ok(data):
    