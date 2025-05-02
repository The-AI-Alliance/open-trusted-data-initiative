from argparse import ArgumentParser, Namespace
from typing import Any

import pyarrow as pa
from data_processing.transform import AbstractTableTransform, TransformConfiguration
from data_processing.utils import CLIArgumentProvider


short_name = "license"
cli_prefix = f"{short_name}_"
license_content_column_key = "license_column"
license_content_column_cli_param = f"{cli_prefix}{license_content_column_key}"

default_license_column = "license"


def compute_execution_stats(stats: dict[str, Any]) -> dict[str, Any]:
    # compute execution statistics
    source_doc_count = stats["source_doc_count"]
    to_del = []
    to_add = {}
    for key in stats.keys():
        if key.startswith("license_"):
            # its license count
            to_del.append(key)
            c_license = key.split(sep="_")[1]
            count = stats[key]
            to_add[f"% with license {c_license}"] = round(
                (count / source_doc_count) * 100, 2
            )
    for key in to_del:
        stats.pop(key, None)
    return stats | to_add


class LicenseValidatorTransform(AbstractTableTransform):
    """
    Implements a simple copy of a pyarrow Table.
    """

    def __init__(self, config: dict[str, Any]):
        """
        Initialize based on the dictionary of configuration information.
        This is generally called with configuration parsed from the CLI arguments defined
        by the companion runtime, LicenseValidatorTransformRuntime.  If running inside the RayMutatingDriver,
        these will be provided by that class with help from the RayMutatingDriver.
        Make sure that the param name corresponds to the name used in apply_input_params method
        of LicenseValidatorTransformConfiguration class
        """
        super().__init__(config)
        self.license_column = config.get(
            license_content_column_key, default_license_column
        )

    def transform(
            self, table: pa.Table, file_name: str = None
    ) -> tuple[list[pa.Table], dict[str, Any]]:
        """
        Put Transform-specific to convert one Table to 0 or more tables. It also returns
        a dictionary of execution statistics - arbitrary dictionary
        This implementation makes no modifications so effectively implements a copy of the
        input parquet to the output folder, without modification.
        """
        self.logger.debug(f"Transforming one table with {len(table)} rows")
        metadata = {}
        columns = table.column_names
        if self.license_column in columns:
            # we have a license column, check it values
            for lic in table[self.license_column]:
                current_license = lic.as_py()
                if current_license is None or len(current_license) == 0:
                    # empty one
                    metadata["license_none"] = metadata.get("license_none", 0) + 1
                else:
                    key = f"license_{current_license}"
                    metadata[key] = metadata.get(key, 0) + 1
        else:
            # no license column
            metadata["license_none"] = table.num_rows
        # return result - just metadata
        return [], metadata


class LicenseValidatorTransformConfiguration(TransformConfiguration):
    """
    Provides support for configuring and using the associated Transform class include
    configuration with CLI args.
    """

    def __init__(self):
        super().__init__(
            name=short_name,
            transform_class=LicenseValidatorTransform,
        )
        from data_processing.utils import get_logger

        self.logger = get_logger(__name__)

    def add_input_params(self, parser: ArgumentParser) -> None:
        """
        Add Transform-specific arguments to the given  parser.
        This will be included in a dictionary used to initialize the LicenseValidatorTransform.
        By convention a common prefix should be used for all transform-specific CLI args
        (e.g, noop_, pii_, etc.)
        """
        parser.add_argument(
            f"--{license_content_column_cli_param}",
            type=str,
            default=default_license_column,
            help="name of the table column containing license",
        )

    def apply_input_params(self, args: Namespace) -> bool:
        """
        Validate and apply the arguments that have been parsed
        :param args: user defined arguments.
        :return: True, if validate pass or False otherwise
        """
        captured = CLIArgumentProvider.capture_parameters(args, cli_prefix, False)
        self.params = self.params | captured
        self.logger.info(f"license validator parameters are : {self.params}")
        return True