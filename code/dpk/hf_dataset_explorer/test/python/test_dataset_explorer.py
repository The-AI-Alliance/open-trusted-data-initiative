from data_processing.data_access import DataAccessFactory
from data_processing.test_support.transform import AbstractBinaryTransformTest
from hf_dataset_explorer.python import DatasetExplorerTransform


input_data_factory = DataAccessFactory()
input_data_factory.apply_input_params(
    args={"data_hf_config": {"input_folder": "datasets/"}}
)
output_data_factory = DataAccessFactory()

data_access = input_data_factory.create_data_access()
f_name = "datasets/blublinsky/test/README.md"
data, _ = data_access.get_file(f_name)

expected_metadata_list = [
    {"license_apache-2.0": 1},
    {},
]  # transform() result  # flush() result


class TestLicenseValidatorTransform(AbstractBinaryTransformTest):
    """
    Extends the super-class to define the test data for the tests defined there.
    The name of this class MUST begin with the word Test so that pytest recognizes it as a test class.
    """

    def get_test_transform_fixtures(self) -> list[tuple]:
        config = {"data_access_factory": [input_data_factory, output_data_factory]}
        fixtures = [
            (
                DatasetExplorerTransform(config),
                [[f_name, data]],
                [],
                expected_metadata_list,
            ),
        ]
        return fixtures