from pathlib import Path

from slugify import slugify


def pytest_runtest_makereport(item, call) -> None:
    if call.when == "call":
        if call.excinfo is not None:
            page = item.funcargs["page"]
            screenshot_dir = Path(".playwright-screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            page.screenshot(path=str(screenshot_dir / f"{slugify(item.nodeid)}.png"))
