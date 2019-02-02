import pytest  # type: ignore

from cnab import CNAB, Bundle, InvocationImage


class HelloWorld(object):
    @pytest.fixture
    def app(self):
        return CNAB("fixtures/helloworld/bundle.json")


class TestHelloWorld(HelloWorld):
    @pytest.mark.parametrize("action", ["install", "upgrade", "uninstall"])
    def test_actions_present(self, app, action):
        assert action in app.actions

    def test_credentials_empty(self, app):
        assert app.credentials == None

    def test_port_parameter_present(self, app):
        assert "port" in app.parameters

    def test_port_details(self, app):
        assert app.parameters["port"].type == "int"
        assert app.parameters["port"].default_value == 8080

    def test_app_name(self, app):
        assert app.name == "helloworld"

    def test_version(self, app):
        assert app.bundle.version == "0.1.1"

    def test_app_bundle(self, app):
        assert isinstance(app.bundle, Bundle)

    def test_invocation_images(self, app):
        assert len(app.bundle.invocation_images) == 1


@pytest.mark.docker
class TestIntegrationHelloWorld(HelloWorld):
    @pytest.fixture
    def install(self, app):
        return str(app.run("install", parameters={"port": 9090}))

    def test_run(self, install):
        assert "install" in install


class TestHelloHelm(object):
    @pytest.fixture
    def app(self):
        return CNAB("fixtures/hellohelm/bundle.json")

    @pytest.mark.parametrize("action", ["install", "upgrade", "uninstall", "status"])
    def test_actions_present(self, app, action):
        assert action in app.actions


def test_app_from_dict():
    bundle = {
        "name": "helloworld",
        "version": "0.1.1",
        "invocationImages": [
            {"imageType": "docker", "image": "cnab/helloworld:latest"}
        ],
        "images": {},
        "parameters": {
            "port": {
                "defaultValue": 8080,
                "type": "int",
                "destination": {"env": "PORT"},
                "metadata": {"descriptiob": "the public port"},
            }
        },
        "maintainers": [
            {"email": "test@example.com", "name": "test", "url": "example.com"}
        ],
    }
    assert CNAB(bundle)


def test_app_from_bundle():
    bundle = Bundle(
        name="sample",
        version="0.1.0",
        invocation_images=[
            InvocationImage(image_type="docker", image="garethr/helloworld:0.1.0")
        ],
    )
    assert CNAB(bundle)


def test_app_from_invalid_input():
    with pytest.raises(TypeError):
        CNAB(1)
