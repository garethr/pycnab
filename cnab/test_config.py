import json

from cnab import Bundle, InvocationImage


def test_create_bundle():
    bundle = Bundle(
        name="sample",
        version="0.1.0",
        invocation_images=[
            InvocationImage(image_type="docker", image="garethr/helloworld:0.1.0")
        ],
    )
    assert bundle.to_dict()


def test_read_bundle():
    with open("bundle.json") as f:
        data = json.load(f)

    assert Bundle.from_dict(data)
