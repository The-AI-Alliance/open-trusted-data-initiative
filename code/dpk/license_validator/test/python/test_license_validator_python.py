import os

from data_processing.runtime.python import PythonTransformLauncher
from data_processing.test_support.launch.transform_test import (
    AbstractTransformLauncherTest,
)
from license_validator.python import (
    default_license_column,
    license_content_column_cli_param,
    LicenseValidatorPythonTransformRuntimeConfiguration,
)


class TestPythonLicenseValidatorTransform(AbstractTransformLauncherTest):
    """
    Extends the super-class to define the test data for the tests defined there.
    The name of this class MUST begin with the word Test so that pytest recognizes it as a test class.
    """

    def get_test_transform_fixtures(self) -> list[tuple]:
        src_file_dir = os.path.abspath(os.path.dirname(__file__))
        fixtures = []

        launcher = PythonTransformLauncher(
            LicenseValidatorPythonTransformRuntimeConfiguration()
        )
        basedir = os.path.join(src_file_dir, "../../test-data")
        transform_config = {license_content_column_cli_param: default_license_column}
        fixtures.append(
            (
                launcher,
                transform_config,
                basedir + "/input",
                basedir + "/expected",
                [],  # optional list of column names to ignore in comparing test-generated with expected.
            )
        )

        return fixtures
