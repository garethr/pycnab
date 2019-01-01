from typing import Union
import json

from cnab.config import Bundle, Action


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

    def run(self, action, **parameters):
        import docker

        client = docker.from_env()
        docker_images = list(
            filter(lambda x: x.image_type == "docker", self.bundle.invocation_images)
        )
        assert len(docker_images) == 1

        env = {
            "CNAB_INSTALLATION_NAME": self.name,
            "CNAB_BUNDLE_NAME": self.bundle.name,
            "CNAB_ACTION": action,
        }

        # check if action is supported
        assert action in self.actions()

        # check if parameters passed in are in bundle parameters

        errors = []
        for key in parameters:
            if key not in self.bundle.parameters:
                errors.append(f"Invalid parameter provided: {key}")

        assert len(errors) == 0

        # check if required parameters have been passed in

        # validate passed in params

        # build environment hash
        for param in self.bundle.parameters:
            parameter = self.bundle.parameters[param]
            key = parameter.destination or f"CNAB_P_{param.upper()}"
            value = (
                parameters[param] if param in parameters else parameter.default_value
            )
            env[key] = value

        return client.containers.run(
            docker_images[0].image, auto_remove=False, remove=True, environment=env
        )

    def actions(self) -> list:
        actions = {
            "install": Action(modifies=True),
            "uninstall": Action(modifies=True),
            "upgrade": Action(modifies=True),
        }
        if self.bundle.actions:
            actions.update(self.bundle.actions)
        return actions

    def parameters(self) -> dict:
        return self.bundle.parameters