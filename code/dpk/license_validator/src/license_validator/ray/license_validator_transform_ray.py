from typing import Any

from data_processing.utils import get_logger
from data_processing.runtime.ray import (
    RayTransformLauncher,
    RayTransformRuntimeConfiguration,
)
from data_processing.transform.ray import DefaultRayTransformRuntime
from license_validator.python import (
    LicenseValidatorTransformConfiguration,
    compute_execution_stats,
)


logger = get_logger(__name__)


class LicenseValidatorRuntimeRay(DefaultRayTransformRuntime):
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
        # compute and add additional statistics
        return compute_execution_stats(stats=stats)


class LicenseValidatorRayTransformConfiguration(RayTransformRuntimeConfiguration):
    """
    Implements the RayTransformConfiguration for LicenseValidator as required by the RayTransformLauncher.
    LicenseValidator does not use a RayRuntime class so the superclass only needs the base
    python-only configuration.
    """

    def __init__(self):
        """
        Initialization
        """
        super().__init__(
            transform_config=LicenseValidatorTransformConfiguration(),
            runtime_class=LicenseValidatorRuntimeRay,
        )


if __name__ == "__main__":
    # launcher = LicenseValidatorRayLauncher()
    launcher = RayTransformLauncher(LicenseValidatorRayTransformConfiguration())
    logger.info("Launching License validator transform")
    launcher.launch()
