import pytest

from meeting.app import create_app


@pytest.fixture(scope="module")
def app():
    return create_app()
