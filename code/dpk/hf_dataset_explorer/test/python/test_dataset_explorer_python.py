import os

from data_processing.data_access import DataAccessFactory
from data_processing.runtime.python import PythonTransformLauncher
from hf_dataset_explorer.python import (
    AbstractDataSetsTransformLauncherTest,
    PythonDataSetsTransformOrchestrator,
    DatasetExplorerPythonTransformRuntimeConfiguration,
)


class TestPythonDatasetExplorerTransform(AbstractDataSetsTransformLauncherTest):
    """
    Extends the super-class to define the test data for the tests defined there.
    The name of this class MUST begin with the word Test so that pytest recognizes it as a test class.
    """

    def get_test_transform_fixtures(self) -> list[tuple]:
        fixtures = []
        launcher = PythonTransformLauncher(
            runtime_config=DatasetExplorerPythonTransformRuntimeConfiguration(),
            data_access_factory=[
                DataAccessFactory(cli_arg_prefix="input_"),
                DataAccessFactory(cli_arg_prefix="output_"),
            ],
            orchestrator=PythonDataSetsTransformOrchestrator,
        )
        input_dir = ""
        expected_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../test-data/expected")
        )
        transform_config = {"input_max_files": 5}
        fixtures.append(
            (
                launcher,
                transform_config,
                input_dir,
                expected_dir,
                [],  # optional list of column names to ignore in comparing test-generated with expected.
            )
        )

        return fixtures