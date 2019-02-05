import pytest  # type: ignore

from cnab import CNABDirectory
from cnab.invocation_image import InvalidCNABDirectoryError


class SampleCNAB(object):
    @pytest.fixture
    def directory(self):
        return CNABDirectory("fixtures/invocationimage")


class TestCNABDirectory(SampleCNAB):
    def test_has_app_dir(self, directory):
        assert directory.has_app_directory()

    def test_has_cnab_dir(self, directory):
        assert directory.has_cnab_directory()

    def test_has_readme(self, directory):
        assert isinstance(directory.readme(), str)

    def test_has_license(self, directory):
        assert isinstance(directory.license(), str)

    def test_has_no_misc_files(self, directory):
        assert directory.has_no_misc_files_in_cnab_dir()

    def test_has_run(self, directory):
        assert directory.has_run()

    def test_has_executable(self, directory):
        assert directory.has_executable_run()

    def test_is_valid(self, directory):
        assert directory.valid()


class InvalidCNAB(object):
    @pytest.fixture
    def directory(self):
        return CNABDirectory("fixtures/invalidinvocationimage")


class TestInvalidCNABDirectory(InvalidCNAB):
    def test_has_no_app_dir(self, directory):
        assert not directory.has_app_directory()

    def test_has_cnab_dir(self, directory):
        assert directory.has_cnab_directory()

    def test_has_readme(self, directory):
        assert isinstance(directory.readme(), str)

    def test_has_no_license(self, directory):
        assert not directory.license()

    def test_has_invalid_misc_files(self, directory):
        assert not directory.has_no_misc_files_in_cnab_dir()

    def test_has_no_run(self, directory):
        assert not directory.has_run()

    def test_has_no_executable(self, directory):
        assert not directory.has_executable_run()

    def test_is_invalid(self, directory):
        with pytest.raises(InvalidCNABDirectoryError):
            directory.valid()
