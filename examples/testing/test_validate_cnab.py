"""
This pytest set of tests is designed to validate uses of CNAB, both bundle.json
metadata files and the file system layout for invocation images.

The tests below will automatically generate individual unit tests along various axis:

    - for every schema in the schemas directory
    - for every bundle.json file found in decendent directories
    - for every cnab directory found in decendent directories

"""

import json
import glob
import os
import shutil
from urllib.request import urlopen

from jsonschema import validate
import pytest

from cnab import Bundle, CNABDirectory

# If we don't already have a schemas directory from a previous run or extra schemas then create one
if not os.path.exists('schemas'):
    os.makedirs('schemas')

# We grab the latest version of the schema from the spec repository whenever the tests are run
URL = "https://raw.githubusercontent.com/deislabs/cnab-spec/master/schema/bundle.schema.json"
with urlopen(URL) as response, open("schemas/latest.json", 'wb') as out_file:
    shutil.copyfileobj(response, out_file)

@pytest.fixture(scope="module", params=glob.glob("schemas/*.json"))
def schema(request):
    "This fixture will pick up multiple schemas if present"
    with open(request.param) as schema_data:
        return json.load(schema_data)


@pytest.mark.parametrize("path", glob.glob("**/bundle.json"))
def test_valid_bundles(path):
    "Test that any bundle.json files present are valid according to pycnab"
    with open(path) as data:
        Bundle.from_dict(json.load(data))


@pytest.mark.parametrize("path", glob.glob("**/bundle.json"))
def test_valid_jsonschema(schema, path):
    "Test that any bundle.json files present are valid according to the JSON Schema"
    with open(path) as data:
        validate(json.load(data), schema)


@pytest.mark.parametrize("path", glob.glob("**/cnab"))
def test_valid_invocation_image(path):
    "Test that CNAB build directories for adherence to the spec"
    head, tail = os.path.split(path)
    directory = CNABDirectory(head)
    directory.valid()
