# Python CNAB Library

_Work-in-progress_ library for working with [CNAB](https://cnab.io/) in Python.

There are probably three main areas of interest for a CNAB client:

1. Creation/parsing of the `bundle.json` format
2. Building invocation images
3. Running actions against a CNAB

At this early stage only the first of these is currently work-in-progress.

## Parsing `bundle.json`

Nothing too fancy here, the `Bundle` class  has a `from_dict` static method which
builds a full `Bundle` object.

```python
import json
from cnab import Bundle

with open("bundle.json") as f:
    data = json.load(f)

bundle = Bundle.from_dict(data)
```

This could for example be used for validation purposes, or for building user interfaces for `bundle.json` files.


## Describing `bundle.json` in Python 

You can also describe the `bundle.json` file in Python. This will correctly validate the
structure based on the current specification and would allow for building a custom DSL or other
user interface for generating `bundle.json` files.

```python
import json
from cnab import Bundle, InvocationImage

bundle = Bundle(
    name="hello",
    version="0.1.0",
    invocation_images=[
        InvocationImage(
            image_type="docker",
            image="technosophos/helloworld:0.1.0",
            digest="sha256:aaaaaaa...",
        )
    ],
)

print(json.dumps(bundle.to_dict(), indent=4))
```


## Thanks

Thanks to [QuickType](https://quicktype.io/) for bootstrapping the creation of the Python code for manipulating `bundle.json` based on the current JSON Schema.

