import json
import tempfile
from typing import Union

from cnab.types import Bundle, Action
from cnab.util import extract_docker_images


class CNAB:
    bundle: Bundle
    name: str

    def __init__(self, bundle: Union[Bundle, dict, str], name: str = None):
        if isinstance(bundle, Bundle):
            self.bundle = bundle
        elif isinstance(bundle, dict):
            self.bundle = Bundle.from_dict(bundle)
        elif isinstance(bundle, str):
            with open(bundle) as f:
                data = json.load(f)
            self.bundle = Bundle.from_dict(data)
        else:
            raise TypeError

        self.name = name or self.bundle.name

    def run(self, action: str, credentials: dict = {}, parameters: dict = {}):
        import docker  # type: ignore

        # check if action is supported
        assert action in self.actions

        client = docker.from_env()
        docker_images = extract_docker_images(self.bundle.invocation_images)
        assert len(docker_images) == 1

        # check if parameters passed in are in bundle parameters
        errors = []
        for key in parameters:
            if key not in self.bundle.parameters:
                errors.append(f"Invalid parameter provided: {key}")
        assert len(errors) == 0

        # check if required parameters have been passed in
        required = []
        for param in self.bundle.parameters:
            parameter = self.bundle.parameters[param]
            if parameter.required:
                required.append(param)

        for param in required:
            assert param in parameters

        # validate passed in params
        for param in parameters:
            parameter = self.bundle.parameters[param]
            if parameter.allowed_values:
                assert param in parameter.allowed_values
            if isinstance(param, int):
                if parameter.max_value:
                    assert param <= parameter.max_value
                if parameter.min_value:
                    assert param >= parameter.min_value
            elif isinstance(param, str):
                if parameter.max_length:
                    assert len(param) <= parameter.max_length
                if parameter.min_length:
                    assert len(param) >= parameter.min_length

        env = {
            "CNAB_INSTALLATION_NAME": self.name,
            "CNAB_BUNDLE_NAME": self.bundle.name,
            "CNAB_ACTION": action,
        }

        # build environment hash
        for param in self.bundle.parameters:
            parameter = self.bundle.parameters[param]
            if parameter.destination:
                if parameter.destination.env:
                    key = parameter.destination.env
                    value = (
                        parameters[param]
                        if param in parameters
                        else parameter.default_value
                    )
                    env[key] = value
                if parameter.destination.path:
                    # not yet supported
                    pass

        mounts = []
        if self.bundle.credentials:
            for name in self.bundle.credentials:
                # check credential has been provided
                assert name in credentials

                credential = self.bundle.credentials[name]
                if credential.env:
                    # discussing behavour in https://github.com/deislabs/cnab-spec/issues/69
                    assert credential.env[:5] != "CNAB_"
                    env[credential.env] = credentials[name]

                if credential.path:
                    tmp = tempfile.NamedTemporaryFile(mode="w+", delete=True)
                    tmp.write(credentials[name])
                    tmp.flush()
                    mounts.append(
                        docker.types.Mount(
                            target=credential.path,
                            source=tmp.name,
                            read_only=True,
                            type="bind",
                        )
                    )

        # Mount image maps for runtime usage
        tmp = tempfile.NamedTemporaryFile(mode="w+", delete=True)
        tmp.write(json.dumps(self.bundle.images))
        tmp.flush()
        mounts.append(
            docker.types.Mount(
                target="/cnab/app/image-map.json",
                source=tmp.name,
                read_only=True,
                type="bind",
            )
        )

        return client.containers.run(
            docker_images[0].image,
            "/cnab/app/run",
            auto_remove=False,
            remove=True,
            environment=env,
            mounts=mounts,
        )

    @property
    def actions(self) -> dict:
        actions = {
            "install": Action(modifies=True),
            "uninstall": Action(modifies=True),
            "upgrade": Action(modifies=True),
        }
        if self.bundle.actions:
            actions.update(self.bundle.actions)
        return actions

    @property
    def parameters(self) -> dict:
        return self.bundle.parameters

    @property
    def credentials(self) -> dict:
        return self.bundle.credentials
