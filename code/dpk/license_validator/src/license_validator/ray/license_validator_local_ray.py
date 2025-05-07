import os
import sys

from data_processing.data_access import DataAccessFactory
from data_processing.utils import ParamsUtils
from data_processing.runtime.ray import RayTransformLauncher
from license_validator.python import (
    default_license_column,
    license_content_column_cli_param,
)
from license_validator.ray import LicenseValidatorRayTransformConfiguration


# create parameters
input_folder = "datasets/blublinsky/test/data/aai_Latn/train/"
output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
hf_conf_input = {
    "input_folder": input_folder,
}
local_conf_output = {
    "output_folder": output_folder,
}
worker_options = {"num_cpus": 0.8}
params = {
    # where to run
    "run_locally": True,
    # Data access. Only required parameters are specified
    "input_hf_config": ParamsUtils.convert_to_ast(hf_conf_input),
    "output_local_config": ParamsUtils.convert_to_ast(local_conf_output),
    # orchestrator
    "runtime_worker_options": ParamsUtils.convert_to_ast(worker_options),
    "runtime_num_workers": 3,
    "runtime_creation_delay": 0,
    # license validator params
    license_content_column_cli_param: default_license_column,
}
if __name__ == "__main__":
    # Set the simulated command line args
    sys.argv = ParamsUtils.dict_to_req(d=params)
    # create launcher
    launcher = RayTransformLauncher(
        runtime_config=LicenseValidatorRayTransformConfiguration(),
        data_access_factory=[
            DataAccessFactory(cli_arg_prefix="input_"),
            DataAccessFactory(cli_arg_prefix="output_"),
        ],
    )
    # Launch the ray actor(s) to process the input
    launcher.launch()
