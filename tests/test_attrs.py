import pprint
from dataclasses import dataclass, astuple, asdict
from typing import List, Tuple

import attr
from attr import attrs
# -- attr
from singleton_decorator import singleton


@attr.s
class Simple:
    pass


@attrs(auto_attribs=True, frozen=True)  # 'attrs' as alias for 'attr.s'
class Coord:
    x: int
    y: int = 0  # default value


def test_simple():
    s = Simple()
    s2 = Simple()
    assert s == s2
    assert s is not s2


def test_coord():
    c = Coord(1, 2)
    c2 = Coord(x=1, y=2)
    assert c == c2

    # c.x = 2 # not possible because of frozen = True


def test_as_tuple():
    c = Coord(1, 2)
    assert attr.astuple(c) == (1, 2)


def test_as_dict():
    c = Coord(1, 2)
    assert attr.asdict(c) == {"x": 1, "y": 2}


# -- dataclass


@dataclass
class SimpleDC:
    pass


def test_simple_dc():
    s = SimpleDC()
    s2 = SimpleDC()
    assert s == s2
    assert s is not s2


@dataclass(frozen=True)
class CoordDC:
    x: int = 0
    y: int = 1


def test_coord_dc():
    c = CoordDC(1, 2)
    c2 = CoordDC(x=1, y=2)
    assert c == c2

    # c.x = 2 # not possible because of frozen = True
    print(c)  # provides '__repr__'


def test_as_tuple_dc():
    c = CoordDC(1, 2)
    assert astuple(c) == (1, 2)


def test_as_dict_dc():
    c = CoordDC(1, 2)
    assert asdict(c) == {"x": 1, "y": 2}


# --


class Step:
    _id: str

    def __init__(self, id):
        self._id = id


class Script:
    _id: str
    _steps: List[Step] = []

    def __init__(self, id):
        self._id = id

    def add_step(self, step: Step):
        self._steps.append(step)


@dataclass(frozen=True)
class Project(list):
    name: str
    rel: str
    tested_sw: Tuple[str]


@singleton
class Projects(list):
    pass


def test_projects():
    Projects().append(Project(name="aaa", rel="1.0", tested_sw=("jar1",)))
    Projects().append(Project(name="bbb", rel="2.0", tested_sw=("jar2",)))
    Projects().append(Project(name="ccc", rel="3.0", tested_sw=("jar3",)))

    print("\n" + pprint.pformat(Projects()))

    p2 = Project(name="xyz", rel="0.1", tested_sw=("jar0.1",))
    p2.append(Script(id="1"))
    p2.append(Script(id="2"))
    p2.append(Script(id="3"))

    pass
