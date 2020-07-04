from pathlib import Path


def test_path_properties():
    path: Path = Path(__file__)
    parts = path.parts
    drive = path.drive
    root = path.root
    name = path.name
    suffix = path.suffix
    stem = path.stem
    parent = path.parent
    parents = path.parents
    anchor = path.anchor
    uri = path.as_uri()
    posix = path.as_posix()


def test_past_methods():
    home: Path = Path.home()
    cwd: Path = Path.cwd()


def test_relative_to():
    p1: Path = Path("/a/b/c")
    p2: Path = Path("/a")
    delta: Path = p1.relative_to(p2)
    assert delta == Path("b/c")
