import pytest
from playwright.sync_api import Page


# poetry add playwright pytest-playwright
# poetry run python -m playwright install
# poetry add python-slugify


def test_visit_page(page: Page):
    page.goto("http://bvbb-ev.de")
    assert page.innerText("h3") == "Aktuelles"


@pytest.mark.skip_browser("chromium")
def test_skip_browser(page: Page):
    page.goto("http://bvbb-ev.de")
    assert page.innerText("h3") == "Aktuelles"


@pytest.mark.only_browser("firefox")
def test_mark_only_browser(page: Page):
    page.goto("http://bvbb-ev.de")
    assert page.innerText("h3") == "Aktuelles"


def test_breakpoint(page: Page):
    page.goto("http://bvbb-ev.de")
    breakpoint()
    assert page.innerText("h3") == "Aktuelles"
