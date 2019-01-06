import json

from cnab import Bundle, InvocationImage, Action, Credential, Parameter, Maintainer
import pytest  # type: ignore


class TestMinimalParameters(object):
    @pytest.fixture
    def bundle(self):
        return Bundle(
            name="sample",
            version="0.1.0",
            invocation_images=[
                InvocationImage(image_type="docker", image="garethr/helloworld:0.1.0")
            ],
        )

    def test_bundle_images_empty(self, bundle):
        assert bundle.images == []

    def test_bundle_parameters_empty(self, bundle):
        assert bundle.parameters == {}

    def test_bundle_credentials_empty(self, bundle):
        assert bundle.credentials == {}

    def test_bundle_default_schema_version(self, bundle):
        assert bundle.schema_version == "v1"

    def test_bundle_keywords_empty(self, bundle):
        assert bundle.keywords == []

    def test_bundle_actions_empty(self, bundle):
        assert bundle.actions == {}

    def test_bundle_maintainers_empty(self, bundle):
        assert bundle.maintainers == []

    def test_convert_bundle_to_dict(self, bundle):
        assert isinstance(bundle.to_dict(), dict)

    def test_bundle_description_blank(self, bundle):
        assert not bundle.description


def test_read_bundle():
    with open("fixtures/helloworld/bundle.json") as f:
        data = json.load(f)

    assert isinstance(Bundle.from_dict(data), Bundle)


class TestAllParameters(object):
    @pytest.fixture
    def bundle(self):
        return Bundle(
            name="sample",
            version="0.1.0",
            invocation_images=[
                InvocationImage(image_type="docker", image="garethr/helloworld:0.1.0")
            ],
            actions={
                "status": Action(modifies=False),
                "explode": Action(modifies=True),
            },
            parameters={},
            credentials={},
            description="test",
            keywords=["test1", "test2"],
            maintainers=[
                Maintainer(email="test@example.com", name="test", url="example.com")
            ],
            images=[],
            schema_version="v2",
        )

    def test_bundle_set_schema_version(self, bundle):
        assert bundle.schema_version == "v2"

    def test_bundle_set_description(self, bundle):
        assert bundle.description == "test"

    @pytest.mark.parametrize("keyword", ["test1", "test2"])
    def test_bundle_set_keywords(self, bundle, keyword):
        assert keyword in bundle.keywords

    @pytest.mark.parametrize("action", ["status", "explode"])
    def test_bundle_set_actions(self, bundle, action):
        assert action in bundle.actions

    def test_bundle_set_maintainer(self, bundle):
        assert len(bundle.maintainers) == 1

    def test_convert_bundle_to_dict(self, bundle):
        assert isinstance(bundle.to_dict(), dict)
