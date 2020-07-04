import operator
from functools import reduce

import pytest
import yaml
from jsonschema import ValidationError, SchemaError, Draft7Validator, validators


def load_yaml_file(path: str) -> dict:
    with open(path, "r") as file:
        return yaml.safe_load(file)


@pytest.fixture()
def schema() -> dict:
    return load_yaml_file("../syntax/schema.yml")


@pytest.fixture()
def instance() -> dict:
    return load_yaml_file("../syntax/scenario.yml")


def property_order(validator, value, instance, schema):
    instance_properties = [p for p in instance.keys() if p in schema["propertyOrder"]]
    schema_properties = [p for p in schema["propertyOrder"] if p in instance.keys()]
    if instance_properties != schema_properties:
        raise ValidationError(
            message=f"wrong property order: actual={instance_properties}, expected={schema_properties}"
        )


def create_validator(schema: dict) -> Draft7Validator:
    _validators = Draft7Validator.VALIDATORS
    _validators["propertyOrder"] = property_order
    extended_validator: Draft7Validator = validators.create(
        meta_schema=Draft7Validator.META_SCHEMA, validators=_validators
    )
    return extended_validator(schema=schema)


def validate(instance: dict, schema: dict):
    validator_: Draft7Validator = create_validator(schema=schema)
    validator_.validate(instance=instance)


@pytest.mark.parametrize(
    "keys, value",
    [
        [["steps", "#1 test step", "input", "param", "assign"], ""],
        [["steps", "#1 test step", "input", "param", "assign"], True],
        [["steps", "#1 test step", "input", "param", "assign"], 1],
        [["steps", "#1 test step", "input", "param", "assign"], 1.0],
        [["steps", "#1 test step", "input", "param", "assign"], []],
        [["steps", "#1 test step", "input", "param", "assign"], ["a", "b", "c"]],
        [["steps", "#1 test step", "output", "string", "equal"], True],
        [["steps", "#1 test step", "output", "string", "equal"], 1],
        [["steps", "#1 test step", "output", "string", "equal"], 1.0],
        [["steps", "#1 test step", "output", "string", "equal"], []],
    ],
)
def test_validation_value_type_ok(schema, instance, keys, value):
    reduce(operator.getitem, keys[:-1], instance)[keys[-1]] = value
    assert reduce(operator.getitem, keys, instance) == value
    try:
        validate(instance=instance, schema=schema)
    except ValidationError as error:
        print(f">> validation error: {error.message}")
        # raise
    except SchemaError as error:
        print(f">> schema error: {error.message}")
        # raise


@pytest.mark.parametrize(
    "keys, value",
    [
        [["steps", "#1 test step", "input", "id", "env"], True],
        [["steps", "#1 test step", "input", "id", "env"], 1],
        [["steps", "#1 test step", "input", "id", "env"], 1.0],
        [["steps", "#1 test step", "input", "id", "env"], []],
        [["steps", "#1 test step", "input", "id", "env"], {}],
    ],
)
def test_validation_value_type_fail(schema, instance, keys, value):
    reduce(operator.getitem, keys[:-1], instance)[keys[-1]] = value
    assert reduce(operator.getitem, keys, instance) == value
    with pytest.raises(ValidationError):
        validate(instance=instance, schema=schema)
