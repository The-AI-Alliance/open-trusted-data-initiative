from typing import Any

from data_processing.utils import get_logger
from data_processing.runtime.ray import (
    RayTransformLauncher,
    RayTransformRuntimeConfiguration,
)
from data_processing.transform.ray import DefaultRayTransformRuntime
from hf_dataset_explorer.python import (
    DatasetExplorerTransformConfiguration,
    compute_execution_stats,
)
from hf_dataset_explorer.ray import RayDataSetsTransformOrchestrator


logger = get_logger(__name__)


class DatasetExplorerRuntimeRay(DefaultRayTransformRuntime):
    """
    Exact dedup runtime support
    """

    def __init__(self, params: dict[str, Any]):
        super().__init__(params=params)

    def compute_execution_stats(self, stats: dict[str, Any]) -> dict[str, Any]:
        """
        Update/augment the given stats object with runtime-specific additions/modifications.
        :param stats: output of statistics as aggregated across all calls to all transforms.
        :return: job execution statistics.  These are generally reported as metadata by the Ray Orchestrator.
        """
        return compute_execution_stats(stats=stats)


class DatasetExplorerRayTransformConfiguration(RayTransformRuntimeConfiguration):
    """
    Implements the RayTransformConfiguration for DatasetExplorer as required by the RayTransformLauncher.
    DatasetExplorer does not use a RayRuntime class so the superclass only needs the base
    python-only configuration.
    """

    def __init__(self):
        """
        Initialization
        """
        super().__init__(
            transform_config=DatasetExplorerTransformConfiguration(),
            runtime_class=DatasetExplorerRuntimeRay,
        )


if __name__ == "__main__":
    # launcher = DatasetExplorerRayLauncher()
    launcher = RayTransformLauncher(
        runtime_config=DatasetExplorerRayTransformConfiguration(),
        orchestrator=RayDataSetsTransformOrchestrator,
    )
    logger.info("Launching License validator transform")
    launcher.launch()
