import os
from pathlib import Path
from typing import Optional, Dict

import yaml


class EnvTag(yaml.YAMLObject):
    @classmethod
    def from_yaml(cls, loader, node):
        if not isinstance(node, yaml.ScalarNode):
            raise EnvironmentError(f"'{node.tag}' tag must have a scalar value")
        if not os.environ.get(node.value):
            raise EnvironmentError(f"environment variable '{node.value}' not found")
        return os.environ.get(node.value)


def load_yaml_file(path: Path) -> Optional[Dict]:
    yaml.SafeLoader.add_constructor("!env", EnvTag.from_yaml)
    with open(str(path), "r") as stream:
        data = yaml.safe_load(stream)
        return data


def test_yaml():
    data = load_yaml_file(Path("file.yaml"))
