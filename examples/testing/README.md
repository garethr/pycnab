# Testing for valid CNAB bundles

The following demonstrates usage of `pycnab`, by building a set of tests to validate CNAB bundles.


## Usage

Dependencies are managed using [Pipenv](https://pipenv.readthedocs.io/en/latest/).

```console
pipenv sync
```

With the dependencies installed you should be able to simply run `pytest` and have it detect the tests. This with sample data you should get something like the following output.

```console
$ pytest
collected 3 items

test_validate.py::test_valid_bundles[helloworld/bundle.json] PASSED
test_validate.py::test_valid_jsonschema[schemas/latest.json-helloworld/bundle.json] PASSED
test_validate.py::test_valid_invocation_image[helloworld/cnab] PASSED
```

You can drop your own schemas in the `schemas` directory, and any directories containing `cnab` directories or `bundle.json` files will be checked for correctness.


### Docker

If you prefer to keep your environment clean you can run using Docker, using the Dockerfile provided.

```console
$ docker build .
Sending build context to Docker daemon  2.331MB
Step 1/3 : FROM kennethreitz/pipenv
# Executing 3 build triggers
 ---> Using cache
 ---> Using cache
 ---> Using cache
 ---> 7c4d92001455
Step 2/3 : COPY . /app
 ---> 7a0045b96aab
Step 3/3 : RUN pytest
 ---> Running in 61ab93743ba2
============================= test session starts ==============================
platform linux -- Python 3.7.1, pytest-4.2.0, py-1.7.0, pluggy-0.8.1 -- /usr/bin/python3.7
cachedir: .pytest_cache
rootdir: /app, inifile: pytest.ini
collecting ... collected 3 items

test_validate.py::test_valid_bundles[helloworld/bundle.json] PASSED      [ 33%]
test_validate.py::test_valid_jsonschema[schemas/latest.json-helloworld/bundle.json] PASSED [ 66%]
test_validate.py::test_valid_invocation_image[helloworld/cnab] PASSED    [100%]

=========================== 3 passed in 0.31 seconds ===========================
Removing intermediate container 61ab93743ba2
 ---> 6a50483b8550
Successfully built 6a50483b8550
```


## Failures

[CNAB](https://cnab.io/) is still new, and the specification is changing rapidly. The JSON Schema also has bugs that are being worked out.
`pycnab` is also new, and bugs will exist in there too. Using this test suite should be a useful way of working out those issues, so please report
any suspect failures.
