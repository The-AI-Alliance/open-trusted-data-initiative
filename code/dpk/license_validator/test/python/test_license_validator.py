import pyarrow as pa
from data_processing.test_support.transform import AbstractTableTransformTest
from license_validator.python import (
    LicenseValidatorTransform,
    default_license_column,
    license_content_column_key,
)


table = pa.Table.from_pydict(
    mapping={default_license_column: pa.array(["odc-by", "apache-2.0", "apache-2.0"])}
)
expected_metadata_list = [
    {"license_apache-2.0": 2, "license_odc-by": 1},
    {},
]  # transform() result  # flush() result


class TestLicenseValidatorTransform(AbstractTableTransformTest):
    """
    Extends the super-class to define the test data for the tests defined there.
    The name of this class MUST begin with the word Test so that pytest recognizes it as a test class.
    """

    def get_test_transform_fixtures(self) -> list[tuple]:
        config = {license_content_column_key: default_license_column}
        fixtures = [
            (LicenseValidatorTransform(config), [table], [], expected_metadata_list),
        ]
        return fixtures