import json
from json import JSONDecodeError

import pytest
from jinja2 import Template, FileSystemLoader, Environment


def test_json_template():
    json_template: str = '{"any": "{{ bar }}"}'
    data: dict = {"bar": "Something!"}
    template: Template = Template(json_template)
    json_result: str = template.render(data)
    assert json.loads(json_result) == {"any": "Something!"}


def test_json_template_with_nested_data():
    json_template: str = '{"any": "{{ nested.level }}"}'
    data: dict = {"nested": {"level": "Nested level!"}}
    template: Template = Template(json_template)
    json_result: str = template.render(data)
    assert json.loads(json_result) == {"any": "Nested level!"}


def test_load_templates_from_file():
    file_loader = FileSystemLoader("template")
    env = Environment(loader=file_loader)
    template: Template = env.get_template("simple.json")
    data: dict = {"bar": "Something!"}
    json_result: str = template.render(data)
    assert json.loads(json_result) == {"any": "Something!"}


def test_loop():
    file_loader = FileSystemLoader("template")
    env = Environment(loader=file_loader)
    template: Template = env.get_template("loop.json")
    data: dict = {"colors": ["red", "green", "blue"]}
    json_result: str = template.render(data)
    # assert json.loads(json_result) == {"farben": ["red", "green", "blue"]}
    with pytest.raises(JSONDecodeError):  # because of last comma in ["red", "green", "blue",]
        json.loads(json_result)
