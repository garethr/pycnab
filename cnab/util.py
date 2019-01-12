from typing import List

from cnab.types import InvocationImage


def extract_docker_images(images: List[InvocationImage]) -> list:
    return list(filter(lambda x: x.image_type == "docker", images))
