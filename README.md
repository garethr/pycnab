# Python CNAB Library

_Work-in-progress_ library for working with [CNAB](https://cnab.io/) in Python.

There are probably three main areas of interest for a CNAB client:

1. Handling the `bundle.json` format ([101](https://github.com/deislabs/cnab-spec/blob/master/101-bundle-json.md))
2. Building invocation images ([102](https://github.com/deislabs/cnab-spec/blob/master/102-invocation-image.md))
3. Running actions against a CNAB ([103](https://github.com/deislabs/cnab-spec/blob/master/103-bundle-runtime.md))

Claims and Signing are optional but will be worked on once the above are stable.


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

print(bundle.to_json())
```

## Running CNABs

The module supports running actions on a CNAB, using the `docker` driver.

```python
from cnab import CNAB

# The first argument can be a path to a bundle.json file, a dictionary
# or a full `Bundle` object
app = CNAB("fixtures/helloworld/bundle.json")

# list available actions
print(app.actions)

# list available parameters
print(app.parameter)

# run the install action
print(app.run("install"))

# run the install action specifying a parameters
print(app.run("install", parameters={"port": 9090}))

# Many applications will require credentials
app = CNAB("fixtures/hellohelm/bundle.json")

# list required credentials
print(app.credentials)

# Here we pass the value for the required credential
# in this case by reading the existing configuration from disk
with open("/home/garethr/.kube/config") as f:
    print(app.run("status", credentials={"kubeconfig": f.read()}))
```

Note that error handling for this is very work-in-progress.


## Working with invocation images

`pycnab` also has a class for working with invocation images.

```python
from cnab import CNABDirectory

directory = CNABDirectory("fixtures/invocationimage")

# Check whether the directory is valid
# Raises `InvalidCNABDirectory` exception if invalid
directory.valid()

# Returns the text of the associated README file if present
directory.readme()

# Returns the text of the associated LICENSE file if present
directory.license()
```


## Thanks

Thanks to [QuickType](https://quicktype.io/) for bootstrapping the creation of the Python code for manipulating `bundle.json` based on the current JSON Schema.

