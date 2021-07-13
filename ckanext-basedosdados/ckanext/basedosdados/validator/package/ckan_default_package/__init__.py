from pydantic import ValidationError
import pydantic


class BaseModel(pydantic.BaseModel):
    class Config:
        extra = "allow"


def treat_scalar_as_single_value_set(*fields):
# We need this as ckan coerses single value list as scalars 🤦
# from:
  # ckan/views/resource.py:185
  # ckan/logic/__init__.py:150
    return pydantic.validator(*fields, pre=True, allow_reuse=True)(_treat_scalar_as_single_value_set)

def _treat_scalar_as_single_value_set(cls, value):
    from collections.abc import Iterable
    if value is None: return None
    if isinstance(value, str): return set([value])
    if isinstance(value, Iterable): return set(value)
    return value



from . import package, resource
