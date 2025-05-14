import sys
import tempfile
from typing import Any

from data_processing.runtime.transform_launcher import AbstractTransformLauncher
from data_processing.test_support.launch.transform_test import (
    AbstractTransformLauncherTest,
)
from data_processing.utils import ParamsUtils


class AbstractDataSetsTransformLauncherTest(AbstractTransformLauncherTest):
    """
    Extension to the AbstractTransformLauncherTest supporting Datasets
    """

    def test_transform(
        self,
        launcher: AbstractTransformLauncher,
        cli_params: dict[str, Any],
        in_table_path: str,
        expected_out_table_path: str,
        ignore_columns: list[str],
    ):
        """
        Test the given transform and its runtime using the given CLI arguments, input directory of data files and expected output directory.
        Data is processed into a temporary output directory which is then compared with the directory of expected output.
        :param launcher: launcher configured to run the transform being tested
        :param cli_params: a map of the simulated CLI arguments (w/o --).  This includes both the transform-specific CLI parameters and the launching args.
        :param in_table_path: a directory containing the input parquet files to be processed and results compared against the expected output table path.
        :param expected_out_table_path: directory contain parquet and metadata.json that is expected to match the processed input directory.
        :return:
        """
        prefix = launcher.get_transform_name()
        with tempfile.TemporaryDirectory(prefix=prefix, dir="/tmp") as temp_dir:
            print(f"Using temporary output path {temp_dir}")
            sys.argv = self._get_argv(cli_params, in_table_path, temp_dir)
            launcher.launch()
            self._validate_directory_contents_match(
                temp_dir, expected_out_table_path, ignore_columns
            )

    @staticmethod
    def _get_argv(cli_params: dict[str, Any], in_table_path: str, out_table_path: str):
        args = {} | cli_params
        hf_conf_input = {"input_folder": "datasets/"}
        local_conf_output = {
            "output_folder": out_table_path,
        }
        args["input_hf_config"] = ParamsUtils.convert_to_ast(hf_conf_input)
        args["output_local_config"] = ParamsUtils.convert_to_ast(local_conf_output)
        argv = ParamsUtils.dict_to_req(args)
        return argv
