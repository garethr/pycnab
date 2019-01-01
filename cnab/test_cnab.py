import pytest  # type: ignore

from cnab import CNAB, Bundle


@pytest.fixture
def app():
    return CNAB("fixtures/helloworld/bundle.json")


@pytest.mark.parametrize("action", ["install", "upgrade", "uninstall"])
def test_actions_present(app, action):
    assert action in app.actions()


def test_port_parameter_present(app):
    assert "port" in app.parameters()


def test_app_name(app):
    assert app.name == "helloworld"


def test_app_bundle(app):
    assert isinstance(app.bundle, Bundle)
