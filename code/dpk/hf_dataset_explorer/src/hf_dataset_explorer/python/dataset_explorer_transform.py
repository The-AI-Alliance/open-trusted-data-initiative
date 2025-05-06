from argparse import ArgumentParser, Namespace
from typing import Any

from data_processing.transform import AbstractBinaryTransform, TransformConfiguration
from data_processing.utils import (
    CLIArgumentProvider,
    UnrecoverableException,
    get_logger,
)


short_name = "explorer"
cli_prefix = f"{short_name}_"


def compute_execution_stats(stats: dict[str, Any]) -> dict[str, Any]:
    # compute execution statistics
    failed_to_get_license = stats.get("failed to get license", 0)
    source_doc_count = stats["source_files"]
    to_del = ["failed to get license"]
    to_add = {
        "% failed to get license": round(
            (failed_to_get_license / source_doc_count) * 100, 2
        )
    }
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


class DatasetExplorerTransform(AbstractBinaryTransform):
    """
    Transform implementation
    """

    def __init__(self, config: dict[str, Any]):
        """
        Initialize based on the dictionary of configuration information.
        This is generally called with configuration parsed from the CLI arguments defined
        by the companion runtime, DatasetExplorerTransformRuntime.  If running inside the RayMutatingDriver,
        these will be provided by that class with help from the RayMutatingDriver.
        Make sure that the param name corresponds to the name used in apply_input_params method
        of DatasetExplorerTransformConfiguration class
        """
        super().__init__(config)
        # get data access factory
        data_access_factory = config.get("data_access_factory", None)
        if data_access_factory is None:
            raise UnrecoverableException("could not get data access factory")
        self.data_access = data_access_factory[0].create_data_access()
        data_access_out = data_access_factory[1].create_data_access()
        self.data_access.set_output_data_access(data_access_out)
        self.logger = get_logger(__name__)

    def transform_binary(
        self, file_name: str, byte_array: bytes
    ) -> tuple[list[tuple[bytes, str]], dict[str, Any]]:
        """
        Converts input file into o or more output files.
        If there is an error, an exception must be raised - exit()ing is not generally allowed.
        :param byte_array: contents of the input file to be transformed.
        :param file_name: the name of the file containing the given byte_array.
        :return: a tuple of a list of 0 or more tuples and a dictionary of statistics that will be propagated
        to metadata.  Each element of the return list, is a tuple of the transformed bytes and a string
        holding the extension to be used when writing out the new bytes.
        """
        self.logger.debug("Transforming next Readme file")
        metadata = {}
        # get dataset card and license
        try:
            content = byte_array.decode("utf-8")
            data_card = self.data_access.readme_to_repocard(content=content)
            license = data_card.data.license
            if license is None or len(license) == 0:
                license = "none"
            metadata[f"license_{license}"] = 1
        except Exception as e:
            self.logger.error(
                f"error getting license info for file {file_name}, error {e}"
            )
            metadata["failed to get license"] = 1
        # result
        return [], metadata


class DatasetExplorerTransformConfiguration(TransformConfiguration):
    """
    Provides support for configuring and using the associated Transform class include
    configuration with CLI args.
    """

    def __init__(self):
        super().__init__(
            name=short_name,
            transform_class=DatasetExplorerTransform,
        )
        from data_processing.utils import get_logger

        self.logger = get_logger(__name__)

    def add_input_params(self, parser: ArgumentParser) -> None:
        """
        Add Transform-specific arguments to the given  parser.
        This will be included in a dictionary used to initialize the DatasetExplorerTransform.
        By convention a common prefix should be used for all transform-specific CLI args
        (e.g, noop_, pii_, etc.)
        """
        pass

    def apply_input_params(self, args: Namespace) -> bool:
        """
        Validate and apply the arguments that have been parsed
        :param args: user defined arguments.
        :return: True, if validate pass or False otherwise
        """
        captured = CLIArgumentProvider.capture_parameters(args, cli_prefix, False)
        self.params = self.params | captured
        self.logger.info(f"Dataset explorer parameters are : {self.params}")
        return True
