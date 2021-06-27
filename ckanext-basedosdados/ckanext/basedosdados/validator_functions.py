# Documentation on: https://docs.ckan.org/en/2.9/extensions/adding-custom-fields.html?highlight=validators#custom-validators

from ckantoolkit import missing as MISSING

# TODO: check if this file is still relevant
def _get_type(key, data):
    k = list(key)
    k[-1] = "resource_type"
    type_ = data.get(tuple(k))
    SUPPORTED_TYPES = ("bdm_table", "external_link")
    if type_ not in SUPPORTED_TYPES:
        return None
        # raise Exception( f'Resource Type invalid! Found {type_!r}, but we only accept types: {SUPPORTED_TYPES!r}\n{locals()}')
    return type_


def required_on_types(*types):
    def validator(key, data, errors, con):
        type_ = _get_type(key, data)
        if type_ == None:
            errors[key].append(f"resource_type not supported.")
            return
        has_data = data[key] != MISSING and data[key]
        if type_ in types and not has_data:
            errors[key].append(f"Field required for {type_} resources")

    return validator


def only_on_types(*types):
    def validator(key, data, errors, con):
        type_ = _get_type(key, data)
        if type_ == None:
            errors[key].append(f"resource_type not supported.")
            return
        has_data = data[key] != MISSING and data[key]
        if type_ not in types and has_data:
            errors[key].append(
                f"Field only available for {types} resources. This resource is of type {type_}"
            )

    return validator

def string_validator(value):
    if type(value) == str:
        return value
            
def not_missing(value):
    if value is not None:
        return value
    else:
        value=""
        return value
