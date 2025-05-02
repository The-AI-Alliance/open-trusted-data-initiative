import os

from data_processing.test_support.launch.transform_test import (
    AbstractTransformLauncherTest,
)
from data_processing.runtime.ray import RayTransformLauncher
from license_validator.python import (
    default_license_column,
    license_content_column_cli_param,
)
from license_validator.ray import LicenseValidatorRayTransformConfiguration


class TestRayLicenseValidatorTransform(AbstractTransformLauncherTest):
    """
    Extends the super-class to define the test data for the tests defined there.
    The name of this class MUST begin with the word Test so that pytest recognizes it as a test class.
    """

    def get_test_transform_fixtures(self) -> list[tuple]:
        src_file_dir = os.path.abspath(os.path.dirname(__file__))
        fixtures = []

        launcher = RayTransformLauncher(LicenseValidatorRayTransformConfiguration())
        basedir = os.path.join(src_file_dir, "../../test-data")
        transform_config = {
            "run_locally": True,
            license_content_column_cli_param: default_license_column,
        }
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