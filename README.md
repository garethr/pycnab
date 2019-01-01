# Python CNAB Library

_Work-in-progress_ library for working with [CNAB](https://cnab.io/) in Python.

There are probably three main areas of interest for a CNAB client:

1. Creation/parsing of the `bundle.json` format
2. Building invocation images
3. Running actions against a CNAB

At this early stage only the first and third of these are currently work-in-progress.


## Installation

The module is published on [PyPi](https://pypi.org/project/cnab/) and can be installed from there.

```bash
pip install cnab
```


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

## Running CNABs

The module supports running actions on a CNAB, using the `docker` driver.

```python
from cnab import CNAB

# The first argument can be a path to a bundle.json file, a dictionary
# or a full `Bundle` object
app = CNAB("bundle.json")

# list available actions
print(app.actions())

# list available parameters
print(app.parameters())

# run the install action
print(app.run("install"))

# run the install action specifying a parameters
print(app.run("install", port=9090))
```

Error handling for this is very work-in-progress, and this doesn't yet handle credentials at all.


## Thanks

Thanks to [QuickType](https://quicktype.io/) for bootstrapping the creation of the Python code for manipulating `bundle.json` based on the current JSON Schema.

