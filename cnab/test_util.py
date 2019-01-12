import pytest  # type: ignore

import cnab.util
from cnab import InvocationImage


class TestExtractImages(object):
    @pytest.fixture
    def filtered(self):
        images = [
            InvocationImage(image="oci"),
            InvocationImage(image="docker", image_type="docker"),
        ]
        return cnab.util.extract_docker_images(images)

    def test_filtered_images(self, filtered):
        assert len(filtered) == 1

    def test_extract_docker_images(self, filtered):
        assert filtered[0].image == "docker"
