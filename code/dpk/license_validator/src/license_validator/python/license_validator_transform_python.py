from typing import Any

from data_processing.runtime.python import (
    PythonTransformLauncher,
    PythonTransformRuntimeConfiguration,
)
from data_processing.transform.python import DefaultPythonTransformRuntime
from data_processing.utils import get_logger
from license_validator.python import (
    LicenseValidatorTransformConfiguration,
    compute_execution_stats,
)


logger = get_logger(__name__)


class LicenseValidatorRuntimePython(DefaultPythonTransformRuntime):
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


class LicenseValidatorPythonTransformRuntimeConfiguration(
    PythonTransformRuntimeConfiguration
):
    def __init__(self):
        super().__init__(
            transform_config=LicenseValidatorTransformConfiguration(),
            runtime_class=LicenseValidatorRuntimePython,
        )


if __name__ == "__main__":
    # launcher = NOOPRayLauncher()
    launcher = PythonTransformLauncher(
        LicenseValidatorPythonTransformRuntimeConfiguration()
    )
    logger.info("Launching license validator transform")
    launcher.launch()