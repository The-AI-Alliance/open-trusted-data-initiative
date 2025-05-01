from argparse import Namespace
from typing import Any

from data_processing.runtime.python import (
    PythonTransformLauncher,
    PythonTransformRuntimeConfiguration,
)
from data_processing.transform.python import DefaultPythonTransformRuntime
from data_processing.utils import get_logger
from hf_dataset_explorer.python import (
    DatasetExplorerTransformConfiguration,
    compute_execution_stats,
    PythonDataSetsTransformOrchestrator,
)


logger = get_logger(__name__)


class DatasetExplorerTransformPythonConfiguration(
    DatasetExplorerTransformConfiguration
):
    def apply_input_params(self, args: Namespace) -> bool:
        if args.runtime_num_processors > 0:
            self.logger.info(
                f"dataset explorer does not support multiprocessing. Runtime_num_processors should be 0, "
                f"current {args.runtime_num_processors}"
            )
            return False
        return super().apply_input_params(args=args)


class DatasetExplorerRuntimePython(DefaultPythonTransformRuntime):
    """
    Exact dedup runtime support
    """

    def __init__(self, params: dict[str, Any]):
        super().__init__(params=params)

    def compute_execution_stats(self, stats: dict[str, Any]) -> dict[str, Any]:
        """
        Update/augment the given statistics object with runtime-specific additions/modifications.
        :param stats: output of statistics as aggregated across all calls to all transforms.
        :return: job execution statistics.  These are generally reported as metadata by the Ray Orchestrator.
        """
        # compute and add additional statistics
        return compute_execution_stats(stats=stats)


class DatasetExplorerPythonTransformRuntimeConfiguration(
    PythonTransformRuntimeConfiguration
):
    def __init__(self):
        super().__init__(
            transform_config=DatasetExplorerTransformPythonConfiguration(),
            runtime_class=DatasetExplorerRuntimePython,
        )


if __name__ == "__main__":
    # launcher = NOOPRayLauncher()
    launcher = PythonTransformLauncher(
        runtime_config=DatasetExplorerPythonTransformRuntimeConfiguration(),
        orchestrator=PythonDataSetsTransformOrchestrator,
    )
    logger.info("Launching license validator transform")
    launcher.launch()
