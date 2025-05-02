import os
import sys

from data_processing.data_access import DataAccessFactory
from data_processing.runtime.python import PythonTransformLauncher
from data_processing.utils import ParamsUtils
from hf_dataset_explorer.python import (
    PythonDataSetsTransformOrchestrator,
    DatasetExplorerPythonTransformRuntimeConfiguration,
)


# create parameters
input_folder = "datasets/"
output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
hf_conf_input = {
    "input_folder": input_folder,
}
local_conf_output = {
    "output_folder": output_folder,
}
params = {
    # Data access. Only required parameters are specified
    "input_hf_config": ParamsUtils.convert_to_ast(hf_conf_input),
    "input_max_files": 50,
    "output_local_config": ParamsUtils.convert_to_ast(local_conf_output),
}
if __name__ == "__main__":
    # Set the simulated command line args
    sys.argv = ParamsUtils.dict_to_req(d=params)
    # create launcher
    launcher = PythonTransformLauncher(
        runtime_config=DatasetExplorerPythonTransformRuntimeConfiguration(),
        data_access_factory=[
            DataAccessFactory(cli_arg_prefix="input_"),
            DataAccessFactory(cli_arg_prefix="output_"),
        ],
        orchestrator=PythonDataSetsTransformOrchestrator,
    )
    # Launch the ray actor(s) to process the input
    launcher.launch()