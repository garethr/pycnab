import os
from typing import Union, List


class InvalidCNABDirectoryError(Exception):
    pass


class CNABDirectory(object):
    path: str

    def __init__(self, path: str):
        self.path = path

    def has_cnab_directory(self) -> bool:
        cnab = os.path.join(self.path, "cnab")
        return os.path.isdir(cnab)

    def has_app_directory(self) -> bool:
        app = os.path.join(self.path, "cnab", "app")
        return os.path.isdir(app)

    def has_no_misc_files_in_cnab_dir(self) -> bool:
        cnab = os.path.join(self.path, "cnab")
        disallowed_dirs: List[str] = []
        disallowed_files: List[str] = []
        for root, dirs, files in os.walk(cnab):
            disallowed_dirs = [x for x in dirs if x not in ["app", "build"]]
            disallowed_files = [
                x for x in files if x not in ["LICENSE", "README.md", "README.txt"]
            ]
            break
        if disallowed_dirs or disallowed_files:
            return False
        else:
            return True

    def has_run(self) -> bool:
        run = os.path.join(self.path, "cnab", "app", "run")
        return os.path.isfile(run)

    def has_executable_run(self) -> bool:
        run = os.path.join(self.path, "cnab", "app", "run")
        return os.access(run, os.X_OK)

    def readme(self) -> Union[bool, str]:
        readme = os.path.join(self.path, "cnab", "README")
        txt = readme + ".txt"
        md = readme + ".md"
        if os.path.isfile(txt):
            with open(txt, "r") as content:
                return content.read()
        elif os.path.isfile(md):
            with open(md, "r") as content:
                return content.read()
        else:
            return False

    def license(self) -> Union[bool, str]:
        license = os.path.join(self.path, "cnab", "LICENSE")
        if os.path.isfile(license):
            with open(license, "r") as content:
                return content.read()
        else:
            return False

    def valid(self) -> bool:
        errors = []
        if not self.has_executable_run():
            errors.append("Run entrypoint is not executable")
        if not self.has_run():
            errors.append("Missing a run entrypoint")
        if not self.has_app_directory():
            errors.append("Missing the app directory")
        if not self.has_cnab_directory():
            errors.append("Missing the cnab directory")
        if not self.has_no_misc_files_in_cnab_dir():
            errors.append("Has additional files in the cnab directory")

        if len(errors) == 0:
            return True
        else:
            raise InvalidCNABDirectoryError(errors)
